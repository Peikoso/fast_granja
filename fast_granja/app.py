from fastapi import FastAPI
from fast_granja.admin_create_script import admin_create
from fast_granja.router.user import router as user
from fast_granja.router.flock import router as flock
from fast_granja.router.eggs import router as eggs
from fast_granja.router.chicken.death import router as chicken_death
from fast_granja.router.chicken.race import router as chicken_race
from fast_granja.router.chicken.reason import router as chicken_death_reason
from fast_granja.router.auth import router as auth_router


async def lifespan(app: FastAPI):
    await admin_create()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user, tags=["User"], prefix="/user")
app.include_router(flock, tags=["Flock"], prefix="/flock")
app.include_router(eggs, tags=["Eggs"], prefix="/eggs")
app.include_router(chicken_death, tags=["Chicken Death"], prefix="/chicken_death")
app.include_router(chicken_race, tags=["Chicken Race"], prefix="/chicken_race")
app.include_router(
    chicken_death_reason, tags=["Chicken Death Reason"], prefix="/chicken_death_reason"
)
app.include_router(auth_router, tags=["Auth"], prefix="/auth")


@app.get("/")
async def root():
    return "Bem vindo a Fast Granja"
