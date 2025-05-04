# main.py
# this is what luke's been using to test the frontend. feel free to use for whatever it's worth

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any, Tuple
from datetime import date, datetime
from enum import Enum

app = FastAPI(title="STEM Summer Camp Registration API", version="1.0.0")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # for development; lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class Family(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CampSession(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    capacity: int
    created_at: datetime
    updated_at: datetime

class Gender(str, Enum):
    M = 'M'
    F = 'F'
    Other = 'Other'

class Camper(BaseModel):
    id: int
    family_id: int
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    created_at: datetime
    updated_at: datetime

class RegistrationStatus(str, Enum):
    registered = 'registered'
    waitlisted = 'waitlisted'

class Registration(BaseModel):
    id: int
    camper_id: int
    session_id: int
    status: RegistrationStatus
    waitlist_position: Optional[int] = None
    registered_at: datetime
    updated_at: datetime

class NotificationType(str, Enum):
    confirmation = 'confirmation'
    waitlist = 'waitlist'
    availability = 'availability'

class Notification(BaseModel):
    id: int
    registration_id: int
    type: NotificationType
    canvas_message_id: Optional[str] = None
    sent_at: datetime

# --- In-memory “database” with expanded mock data ---
families: List[Family] = [
    Family(id=1, name="Smith", email="smith@example.com", phone="555-1234",
           created_at=datetime.now(), updated_at=datetime.now()),
    Family(id=2, name="Johnson", email="johnson@example.com", phone="555-5678",
           created_at=datetime.now(), updated_at=datetime.now()),
    Family(id=3, name="Williams", email="williams@example.com", phone=None,
           created_at=datetime.now(), updated_at=datetime.now()),
]

camp_sessions: List[CampSession] = [
    CampSession(id=1, name="Robotics 101", start_date=date(2025,6,1), end_date=date(2025,6,5),
                capacity=20, created_at=datetime.now(), updated_at=datetime.now()),
    CampSession(id=2, name="Chemistry Lab", start_date=date(2025,6,10), end_date=date(2025,6,14),
                capacity=15, created_at=datetime.now(), updated_at=datetime.now()),
    CampSession(id=3, name="Astronomy Adventures", start_date=date(2025,7,1), end_date=date(2025,7,5),
                capacity=25, created_at=datetime.now(), updated_at=datetime.now()),
]

campers: List[Camper] = [
    Camper(id=1, family_id=1, first_name="Alice", last_name="Smith",
           dob=date(2012,5,17), gender=Gender.F,
           created_at=datetime.now(), updated_at=datetime.now()),
    Camper(id=2, family_id=2, first_name="Bob", last_name="Johnson",
           dob=date(2011,8,30), gender=Gender.M,
           created_at=datetime.now(), updated_at=datetime.now()),
    Camper(id=3, family_id=1, first_name="Charlie", last_name="Smith",
           dob=date(2013,2,20), gender=Gender.Other,
           created_at=datetime.now(), updated_at=datetime.now()),
    Camper(id=4, family_id=3, first_name="Diana", last_name="Williams",
           dob=date(2010,11,5), gender=Gender.F,
           created_at=datetime.now(), updated_at=datetime.now()),
]

registrations: List[Registration] = [
    Registration(id=1, camper_id=1, session_id=1, status=RegistrationStatus.registered,
                 waitlist_position=None, registered_at=datetime.now(), updated_at=datetime.now()),
    Registration(id=2, camper_id=2, session_id=1, status=RegistrationStatus.waitlisted,
                 waitlist_position=1, registered_at=datetime.now(), updated_at=datetime.now()),
    Registration(id=3, camper_id=3, session_id=2, status=RegistrationStatus.registered,
                 waitlist_position=None, registered_at=datetime.now(), updated_at=datetime.now()),
    Registration(id=4, camper_id=4, session_id=3, status=RegistrationStatus.registered,
                 waitlist_position=None, registered_at=datetime.now(), updated_at=datetime.now()),
]

notifications: List[Notification] = [
    Notification(id=1, registration_id=1, type=NotificationType.confirmation,
                 canvas_message_id="msg-abc123", sent_at=datetime.now()),
    Notification(id=2, registration_id=2, type=NotificationType.waitlist,
                 canvas_message_id=None, sent_at=datetime.now()),
    Notification(id=3, registration_id=3, type=NotificationType.confirmation,
                 canvas_message_id="msg-def456", sent_at=datetime.now()),
    Notification(id=4, registration_id=4, type=NotificationType.availability,
                 canvas_message_id="msg-ghi789", sent_at=datetime.now()),
]

# --- Utility functions ---
def apply_search(items: List[BaseModel], search: Optional[str]) -> List[BaseModel]:
    if not search:
        return items
    s = search.lower()
    filtered = []
    for item in items:
        for v in item.dict().values():
            if v is not None and s in str(v).lower():
                filtered.append(item)
                break
    return filtered

def apply_sort(items: List[BaseModel], sort_by: Optional[str]) -> List[BaseModel]:
    if not sort_by:
        return items
    keys = sort_by.split(',')
    def sort_key(item: BaseModel) -> Tuple[Any, ...]:
        return tuple(getattr(item, k, None) for k in keys)
    return sorted(items, key=sort_key)

