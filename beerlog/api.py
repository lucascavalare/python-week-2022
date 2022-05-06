from fastapi import FastAPI, Response, status  # ASGI

# Needs 'poetry add uvicorn'
# uvicorn beerlog.api:api
from beerlog.core import get_beers_from_database
from typing import List, Optional

# from beerlog.models import Beer
from beerlog.serializers import BeerOut, BeerIn
from beerlog.database import get_session
from beerlog.models import Beer

# Create and name API
api = FastAPI(title="beerlog")


# Decorator
@api.get("/beers", response_model=List[BeerOut])
# Async to distrubute processing
async def list_beers(style: Optional[str] = None):
    beers = get_beers_from_database(style)
    return beers


@api.post("/beers", response_model=BeerOut)
async def add_beer(beer_in: BeerIn, response: Response):
    beer = Beer(**beer_in.dict())
    with get_session() as session:
        session.add(beer)
        session.commit()
        session.refresh(beer)

    response.status_code = status.HTTP_201_CREATED
    return beer
