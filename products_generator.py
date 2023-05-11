import random
import string
from psycopg2 import sql
import os

from faker import Faker
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Подключение к БД
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user=username,
    password=password)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Удаление всех данных из таблицы products
cur.execute("DELETE FROM products")

# Создание 100 случайных записей в таблице products
fake = Faker()

for i in range(100):
    name = fake.name()
    price = round(random.uniform(10, 1000), 2)
    description = fake.text()
    image_url = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.jpg'
    cur.execute("INSERT INTO products (name, price, description, image_url) VALUES (%s, %s, %s, %s)", (name, price, description, image_url))

# Подтверждение транзакции
conn.commit()

# Закрытие курсора и подключения к базе данных
cur.close()
conn.close()