from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, DateTime, Text, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Configurez la base de données
SQLALCHEMY_DATABASE_URL = "sqlite:///./bdd.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Définissez le modèle de données pour le compte utilisateur
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    pseudo = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.now())

class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.now())
    id_1 = Column(Integer, ForeignKey('user.id'), nullable=False)
    
class Commentaire(Base):
    __tablename__ = "commentaire"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.now())
    id_1 = Column(Integer, ForeignKey('video.id'), nullable=False)
    id_2 = Column(Integer, ForeignKey('user.id'), nullable=False)
    
class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)

class Aime(Base):
    __tablename__ = "aime"
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    id_1 = Column(Integer, ForeignKey('video.id'), primary_key=True)    
    

class View(Base):
    __tablename__ = "view"
    id = Column(Integer, primary_key=True, index=True)    
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    id_1 = Column(Integer, ForeignKey('video.id'), primary_key=True)    

class Contient(Base):
    __tablename__ = "contient"
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    id_1 = Column(Integer, ForeignKey('video.id'), primary_key=True)    


# Créez la table dans la base de données
Base.metadata.create_all(bind=engine)

# Modèle pour la création d'un utilisateur
class CreateUserRequest(BaseModel):
    username: str
    password: str


app = FastAPI()


# Créer un compte utilisateur
@app.post("/user")
def create_user(user: CreateUserRequest):
    db = SessionLocal()
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Utilisateur créé avec succès"}


# Authentifier un utilisateur
@app.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect.")
    return {"message": "Connexion réussie"}


# Récupérer les détails d'un utilisateur
@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    return {"username": user.username}


# Mettre à jour les informations de l'utilisateur
@app.put("/users/{user_id}")
def update_user(user_id: int, user: CreateUserRequest):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà.")
    db_user = db.query(User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    db_user.username = user.username
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return {"message": "Utilisateur mis à jour avec succès"}


# Supprimer un compte utilisateur
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}


