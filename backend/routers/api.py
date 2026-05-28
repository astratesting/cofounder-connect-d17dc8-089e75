import json
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from models import ChatMessage, Match, PitchDeck, Subscription, User
from routers.auth import get_current_user, serialize_user, UserResponse

router = APIRouter(prefix='/api', tags=['cofounder-connect'])

class ProfileUpdate(BaseModel):
    name: str | None = None
    skills: list[str] | None = None
    industry: str | None = None
    stage: str | None = None
    preferences: dict | None = None

class MatchResponse(BaseModel):
    id: int
    founder: UserResponse
    match_score: float
    status: str
    reasons: list[str]

class MessageCreate(BaseModel):
    receiver_id: int
    body: str = Field(min_length=1, max_length=2000)
    include_video_room: bool = False

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    body: str
    video_room_url: str | None
    created_at: datetime

class SubscriptionUpdate(BaseModel):
    plan: str = Field(pattern='^(free|premium)$')

class SubscriptionResponse(BaseModel):
    plan: str
    start_date: datetime
    end_date: datetime | None

class PitchDeckResponse(BaseModel):
    id: int
    filename: str
    url: str
    views: int

SIGNAL_WEIGHTS = {
    'shared_skill': 10,
    'industry_match': 18,
    'stage_match': 14,
    'complementary_skill': 8,
    'availability': 6,
    'fundraising': 5,
    'location': 4,
    'risk': 4,
    'customer_access': 4,
    'technical_depth': 4,
    'sales_depth': 4,
    'domain_expertise': 4,
    'company_type': 3,
    'timeline': 3,
    'equity_expectation': 3,
    'communication_style': 3,
    'decision_speed': 3,
    'remote_preference': 3,
    'network_strength': 3,
    'prior_startups': 3,
    'operator_experience': 3,
    'product_sense': 3,
    'design_sense': 2,
    'go_to_market': 2,
    'enterprise_experience': 2,
    'consumer_experience': 2,
    'regulated_industry': 2,
    'capital_efficiency': 2,
    'mission_alignment': 2,
    'work_hours': 2,
    'learning_velocity': 2
}

def _skills(user: User) -> set[str]:
    return {skill.lower() for skill in json.loads(user.skills or '[]')}

def score_match(current: User, candidate: User) -> tuple[float, list[str]]:
    score = 35.0
    reasons: list[str] = []
    overlap = _skills(current) & _skills(candidate)
    if overlap:
        score += min(20, len(overlap) * SIGNAL_WEIGHTS['shared_skill'])
        reasons.append(f"Shared skills: {', '.join(sorted(overlap))}")
    if current.industry and current.industry == candidate.industry:
        score += SIGNAL_WEIGHTS['industry_match']
        reasons.append(f'Both building in {current.industry}')
    if current.stage and current.stage == candidate.stage:
        score += SIGNAL_WEIGHTS['stage_match']
        reasons.append(f'Same company stage: {current.stage}')
    candidate_skills = _skills(candidate)
    if {'sales', 'growth', 'fundraising'} & candidate_skills and {'engineering', 'product', 'ml'} & _skills(current):
        score += SIGNAL_WEIGHTS['complementary_skill']
        reasons.append('Complementary technical and GTM coverage')
    preferences = json.loads(current.preferences or '{}')
    candidate_preferences = json.loads(candidate.preferences or '{}')
    for key in ['availability', 'location', 'risk', 'timeline', 'remote_preference', 'mission_alignment', 'work_hours']:
        if preferences.get(key) and preferences.get(key) == candidate_preferences.get(key):
            score += SIGNAL_WEIGHTS.get(key, 2)
            reasons.append(f'Aligned {key.replace("_", " ")}')
    return min(round(score, 1), 99.0), reasons[:5] or ['Strong baseline profile compatibility']

@router.get('/profiles', response_model=list[UserResponse])
def profiles(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).limit(50).all()
    return [serialize_user(user) for user in users]

@router.put('/profiles/me', response_model=UserResponse)
def update_profile(payload: ProfileUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    for field in ['name', 'industry', 'stage']:
        value = getattr(payload, field)
        if value is not None:
            setattr(current_user, field, value)
    if payload.skills is not None:
        current_user.skills = json.dumps(payload.skills)
    if payload.preferences is not None:
        current_user.preferences = json.dumps(payload.preferences)
    db.commit()
    db.refresh(current_user)
    return serialize_user(current_user)

@router.get('/matches', response_model=list[MatchResponse])
def matches(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    candidates = db.query(User).filter(User.id != current_user.id).limit(20).all()
    responses: list[MatchResponse] = []
    for candidate in candidates:
        score, reasons = score_match(current_user, candidate)
        match = db.query(Match).filter(Match.user1_id == current_user.id, Match.user2_id == candidate.id).first()
        if not match:
            match = Match(user1_id=current_user.id, user2_id=candidate.id, match_score=score, status='suggested')
            db.add(match)
            db.flush()
        else:
            match.match_score = score
        responses.append(MatchResponse(id=match.id, founder=serialize_user(candidate), match_score=score, status=match.status, reasons=reasons))
    db.commit()
    return sorted(responses, key=lambda item: item.match_score, reverse=True)

@router.post('/matches/{match_id}/status')
def update_match_status(match_id: int, status_value: str, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    match = db.get(Match, match_id)
    if not match or current_user.id not in {match.user1_id, match.user2_id}:
        raise HTTPException(status_code=404, detail='Match not found')
    if status_value not in {'suggested', 'accepted', 'dismissed'}:
        raise HTTPException(status_code=400, detail='Invalid status')
    match.status = status_value
    db.commit()
    return {'status': match.status}

@router.post('/chat', response_model=MessageResponse)
def send_message(payload: MessageCreate, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    receiver = db.get(User, payload.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail='Receiver not found')
    room = f'https://meet.jit.si/cofounder-connect-{current_user.id}-{receiver.id}' if payload.include_video_room else None
    message = ChatMessage(sender_id=current_user.id, receiver_id=receiver.id, body=payload.body, video_room_url=room)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get('/chat/{other_user_id}', response_model=list[MessageResponse])
def conversation(other_user_id: int, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == other_user_id)) |
        ((ChatMessage.sender_id == other_user_id) & (ChatMessage.receiver_id == current_user.id))
    ).order_by(ChatMessage.created_at.asc()).all()
    return messages

@router.post('/pitch-decks', response_model=PitchDeckResponse)
def upload_pitch_deck(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)], file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Only PDF pitch decks are supported')
    deck = PitchDeck(user_id=current_user.id, filename=file.filename or 'pitch-deck.pdf', url=f'/uploads/{current_user.id}/{file.filename or "pitch-deck.pdf"}')
    db.add(deck)
    db.commit()
    db.refresh(deck)
    return deck

@router.get('/pitch-decks', response_model=list[PitchDeckResponse])
def list_pitch_decks(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    return db.query(PitchDeck).filter(PitchDeck.user_id == current_user.id).all()

@router.put('/subscriptions/me', response_model=SubscriptionResponse)
def update_subscription(payload: SubscriptionUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not subscription:
        subscription = Subscription(user_id=current_user.id)
        db.add(subscription)
    subscription.plan = payload.plan
    subscription.start_date = datetime.utcnow()
    subscription.end_date = datetime.utcnow() + timedelta(days=30) if payload.plan == 'premium' else None
    db.commit()
    db.refresh(subscription)
    return subscription
