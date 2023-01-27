import json
import datetime
from fastapi import HTTPException
from core.auth import check_token
from sqlalchemy.orm import Session
from core.models.database import EventTable
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from core.schemas.schema import Event, CreateEvent, UpdateEvent, DeleteEvent, Set, UserEventTime, UserWithEvents,\
    AllUserEvent, FrontComment


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


def get_template(user: int = None):
    user_can_join = ''
    if user:
        user_can_join = f"""events.owner <> {user} and {user} not in (SELECT UNNEST(members)) and"""
    return f"""
        SELECT 
            id
        ,   title
        ,   description
        ,   date::text
        ,   count_people
        ,   start_time::text
        ,   address
        ,   icon_id
        ,   owner
        ,   tags
        ,   members
        ,   likes
        ,   dislikes
        ,   comments
        ,   (
                {user_can_join}
                (
                    array_length(members, 1) IS NULL 
                    OR count_people > array_length(members, 1)
                )
            ) as "can_join"
        FROM 
           events 
    """


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


def get_params(key: list):
    if len(key) == 2:
        param1, param2 = key
    else:
        param1, param2 = key[0], None
    return param1, param2


def read_events(session: Session, *args, **kwargs):
    id = kwargs.get('id')
    query = get_template()
    if id:
        query += f"""WHERE events."id" = {id}"""
        result = [Event(**rec._mapping) for rec in session.execute(query).all()]
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Not found")

    else:
        tags = kwargs.get('tags')
        title = kwargs.get('title')
        owner = kwargs.get('owner')
        start_time = kwargs.get('start_time')
        date = kwargs.get('date')
        count_people = kwargs.get('count_people')
        sort = kwargs.get('sort')
        filters = []

        if tags:
            filters.append(f"""
                events."tags" && ARRAY{tags}::smallint[]
            """)

        if title:
            filters.append(f"""
                events."title" ILIKE '%{title}%'
            """)

        if owner:
            filters.append(f"""
                events."owner" = ANY(ARRAY{owner}::int[])
            """)

        if start_time:
            start_from, start_to = get_params(start_time)

            if start_to:
                filters.append(f"""
                    events."start_time" >= '{str(start_from)}'::time and 
                    events."start_time" <= '{str(start_to)}'::time  
                """)
            else:
                filters.append(f"""
                    events."start_time" = '{str(start_from)}'::time  
                """)

        if date:
            date_from, date_to = get_params(date)

            if date_to:
                filters.append(f"""
                    events."date" >= '{str(date_from)}'::date and 
                    events."date" <= '{str(date_to)}'::date 
                """)
            else:
                filters.append(f"""
                    events."date" = '{str(date_from)}'::date
                """)

        if count_people:
            count_people_from, count_people_to = get_params(count_people)

            if count_people_to:
                filters.append(f"""
                    events."count_people" >= {count_people_from} and 
                    events."count_people" <= {count_people_to} 
                """)
            else:
                filters.append(f"""
                    events."count_people" = {count_people_from} 
                """)

        if filters:
            query += "WHERE "
            iterations = len(filters)
            for i in range(iterations):
                query += filters[i]
                if i != iterations - 1:
                    query += "and "

        if sort:
            sort = sort.split('|')
            if len(sort) == 2:
                column, order = sort
            else:
                column, order = sort[0], 'asc'
            query += f"ORDER BY {column} {order}"

    return [Event(**rec._mapping) for rec in session.execute(query).all()]


@check_token
def read_my_events(user: int, session: Session):
    return read_user_events(session, user)


