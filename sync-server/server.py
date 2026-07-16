#!/usr/bin/env python3
"""Urunan device-sync relay.

A stateless rendezvous for syncing Urunan trips between devices. It keeps
nothing on disk and owns no data: each room's payload lives only in memory
and only long enough for another device to pick it up (TTL below), then it
is evicted. Restarting the process wipes every room. The devices' own
localStorage is always the source of truth — this relay just forwards the
most recent push from one device to the next.

Payloads are opaque bytes (the client gzips + AES-GCM encrypts before
sending), so the relay never sees trip contents. Standard library only.

    PUT /room/<id>   store a payload for <id>            -> 204
    GET /room/<id>   fetch the current payload for <id>  -> 200 | 404
    GET /            health check                        -> 200
    OPTIONS *        CORS preflight                      -> 204

Run locally:  PORT=8080 python server.py
"""

import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Room id = 16 random bytes, base64url, unpadded (see the client's genRoomId).
ROOM_ID_RE = re.compile(r"^[A-Za-z0-9_-]{22}$")

TTL_SECONDS = 300          # evict a room this long after its last push
MAX_BODY_BYTES = 128 * 1024  # generous headroom; a trip is a few KB gzipped

_rooms = {}                # id -> (payload_bytes, stored_at_epoch)
_lock = threading.Lock()


def _purge_expired(now):
    """Drop rooms older than the TTL. Caller must hold _lock."""
    stale = [rid for rid, (_, ts) in _rooms.items() if now - ts > TTL_SECONDS]
    for rid in stale:
        del _rooms[rid]


def _get(room_id):
    now = time.time()
    with _lock:
        _purge_expired(now)
        entry = _rooms.get(room_id)
        return entry[0] if entry else None


def _put(room_id, payload):
    now = time.time()
    with _lock:
        _purge_expired(now)
        _rooms[room_id] = (payload, now)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # ── helpers ──────────────────────────────────────────────
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _finish(self, status, body=b"", content_type=None):
        self.send_response(status)
        self._cors()
        if content_type:
            self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body and self.command != "HEAD":
            self.wfile.write(body)

    def _room_id(self):
        """Return a valid room id from the path, or None."""
        m = re.match(r"^/room/([^/]+)$", self.path)
        if not m:
            return None
        rid = m.group(1)
        return rid if ROOM_ID_RE.match(rid) else None

    # ── routes ───────────────────────────────────────────────
    def do_OPTIONS(self):
        self._finish(204)

    def do_GET(self):
        if self.path == "/" or self.path == "/healthz":
            self._finish(200, json.dumps({"status": "ok"}).encode(),
                         "application/json")
            return
        rid = self._room_id()
        if rid is None:
            self._finish(404)
            return
        payload = _get(rid)
        if payload is None:
            self._finish(404)
            return
        self._finish(200, payload, "application/octet-stream")

    def do_PUT(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.close_connection = True
            self._finish(400)
            return
        if length > MAX_BODY_BYTES:
            # Don't drain a huge body; drop the connection instead so its
            # unread bytes can't bleed into the next keep-alive request.
            self.close_connection = True
            self._finish(413)
            return
        # Read (drain) the body before validating so a well-formed but
        # mis-addressed request leaves the connection clean for reuse.
        payload = self.rfile.read(length) if length else b""
        rid = self._room_id()
        if rid is None:
            self._finish(400)
            return
        _put(rid, payload)
        self._finish(204)

    # Quiet the default request logging (Cloud Run captures stdout anyway).
    def log_message(self, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"urunan-sync relay listening on :{port} (ttl={TTL_SECONDS}s)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
