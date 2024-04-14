from sqlmodel import Session , create_engine
from db import engine
from typing import Generator

        
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        