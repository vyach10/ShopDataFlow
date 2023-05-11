import os
import random
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from faker import Faker

fake = Faker()

load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# подключение к БД
conn=psycopg2.connect(host="localhost",
                      database="postgres",
                      user=username,
                      password=password,
                      port=5432)

#cursor для выполнения SQL-запросов
cur = conn.cursor()

# создание таблицы orders
cur.execute("""
            CREATE TABLE IF NOT EXISTS public.orders (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(50),
                customer_email VARCHAR(50),
                product_name VARCHAR(50),
                product_price FLOAT,
                order_date DATE
            )
            """)

#генерирование случайных заказов
for i in range(1000):
    order_date = fake.date_between(start_date='-1y', end_date='today')
    customer_name = fake.name()
    customer_email = fake.email()
    product_name = fake.word().capitalize()
    product_price = round(random.uniform(10.0, 1000.0), 2)

    #вставка данных в таблицу orders
    insert_query = sql.SQL("INSERT INTO orders (customer_name, customer_email, product_name, product_price, order_date) VALUES ({}, {}, {}, {}, {})").format(
        sql.Literal(customer_name), sql.Literal(customer_email), sql.Literal(product_name), sql.Literal(product_price), sql.Literal(order_date))
    cur.execute(insert_query)

#подтверждение транзакции
conn.commit()

#закрытие подключения и cursor
cur.close()
conn.close()