from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from app.core.security import hash_password, verify_password, create_access_token, generate_api_key
from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models import User, APIKey

router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class APIKeyRequest(BaseModel):
    name: str
    mode: str = "test"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="email_already_registered")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    await db.flush()
    return {"id": str(user.id), "email": user.email, "name": user.name}


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email, User.is_active == True))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid_credentials")

    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/api-keys")
async def create_api_key(
    data: APIKeyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.mode not in ("test", "live"):
        raise HTTPException(status_code=400, detail="mode must be 'test' or 'live'")

    raw_key, key_hash = generate_api_key(data.mode)
    api_key = APIKey(
        user_id=current_user.id,
        name=data.name,
        key_hash=key_hash,
        key_prefix=raw_key[:12],
        mode=data.mode,
    )
    db.add(api_key)
    await db.flush()

    return {
        "id": str(api_key.id),
        "name": api_key.name,
        "mode": api_key.mode,
        "key": raw_key,
        "prefix": api_key.key_prefix,
    }


@router.get("/api-keys")
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(APIKey).where(APIKey.user_id == current_user.id, APIKey.is_active == True)
    )
    keys = result.scalars().all()
    return [{"id": str(k.id), "name": k.name, "mode": k.mode, "prefix": k.key_prefix} for k in keys]


@router.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(APIKey).where(APIKey.id == key_id, APIKey.user_id == current_user.id)
    )
    key = result.scalar_one_or_none()
    if not key:
        raise HTTPException(status_code=404, detail="key_not_found")
    key.is_active = False
    return {"status": "revoked"}
