import psycopg2
import sqlalchemy
from sqlalchemy.exc import DBAPIError

FILE = 'specialties.csv'
# conn = psycopg2.connect("host= localhost dbname=aiogram user=akhmadi password=HaBuR394760")
engine = sqlalchemy.create_engine('postgresql://akhmadi:HaBuR394760@localhost/aiogram')
conn = engine.raw_connection()
print("Подключение к Базе данных")
# cur = conn.cursor()
try:
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS specialties(
        id serial PRIMARY KEY,
        code varchar not null,
        name varchar not null,
        category integer not null,
        university_id integer not null references universities (id)
        )
         """)

        cur.execute("""CREATE TEMPORARY TABLE specialties_staging ( LIKE specialties )
        ON COMMIT DROP
        """)

        with open(FILE, 'r', encoding='utf-8-sig') as data:
            next(data)
            cur.copy_from(data, 'specialties_staging', sep=';', columns=(
                'id', 'code', 'name', 'category', 'university_id'))

        cur.execute("""INSERT INTO specialties ( id, code, name, category, university_id )
                               SELECT id, code, name, category, university_id
                               FROM specialties_staging
                               ON CONFLICT ( id )
                               DO UPDATE SET code = EXCLUDED.code
                                           , name = EXCLUDED.name
                                           , category = EXCLUDED.category
                                           , university_id = EXCLUDED.university_id""")

except:
    conn.rollback()
    raise

else:
    conn.commit()
    print("Данные были успешно перенесены")

finally:
    conn.close()
    print("Закрываем подключение")

# with open(FILE, 'r') as f:
# next(f)
# cur.copy_from(f, 'universities', sep=';', columns=('id', 'title', 'link', 'price', 'specialty'))

# conn.commit()
# cur.close()
# conn.close()
