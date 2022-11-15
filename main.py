import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from auth import routers
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(routers.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
