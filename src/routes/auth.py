from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import traceback

from src.config.database import get_db
from src.model.models import User
from src.schema.user import UserCreate
from src.core.security import get_password_hash, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        print("Signup started")  # Debug
        result = await db.execute(select(User).where(User.username == user.username))
        existing_user = result.scalars().first()
        print("Checked existing user")  # Debug

        if existing_user:
            print("Username exists")  # Debug
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = get_password_hash(user.password)
        print("Hashed password")  # Debug

        new_user = User(username=user.username, password=hashed_password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        print("User created and committed")  # Debug

        token = create_access_token(data={"sub": new_user.username})
        print("Token created")  # Debug
        return {"access_token": token, "token_type": "bearer"}

    # Inside signup
    except Exception as e:
        traceback.print_exc()  # ⬅️ This shows the full traceback in terminal
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
