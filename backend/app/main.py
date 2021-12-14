from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router


#-----------------------------------------------------------------------------#
# api setup
#-----------------------------------------------------------------------------#
app = FastAPI()

# origin: null - "... your server must read the value of the request's Origin 
# header and use that value to set Access-Control-Allow-Origin"
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin
origins = [
    "http://localhost:5000", # js serve uses port 5000 as default
    "http://localhost:3000", # react-scripts npm start uses port 3000 as default
    "null", # use null if running client app through a static html file, i.e. no server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"], # could also be '*'
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}
