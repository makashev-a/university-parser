import psycopg2

FILE = 'universities.csv'
conn = psycopg2.connect("host= localhost dbname=aiogram user=akhmadi password=HaBuR394760")
print("Подключение к Базе данных")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS universities(
id integer PRIMARY KEY,
title varchar,
link varchar,
price varchar,
specialty integer
)
 """)

with open('universities.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'universities', sep=';', columns=('id', 'title', 'link', 'price', 'specialty'))
conn.commit()
print("Данные были успешно перенесены")
cur.close()
conn.close()
