from fastapi import APIRouter

router = APIRouter()

@router.get("/population")
def population_get():
    pass