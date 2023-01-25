from fastapi import HTTPException
from core.auth import check_token
from sqlalchemy.orm import Session
from core.models.database import EventTable
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from core.schemas.schema import Event, CreateEvent, UpdateEvent, DeleteEvent


map_tags = {
    'Спорт': 0,
    'Музыка': 1,
    'Учеба': 2,
    'Наука': 3,
    'Развлечения': 4,
    'Соревнования': 5,
    'Олимпиада': 6,
    'Программирование': 7,
    'Праздник': 8,
    'Культура и искусство': 9,
    'Творчество': 10,
    'Университетское': 11,
    'Мастеркласс': 12,
    'Cтажировка': 13,
    'Волонтер': 14,
    'Медиа': 15,
    'Туризм': 16,
    'Медицина': 17,
    'Кино': 18
}


@check_token
def add_event(user: int, session: Session, event: CreateEvent):
    event.owner = user
    stmt_create = insert(EventTable).values(event.dict()).returning(EventTable)
    stmt_select = select(EventTable).from_statement(stmt_create)
    id = session.execute(stmt_select).scalar().id
    return {'status': 'OK', 'event_id': id}


@check_token
def change_event(user: int, session: Session, event: UpdateEvent):
    event.owner = user
    if event.id:
        if session.query(EventTable).get(event.id):
            event_dict = event.dict()
            event_dict = {key: event_dict[key] for key in event_dict if event_dict[key]}
            stmt_update = update(EventTable).where(EventTable.id==event.id).values(event_dict).returning(EventTable)
            stmt_select = select(EventTable).from_statement(stmt_update)
            id = session.execute(stmt_select).scalar().id
            return {'status': 'OK', 'event_id': id}
        else:
            raise HTTPException(status_code=404, detail="Not found")
    else:
        raise HTTPException(status_code=404, detail="Not found")


@check_token
def delete_event(user: int, session: Session, event: DeleteEvent):
    if exist_event := session.query(EventTable).get(event.id):
        if exist_event.owner == user:
            session.execute(delete(EventTable).where(EventTable.id == event.id))
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {'status': 'OK', 'event_id': event.id}


def read_events(session: Session, *args, **kwargs):
    id = kwargs.get('id')
    if id:
        result = session.query(EventTable).get(id)
        if result:
            return [Event(**result.dict())]
        else:
            raise HTTPException(status_code=404, detail="Not found")
    return [Event(**rec.dict()) for rec in session.query(EventTable).all()]


@check_token
def read_my_events(user: int, session: Session):
    return [Event(**rec.dict()) for rec in session.query(EventTable).filter(EventTable.owner == user).all()]
