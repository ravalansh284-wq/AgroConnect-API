from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password,create_access_token,get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse

router=APIRouter()

@router.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate,db: Session=Depends(get_db)):
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400,detail="Email already registered")
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400,detail="Username already taken")
    
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}