def read_user(user: str, session: Session):
    if user.isdigit():
        user = session.execute(f"""
            SELECT 
                id, username, name, surname, last_name, sex, email  
            FROM users WHERE id = '{user}'
        """).all()
    else:
        user = session.execute(f"""
            SELECT 
                id, username, name, surname, last_name, sex, email 
            FROM users WHERE username = '{user}'
        """).all()
    if user:
        user = user[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")
    events = read_user_events(session, user.id)
    return UserWithEvents(events=events, **user._mapping)
    # return UserWithEvents(id=user.id, username=user.username, name=user.name, surname=user.surnevents=events, **)


def read_user_events(session: Session, user: int = None):
    date, time = str(datetime.datetime.now()).split(' ')
    query = get_template(user)
    query += f"""WHERE events."owner" = {user} or {user} = ANY(events."members")"""
    rs = session.execute(query).all()
    owner_future = []
    owner_past = []
    member_future = []
    member_past = []
    for rec in rs:
        if rec.owner == user:
            if rec.date > date:
                owner_future.append(Event(**rec._mapping))
            elif rec.date == date:
                if rec.start_time > time:
                    owner_future.append(Event(**rec._mapping))
                else:
                    owner_past.append(Event(**rec._mapping))
            else:
                owner_past.append(Event(**rec._mapping))
        else:
            if rec.date > date:
                member_future.append(Event(**rec._mapping))
            elif rec.date == date:
                if rec.start_time > time:
                    member_future.append(Event(**rec._mapping))
                else:
                    member_past.append(Event(**rec._mapping))
            else:
                member_past.append(Event(**rec._mapping))

    return AllUserEvent(
        owner=UserEventTime(future_event=owner_future, past_event=owner_past),
        member=UserEventTime(future_event=member_future, past_event=member_past)
    )


def read_sets(session: Session):
    rs = json.dumps([{'@Id': value, "name": key} for key, value in map_tags.items()], default=str)
    return [Set(**row._mapping) for row in session.execute(f"""
                WITH mat_data as (
                    SELECT
                        "@Id"
                    ,   "name"
                    ,   True as "event"
                    FROM 
                        jsonb_to_recordset('{rs}'::jsonb) as md(
                            "@Id" smallint
                        ,   "name" text
                        )
                    JOIN
                        events on md."@Id" = ANY(events.tags)
                )
                , event_count as (
                    SELECT
                        mat_data."@Id"
                    ,   COUNT(*) as "event_count"
                    FROM
                        mat_data
                    GROUP BY 
                        mat_data."@Id"
                )
                SELECT DISTINCT
                    event_count."@Id" as "id"
                ,   mat_data."name"
                ,   event_count."event_count"
                FROM
                    event_count
                JOIN
                    mat_data on event_count."@Id" = mat_data."@Id"
                ORDER BY 
                    event_count."event_count" desc
                ,   event_count."@Id" asc
            """).all()]


@check_token
def like_dislike_event(user: int, id: int, action: str, session: Session):
    session.execute(f"""
        UPDATE
            events
        SET
            "{action}" =  CASE 
                WHEN "{action}" IS NOT NULL THEN
                    "{action}" + 1  
                ELSE
                    1
            END 
        WHERE
            "id" = {id}
    """)
    return {'status': 'OK', 'id': id}


@check_token
def join_event(id: int, user: int, session: Session):
    result = session.execute(f"""
        WITH join_people AS (
            UPDATE
                events
            SET
                members = CASE
                    WHEN "members" IS NOT NULL THEN
                        array_append("members", {user})
                    ELSE
                        ARRAY[{user}]::int[]
                end
                    
            WHERE
                "id" = {id} AND
                (array_length("members", 1) IS NULL OR 
                "count_people" > array_length("members", 1))
            RETURNING
                events."id"
        )
        SELECT
            CASE
                WHEN EXISTS(SELECT "id" from join_people)
            THEN
                TRUE
            ELSE
                FALSE
            END
    """).one()
    if result:
        return {'status': 'OK', 'id': id}
    else:
        return {'status': 'ERROR', 'id': id}


@check_token
def write_comment(user: int, comment: FrontComment, session: Session):
    user = session.execute(f"""
        SELECT username FROM users WHERE id = '{user}'
    """).one()

    session.execute(f"""
        UPDATE
            events
        SET
            comments = CASE
                            WHEN comments is null then
                                ARRAY[ARRAY['{user.username}',  '{comment.comment}']]
                            ELSE
                                array_cat(comments,  ARRAY[ARRAY['{user.username}',  '{comment.comment}']])
                        END
        WHERE
            id = {comment.event_id}
    """)
    return {'status': 'OK', 'event_id': comment.event_id}
