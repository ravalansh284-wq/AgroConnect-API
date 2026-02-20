from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password,create_access_token,get_password_hash
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse

router=APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_role = db.query(Role).filter(Role.name == user.role).first()
    if not user_role:
        raise HTTPException(status_code=400, detail=f"Role '{user.role}' does not exist. (Did you run initial_data.py?)")
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    new_user.roles.append(user_role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
    access_token = create_access_token(subject=user.username, user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}