import uvicorn
import routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
oauth2_scheme = routers.oauth2_scheme
app.include_router(routers.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
