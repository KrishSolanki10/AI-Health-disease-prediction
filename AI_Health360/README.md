# AI-Health360 — Intelligent Disease Prediction & Healthcare Assistant

Phase 1 status: **project scaffold + MySQL schema ready.**
Everything below runs, but most routes/pages are stubs — they get filled in
during their dedicated phase (see the phase list at the bottom).

## Project structure

```
AI_Health360/
├── backend/          Flask API (routes, models, ml/ for trained models)
├── frontend/          React + Vite + Tailwind
├── database/           schema.sql
├── datasets/            raw CSVs go here (diabetes.csv, heart.csv, ...)
├── trained_models/     .pkl files produced during Phase 3-5
└── reports/               generated PDF reports land here
```

## 1. Set up MySQL

Make sure MySQL server is running locally, then:

```bash
mysql -u root -p < database/schema.sql
```

This creates the `ai_health360` database with `users`, `predictions`,
`health_records`, and `reports` tables.

## 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env -> set DB_USER / DB_PASSWORD to your MySQL credentials

python app.py
```

Server runs at `http://localhost:5000`. Confirm it's alive:

```bash
curl http://localhost:5000/api/ping
```

You should get back `{"status": "ok", "service": "AI-Health360 backend"}`.

## 3. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`. API calls to `/api/*` are proxied to the
Flask backend on port 5000 (see `vite.config.js`).

## What's actually working right now

- Flask app boots, connects to MySQL via SQLAlchemy, exposes `/api/ping`.
- Five blueprints registered (`auth`, `predict`, `chatbot`, `health`,
  `reports`) — each has one `/status` stub route just to prove wiring works.
- Three core models defined: `User`, `Prediction`, `HealthRecord`.
- React app boots with React Router wired to 6 placeholder pages
  (Login, Dashboard, Prediction, Chatbot, Reports, Admin).
- Tailwind configured and working.

## What's NOT built yet (upcoming phases)

| Phase | Deliverable |
|-------|-------------|
| 2 | Real authentication (register/login, JWT, role-based access) |
| 3 | Diabetes prediction model + API |
| 4 | Heart disease prediction model + API |
| 5 | Liver + Kidney models |
| 6 | Unified prediction API + model comparison endpoint |
| 7 | Real React dashboard (health score, trends, last prediction) |
| 8 | AI Healthcare Assistant (NLP/LLM chatbot) |
| 9 | Health analytics charts (BP/weight/glucose trends) |
| 10 | PDF report generation (ReportLab) |
| 11 | Doctor/Admin panel |
| 12 | Testing, deployment, documentation |

## Next step

Phase 2: authentication. Bolo jab ready ho.
