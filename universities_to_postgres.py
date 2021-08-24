import psycopg2
import sqlalchemy
from sqlalchemy.exc import DBAPIError

FILE = 'universities.csv'
# conn = psycopg2.connect("host= localhost dbname=aiogram user=akhmadi password=HaBuR394760")
engine = sqlalchemy.create_engine('postgresql://akhmadi:HaBuR394760@localhost/aiogram')
conn = engine.raw_connection()
print("Подключение к Базе данных")
# cur = conn.cursor()
try:
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS universities(
        id integer PRIMARY KEY,
        title varchar,
        link varchar,
        price varchar,
        specialty integer,
        student_number varchar,
        foreign_number varchar,
        teacher_number varchar,
        year_of_foundation varchar,
        address varchar,
        email varchar
        )
         """)

        cur.execute("""CREATE TEMPORARY TABLE universities_staging ( LIKE universities )
        ON COMMIT DROP
        """)

        with open(FILE, 'r') as data:
            next(data)
            cur.copy_from(data, 'universities_staging', sep=';', columns=(
                'id', 'title', 'link', 'price', 'specialty', 'student_number', 'foreign_number', 'teacher_number',
                'year_of_foundation', 'address', 'email'))

        cur.execute("""INSERT INTO universities ( id, title, link, price, specialty, student_number, foreign_number, teacher_number, year_of_foundation, address, email)
                               SELECT id, title, link, price, specialty, student_number, foreign_number, teacher_number, year_of_foundation, address, email
                               FROM universities_staging
                               ON CONFLICT ( id )
                               DO UPDATE SET title = EXCLUDED.title
                                           , link = EXCLUDED.link
                                           , price = EXCLUDED.price
                                           , specialty = EXCLUDED.specialty
                                           , student_number = EXCLUDED.student_number
                                           , foreign_number = EXCLUDED.foreign_number
                                           , teacher_number = EXCLUDED.teacher_number
                                           , year_of_foundation = EXCLUDED.year_of_foundation
                                           , address = EXCLUDED.address
                                           , email = EXCLUDED.email""")

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
