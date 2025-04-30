from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from src.model.models import User
from src.schema.user import UserCreate
from src.core.security import get_password_hash, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signin")
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print("Signin error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
