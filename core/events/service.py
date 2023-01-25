from sqlalchemy.orm import Session
from core.auth import check_token
from core.schemas.schema import Event
from core.models.database import EventTable


@check_token
def add_event(user: int, session: Session, event: Event):
    event.owner = user
    if event.id:
        obj_for_update = session.query(EventTable).get(event.id)
        for key in event:
            setattr(obj_for_update, key[0], getattr(event, key[0]))
        id = session.add(obj_for_update)
    else:
        id = session.add(EventTable(**event.dict()))
    return {'status': 'OK', 'event_id': id}


def read_events(session: Session, *args, **kwargs):
    id = kwargs.get('id')
    if id:
        result = session.query(EventTable).get(id)
        if result:
            return [Event(**result.dict())]
        else:
            return []
    return [Event(**rec.dict()) for rec in session.query(EventTable).all()]


@check_token
def read_my_events(user: int, session: Session):
    return [Event(**rec.dict()) for rec in session.query(EventTable).filter(EventTable.owner == user).all()]

