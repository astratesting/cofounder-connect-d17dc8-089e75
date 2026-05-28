# CoFounder Connect

Production MVP for AI-driven co-founder matching with founder profiles, compatibility scoring, chat, video room links, pitch deck PDF uploads, and freemium subscriptions.

## Stack

- Next.js 14 App Router, TypeScript, Tailwind CSS
- Clerk UI for email/password and Google OAuth flows
- Supabase client ready for database/backend integration
- FastAPI backend with SQLAlchemy models for users, matches, subscriptions, pitch decks, and chat
- PostgreSQL via Docker Compose

## Core features

- Landing page with clear founder matching positioning and $29/mo premium plan
- Protected dashboard with ranked matches, chat/video actions, pitch deck state, and upgrade card
- Auth API: `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- Matching API using 30+ weighted compatibility factors
- Chat API with optional video room URL generation
- PDF pitch deck upload endpoint
- Subscription endpoint for free and premium plans

## Local setup

```bash
cp .env.example .env
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000/docs`.

### Full stack with Docker

```bash
docker compose up
```

## Deployment

1. Create Supabase project and add `users`, `matches`, and `subscriptions` tables matching `backend/models.py`.
2. Configure Clerk email/password and Google OAuth.
3. Add frontend environment variables in Vercel.
4. Deploy `frontend` directory to Vercel.
5. Deploy FastAPI service to preferred Python host and set `NEXT_PUBLIC_API_URL`.

## Database schema

- `users`: id, name, email, skills, industry, stage, preferences
- `matches`: user1_id, user2_id, match_score, status
- `subscriptions`: user_id, plan, start_date, end_date
- `pitch_decks`: user_id, filename, url, views
- `chat_messages`: sender_id, receiver_id, body, video_room_url
