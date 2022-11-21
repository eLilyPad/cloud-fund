# We'll need this to convert SQL responses into dictionaries
from psycopg2.extras import RealDictCursor
from psycopg2 import Error as psyError, DatabaseError, connect, sql


# def update_score(id, by):
#     """update the stories score based on the stories id"""
#     # TODO: add modified value
#     direction = "+" if by == "up" else "-"

#     sql = f"update stories set score = score {direction} 1 where id = {id}"
#     updated_rows = 0
#     conn = get_db_connection()

#     with conn.cursor() as cur:
#         try:
#             cur.execute(sql, id)
#             updated_rows = cur.rowcount
#             conn.commit()
#         except (Exception, DatabaseError) as error:
#             print(error)
#         # finally:
#         # if con:
#         # con.close()
#     return updated_rows


def send_title(title: str):
    query = sql.SQL(
        """--sql
            insert into news.stories (title) 
            values ({t}) 
            on conflict (title) 
            do nothing
        """
    ).format(t=sql.Literal(title))

    result = _insert(query)

    send_log(get_story_id(title), "title has been added to this story")

    return result


def send_tag(tag):
    query = sql.SQL(
        """--sql
            insert into news.tags (tag_name) 
            values ({t})
            on conflict (tag_name) 
            do nothing
        """
    ).format(t=sql.Literal(tag))

    return _insert(query)


def send_link(story_id: int, link: str):
    query = sql.SQL(
        """--sql
            insert into news.links (story_id, link) 
            values ({id}, {l}) 
            on conflict (link) 
            do nothing
        """
    ).format(id=sql.Literal(story_id), l=sql.Literal(link))

    log = send_log(story_id, "link has been added to this story")

    return _insert(query), log


def send_metadata(story_id, tag_id):
    query = sql.SQL(
        """--sql
            insert into news.metadata (story_id, tag_id) 
            values ({id}, {t_id})
        """
    ).format(id=sql.Literal(story_id), t_id=sql.Literal(tag_id))

    log = send_log(story_id, "metadata has been added to this story")

    return _insert(query), log


def send_log(story_id, description):
    query = sql.SQL(
        """--sql
            insert into news.logs (story_id, description)
            values ({id}, {d})
        """
    ).format(id=sql.Literal(story_id), d=sql.Literal(description))

    return _insert(query)


def get_stories():
    query = """--sql
        select story_id, title, link from news.stories
        join news.links 
        on stories.id on = news.links.story_id 
    """
    return _retrieve_dict(query)


def get_story_id(title):
    query = sql.SQL(
        """--sql
            select id from news.stories
            where title = {t}
        """
    ).format(t=sql.Literal(title))

    return _retrieve(query)[0][0]


def get_tag_id(tag):
    query = sql.SQL(
        """--sql
            select id from news.tags
            where tag_name = {t}
        """
    ).format(t=sql.Literal(tag))
    return _retrieve(query)[0][0]


def stories_by_tag(tag: str):
    query = sql.SQL(
        """--sql
            select story_id, title, link from news.stories
            join news.links
            on stories.id = news.links.story_id 
            where stories.id in ( 
                select story_id from news.metadata 
                where tag_id in (
                    select id from news.tags
                    where tag_name like '%u%'
                )
            )
        """
    ).format(t=sql.Literal(f"%{tag}%"))

    return _retrieve(query)


def stories_by_title(title: str):
    query = sql.SQL(
        """--sql
            select * from news.stories
            where title like {t}
        """
    ).format(t=sql.Literal(f"%{title}%"))

    return _retrieve(query)


def _insert(sql):
    rows = 0
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rows = cursor.rowcount
            connection.commit()
        except (Exception, DatabaseError) as error:
            print("something went wrong :(")
            print(error)
        finally:
            if cursor:
                cursor.close()
            return rows


def _retrieve(sql):
    data = []
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            connection.commit()
        except (Exception, psyError) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            # closing database cursor
            if cursor:
                cursor.close()
            return data


def _retrieve_dict(sql):
    data = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            connection.commit()
        except (Exception, psyError) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            # closing database cursor
            if cursor:
                cursor.close()
            return data


def _get_db_connection():
    try:
        conn = connect("dbname=social_news user=elizabeth host=localhost")
        return conn
    except:
        print("Error connecting to database.")


connection = _get_db_connection()
