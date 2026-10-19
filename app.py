from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

EVENTS: dict[int, str] = {}


class Note(BaseModel):
    note: str = Field(min_length=1, max_length=200)


@app.get("/events")
def list_events(limit: Optional[int] = Query(default=10, ge=1)):
    events = [{"id": event_id, "note": note} for event_id, note in sorted(EVENTS.items(), reverse=True)]
    return events[:limit]


@app.get("/events/{id}")
def read_event(id: int):
    if id not in EVENTS:
        raise HTTPException(status_code=404, detail="no such event")
    return {"id": id, "note": EVENTS[id]}


@app.post("/events", status_code=201)
def create_event(body: Note):
    new_id = max(EVENTS, default=0) + 1
    EVENTS[new_id] = body.note
    return {"id": new_id, "note": body.note}