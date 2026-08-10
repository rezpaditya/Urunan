# Firebase (Cloud Firestore) setup for Urunan

Cloud sync is **optional**. Urunan works fully offline with everything in
`localStorage`; this guide only applies if you want trips to sync live across
your devices through a free [Firebase](https://firebase.google.com/) project.

When `FIREBASE_CONFIG` (near the top of `urunan.html`) is left blank, all sync
UI is hidden and the app is 100% local — so you can skip this entirely.

Everything below fits comfortably in Firebase's free **Spark** plan for
personal use.

---

## 1. Create a Firebase project

1. Go to the [Firebase console](https://console.firebase.google.com/) and
   **Add project** (or reuse an existing Google Cloud project).
2. Analytics is optional — you can turn it off.

## 2. Register a Web app and copy the config

1. In the project, click the **Web** icon (`</>`) to *Add an app*.
2. Give it a nickname (e.g. `urunan-web`). You do **not** need Firebase Hosting.
3. Firebase shows a `firebaseConfig` object. Copy these four fields into
   `FIREBASE_CONFIG` in `urunan.html`:

   ```js
   const FIREBASE_CONFIG = {
     apiKey: 'AIza…',
     authDomain: 'your-project.firebaseapp.com',
     projectId: 'your-project',
     appId: '1:1234567890:web:abc123'
   };
   ```

   These values are **not secrets** — a web Firebase config is designed to ship
   in client-side code. Access is controlled by the security rules in step 5,
   not by hiding this object, so it's fine to commit.

## 3. Enable Anonymous Authentication

Every device signs in anonymously so the security rules can require an
authenticated caller (and so no login screen is needed).

1. **Build → Authentication → Get started**.
2. **Sign-in method → Anonymous → Enable → Save**.

## 4. Create the Firestore database

1. **Build → Firestore Database → Create database**.
2. Pick a location close to you (this can't be changed later).
3. Start in **production mode** — you'll paste explicit rules next.

## 5. Publish the security rules

**Firestore Database → Rules**, replace the contents with the following, and
**Publish**:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // A trip document id is an unguessable 128-bit random value that acts as a
    // capability: it is only ever shared through the #fs=<id> link/QR. Any
    // signed-in caller who knows a document id may read/write that one trip.
    match /trips/{tripId} {
      allow read, write: if request.auth != null;
    }

    // The email-keyed restore index (inbox/<hash(email)>). Same model: a
    // signed-in caller who knows the id (derived from an email) may read/write.
    match /inbox/{inboxId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### What these rules do (and don't) protect

- **Require auth.** Only clients that have signed in (Anonymous Auth) can touch
  any document, so the database isn't open to anonymous HTTP.
- **Capability by id.** Trip ids are 128 bits of randomness, shared only via the
  `#fs=` link. In practice you can't reach a trip you were never given a link
  to — this mirrors Urunan's existing "unguessable share link" model.
- **Trade-off — the restore index.** `inbox/<id>` is keyed by a hash of your
  email (not a secret). Anyone who knows your email *and* is signed in could
  read your synced trips' ids from it. That's the deliberate cost of one-tap
  email restore; unsynced trips are never listed. If you don't want that, you
  can delete the `inbox` rule block to disable email restore and rely on sharing
  `#fs=` links by hand.
- **Not row-level ownership.** Because Anonymous Auth gives each device a
  *different* uid, the rules can't scope documents to a single user. If you want
  stricter, per-user ownership, switch to a real sign-in method (Email/Google)
  and add an `ownerUid` field with rules like
  `allow read, write: if request.auth.uid == resource.data.ownerUid;`.

## 6. Try it

1. Open your deployed `urunan.html`, create a trip, open it, and tap
   **Share → Enable cloud sync**.
2. Open the shown `#fs=…` link (or scan the QR) on another device/browser — the
   trip appears and stays in sync both ways.
3. On a fresh device, log in with the **same email** and tap **Restore synced
   trips** to pull them all back.

## Costs

Firestore's free tier (as of writing) includes 1 GiB stored plus tens of
thousands of reads/writes per day — far beyond what a personal bill-splitting
app uses. Sync is push-based (`onSnapshot`), not polling, so an idle app makes
no ongoing requests. Watch usage in the Firebase console if you share widely.
