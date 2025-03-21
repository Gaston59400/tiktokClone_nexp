from fastapi import FastAPI
from models import engine, Base
from routes import user_router, video_router, commentaire_router, tag_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(video_router)
app.include_router(commentaire_router)
app.include_router(tag_router)


# Créez la table dans la base de données
Base.metadata.create_all(bind=engine)

