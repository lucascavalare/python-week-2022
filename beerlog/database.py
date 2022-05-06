import warnings


from sqlalchemy.exc import SAWarning
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlmodel import create_engine, Session
from beerlog.config import settings
from beerlog import models


warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


# Import settings from settings.toml
engine = create_engine(settings.database.url, echo=False)

# Generate SQL code Data Definition Language (select, update, etc)
models.SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
