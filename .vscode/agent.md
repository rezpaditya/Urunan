# agent.md — .vscode

Editor (VS Code) settings for local development.

## Files

- `launch.json` — Debug launch configurations:
  - **Python Debugger: FastAPI** — runs `backend.main:app` under `uvicorn`.
  - **Client Vue3** — runs `npm run dev` in the `frontend/` directory.

## Notes

- These configs target the **archived** FastAPI backend and Vue/Vite frontend,
  not the current single-file `urunan.html` app. They're kept for anyone
  reviving the archived stack under `archived/`.
- The current app needs no launch config — just open `urunan.html` in a browser.
