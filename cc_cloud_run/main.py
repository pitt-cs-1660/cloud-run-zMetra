from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # stream all votes; count tabs / spaces votes, and get recent votes
    votes = votes_collection.stream()
    tabs = 0
    spaces = 0
    vote_data = []
    for v in votes:
        vote_data.append(v.to_dict())
    for v in vote_data:
        if v["team"] == "TABS":
            tabs += 1
        elif v["team"] == "SPACES":
            spaces +=1
    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs,
        "spaces_count": spaces,
        "recent_votes": []
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    votes_collection.add({
    "team": team,
    "time_cast": datetime.datetime.utcnow().isoformat()
    })
    

    # create a new vote document in firestore
    return {"detail": "New Vote!"}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
