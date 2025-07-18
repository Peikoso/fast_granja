from fastapi import FastAPI
from fast_granja.router.user_router import router as user
from fast_granja.router.flock_router import router as flock
from fast_granja.router.eggs_router import router as eggs
from fast_granja.router.chicken.death_router import router as chicken_death
from fast_granja.router.chicken.race_router import router as chicken_race
from fast_granja.router.chicken.reason_router import router as chicken_death_reason


app = FastAPI()

app.include_router(user, tags=["User"], prefix="/user")
app.include_router(flock, tags=["Flock"], prefix="/flock")
app.include_router(eggs, tags=["Eggs"], prefix="/eggs")
app.include_router(chicken_death, tags=["Chicken Death"], prefix="/chicken_death")
app.include_router(chicken_race, tags=["Chicken Race"], prefix="/chicken_race")
app.include_router(
    chicken_death_reason, tags=["Chicken Death Reason"], prefix="/chicken_death_reason"
)


@app.get("/")
def root():
    return "Bem vindo a Fast Granja"
