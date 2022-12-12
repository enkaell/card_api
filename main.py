from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import routers

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(routers.router)

