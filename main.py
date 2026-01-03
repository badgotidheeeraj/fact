from fastapi import FastAPI, Depends, HTTPException,Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth import Authentication
from typing import List
from database import engine, Base
from models import TeaModel, UserModel
from schemas import Tea, TeaCreate, UserCreate, UserOut

Base.metadata.create_all(bind=engine)




# Adjust or add origins as needed for production.
origins = [
    "http://localhost",
    "https://insurance-prediction-rho.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]







app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register user
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(Authentication.get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = Authentication.get_password_hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# login user
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(Authentication.get_db)
):
    user = db.query(UserModel).filter(
        UserModel.username == form_data.username
    ).first()

    if not user or not Authentication.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = Authentication.create_access_token({"sub": user.username})
    refresh_token = Authentication.create_refresh_token({"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



# @app.post("/refresh")
# def refresh_token(refresh_token: str):
#     try:
#         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

#         if payload.get("type") != "refresh":
#             raise HTTPException(status_code=401, detail="Invalid token type")

#         username = payload.get("sub")
#         if not username:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         new_access_token = create_access_token({"sub": username})

#         return {"access_token": new_access_token, "token_type": "bearer"}

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid refresh token")


@app.post("/teas/", response_model=Tea)
def create_tea(tea: TeaCreate, current_user: UserModel = Depends(Authentication.get_current_user), db: Session = Depends(Authentication.get_db)):
    db_tea = TeaModel(**tea.dict(), owner_id=current_user.id)
    db.add(db_tea)
    db.commit()
    db.refresh(db_tea)
    return db_tea

@app.get("/teas/", response_model=List[Tea])
def get_teas(current_user: UserModel = Depends(Authentication.get_current_user), db: Session = Depends(Authentication.get_db)):
    teas = db.query(TeaModel).filter(TeaModel.owner_id == current_user.id).all()
    return teas

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea API!"}