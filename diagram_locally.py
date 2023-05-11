import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Connect to PostgreSQL
conn=psycopg2.connect(host="localhost",
                      database="postgres",
                      user=username,
                      password=password,
                      port=5432)

# SQL-query for importing data
sql_query_month = "SELECT count(id) cnt, date_trunc('MONTH', order_date) as mnth " \
                  "FROM public.orders " \
                  "GROUP BY date_trunc('MONTH', order_date) " \
                  "ORDER BY date_trunc('MONTH', order_date) asc"

sql_query_day = "SELECT count(id) cnt, date_trunc('DAY', order_date) as dy " \
                "FROM public.orders " \
                "GROUP BY date_trunc('DAY', order_date) " \
                "ORDER BY date_trunc('DAY', order_date) asc"

# Load data into DataFrame from Postgres
data_month = pd.read_sql(sql_query_month, conn)
data_day = pd.read_sql(sql_query_day, conn)

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Create diagram 1
axs[0].plot(data_month["mnth"], data_month["cnt"])
axs[0].set_xlabel("Month")
axs[0].set_ylabel("Orders")
axs[0].set_title("Orders by Months")

# Create diagram 2
axs[1].bar(data_day["dy"], data_day["cnt"])
axs[1].set_xlabel("Day")
axs[1].set_ylabel("Orders")
axs[1].set_title("Orders by Day")

# Show diagram
fig.tight_layout()
plt.show()