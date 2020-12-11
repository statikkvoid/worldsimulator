from fastapi import APIRouter

router = APIRouter()


@router.post("/events/{event_id}")
def event_start():
    pass


@router.post("/events/{event_id}")
def event_stop():
    pass