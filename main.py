from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db import engine, get_db
import tables.users as user_tables
from schemas import UserBase, UserUpdate, UserResponse, Token
from app.auth import hash_password, verify_password, create_access_token, verify_token
from app.dependencies import get_current_active_user

user_tables.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Routes
@app.get("/")
async def root():
    return {"status": "API is running"}

@app.get("/profile", response_model=UserResponse)
def profile(current_user=Depends(get_current_active_user)):
    return current_user

@app.post("/users", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Check if user exists by email or username
    if db.query(user_tables.Users).filter(
        (user_tables.Users.email == user.email) |
        (user_tables.Users.username == user.username)
    ).first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = user_tables.Users(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_tables.Users).filter(user_tables.Users.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_tables.Users).filter(user_tables.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(user_tables.Users).filter(user_tables.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email:
        if db.query(user_tables.Users).filter(
            user_tables.Users.email == user_update.email,
            user_tables.Users.id != user_id
        ).first():
            raise HTTPException(status_code=400, detail="Email already in use")

    if user_update.username:
        if db.query(user_tables.Users).filter(
            user_tables.Users.username == user_update.username,
            user_tables.Users.id != user_id
        ).first():
            raise HTTPException(status_code=400, detail="Username already in use")

    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_tables.Users).filter(user_tables.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


