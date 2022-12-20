from sqlalchemy.orm import Session
from core.auth import check_token
from core.schemas.schema import Event
from core.models.database import EventTable


@check_token
def add_event(user: int, session: Session, event: Event):
    event.owner = user
    id = session.add(EventTable(**event.dict()))
    return {'status': 'OK', 'event_id': id}


def read_events(session: Session, *args, **kwargs):
    return session.query(EventTable).all()
