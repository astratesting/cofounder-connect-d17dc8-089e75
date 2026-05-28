from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import api, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='CoFounder Connect API',
    description='AI-driven co-founder matching, chat, video room links, pitch deck uploads, and subscription management.',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://*.vercel.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(api.router)

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'cofounder-connect'}