def paginate(items: List[BaseModel], page: int, limit: int) -> Tuple[List[BaseModel], int]:
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    return items[start:end], total

def make_list_endpoint(data_src: List[BaseModel]):
    def list_fn(
            page: int = Query(1, ge=1),
            limit: int = Query(10, ge=1),
            search: Optional[str] = None,
            sortBy: Optional[str] = None
    ):
        filtered = apply_search(data_src, search)
        sorted_list = apply_sort(filtered, sortBy)
        page_items, total = paginate(sorted_list, page, limit)
        return {"items": page_items, "total": total}
    return list_fn

# --- Families Endpoints ---
@app.get("/families")
def list_families(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = None,
        sortBy: Optional[str] = None
):
    return make_list_endpoint(families)(page, limit, search, sortBy)

@app.post("/families", response_model=Family, status_code=201)
def create_family(f: Family):
    families.append(f)
    return f

@app.get("/families/{id}", response_model=Family)
def get_family(id: int):
    for f in families:
        if f.id == id:
            return f
    raise HTTPException(404, "Family not found")

@app.put("/families/{id}", response_model=Family)
def update_family(id: int, f: Family):
    for idx, existing in enumerate(families):
        if existing.id == id:
            families[idx] = f
            return f
    raise HTTPException(404, "Family not found")

@app.delete("/families/{id}", status_code=204)
def delete_family(id: int):
    global families
    families = [f for f in families if f.id != id]

# --- Camp Sessions Endpoints ---
@app.get("/camp-sessions")
def list_sessions(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = None,
        sortBy: Optional[str] = None
):
    return make_list_endpoint(camp_sessions)(page, limit, search, sortBy)

@app.post("/camp-sessions", response_model=CampSession, status_code=201)
def create_session(s: CampSession):
    camp_sessions.append(s)
    return s

@app.get("/camp-sessions/{id}", response_model=CampSession)
def get_session(id: int):
    for s in camp_sessions:
        if s.id == id:
            return s
    raise HTTPException(404, "Session not found")

@app.put("/camp-sessions/{id}", response_model=CampSession)
def update_session(id: int, s: CampSession):
    for idx, existing in enumerate(camp_sessions):
        if existing.id == id:
            camp_sessions[idx] = s
            return s
    raise HTTPException(404, "Session not found")

@app.delete("/camp-sessions/{id}", status_code=204)
def delete_session(id: int):
    global camp_sessions
    camp_sessions = [s for s in camp_sessions if s.id != id]

# --- Campers Endpoints ---
@app.get("/campers")
def list_campers(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = None,
        sortBy: Optional[str] = None
):
    return make_list_endpoint(campers)(page, limit, search, sortBy)

@app.post("/campers", response_model=Camper, status_code=201)
def create_camper(c: Camper):
    campers.append(c)
    return c

@app.get("/campers/{id}", response_model=Camper)
def get_camper(id: int):
    for c in campers:
        if c.id == id:
            return c
    raise HTTPException(404, "Camper not found")

@app.put("/campers/{id}", response_model=Camper)
def update_camper(id: int, c: Camper):
    for idx, existing in enumerate(campers):
        if existing.id == id:
            campers[idx] = c
            return c
    raise HTTPException(404, "Camper not found")

@app.delete("/campers/{id}", status_code=204)
def delete_camper(id: int):
    global campers
    campers = [c for c in campers if c.id != id]

# --- Registrations Endpoints ---
@app.get("/registrations")
def list_registrations(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = None,
        sortBy: Optional[str] = None
):
    return make_list_endpoint(registrations)(page, limit, search, sortBy)

@app.post("/registrations", response_model=Registration, status_code=201)
def create_registration(r: Registration):
    registrations.append(r)
    return r

@app.get("/registrations/{id}", response_model=Registration)
def get_registration(id: int):
    for r in registrations:
        if r.id == id:
            return r
    raise HTTPException(404, "Registration not found")

@app.put("/registrations/{id}", response_model=Registration)
def update_registration(id: int, r: Registration):
    for idx, existing in enumerate(registrations):
        if existing.id == id:
            registrations[idx] = r
            return r
    raise HTTPException(404, "Registration not found")

@app.delete("/registrations/{id}", status_code=204)
def delete_registration(id: int):
    global registrations
    registrations = [r for r in registrations if r.id != id]

# --- Notifications Endpoints ---
@app.get("/notifications")
def list_notifications(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = None,
        sortBy: Optional[str] = None
):
    return make_list_endpoint(notifications)(page, limit, search, sortBy)

@app.post("/notifications", response_model=Notification, status_code=201)
def create_notification(n: Notification):
    notifications.append(n)
    return n

@app.get("/notifications/{id}", response_model=Notification)
def get_notification(id: int):
    for n in notifications:
        if n.id == id:
            return n
    raise HTTPException(404, "Notification not found")

@app.delete("/notifications/{id}", status_code=204)
def delete_notification(id: int):
    global notifications
    notifications = [n for n in notifications if n.id != id]

# To run:
# pip install fastapi uvicorn pydantic
# uvicorn main:app --reload --port 5000
