import random
import time
import uuid
from datetime import datetime

import psycopg2
from dotenv import dotenv_values
from faker import Faker
from psycopg2 import sql
from tqdm import tqdm

fake = Faker(['en_US', 'pt_BR'])

config = dotenv_values(".env")

def create_conn()->psycopg2.connect:
    conn_str = config.get('PG_CONNECTION_STRING')
    return psycopg2.connect(conn_str)

def create_customers(number_of_customers:int)->None:
    connection = create_conn()

    with connection.cursor() as cursor:

        for _ in tqdm(range(number_of_customers)):
            customer_id = str(uuid.uuid4())
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone = fake.phone_number()
            address = fake.address()

            try:
                cursor.execute(
                    sql.SQL("INSERT INTO customers (customer_id, first_name, last_name, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s)"),
                    (customer_id, first_name, last_name, email, phone, address)
                )
            except:
                ...
        
        connection.commit()

    connection.close()

def create_accounts(number_of_accounts:int)->None:
    time.sleep(1)
    connection = create_conn()

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT customer_id FROM customers"))
        customer_ids = [row[0] for row in cursor.fetchall()]

        for _ in tqdm(range(number_of_accounts)):
            account_id = str(uuid.uuid4())
            customer_id = str(random.choice(customer_ids))
            account_number = fake.random_int(min=10000000, max=99999999)
            balance = round(random.uniform(100.0, 10000.0), 2)

            try:
                cursor.execute(
                    sql.SQL("INSERT INTO accounts (account_id, customer_id, account_number, balance) VALUES (%s, %s, %s, %s)"),
                    (account_id, customer_id, account_number, balance)
                )
            except:
                ...

        connection.commit()

    connection.close()

def create_transactions()->None:
    time.sleep(1)
    transaction_types = ['Sport'] * 3 + ['Travel'] * 9 + ['House'] * 7 + ['Food'] * 1 + ['Game'] * 10 + ['Invest'] * 1
    number_of_transactions_by_month = [random.randint(10, 100) for _ in range(12)]
    
    connection = create_conn()

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT account_id FROM accounts"))
        account_ids = [row[0] for row in cursor.fetchall()]
        last_year = datetime.now().year - 1
        
        for account_id in tqdm(account_ids):
            for month in tqdm(range(1, 13)):
                number_of_transactions = number_of_transactions_by_month[month-1]
                days_in_month = 30 if month in [4, 6, 9, 11] else 31
                if month == 2:
                    days_in_month = 28
                
                for _ in tqdm(range(number_of_transactions)):
                    transaction_timestamp = datetime(last_year, month, random.randint(1, days_in_month))

                    transaction_id = str(uuid.uuid4())
                    transaction_type = random.choice(transaction_types)
                    amount = round(random.uniform(-500.0, 500.0), 2)
                    description = fake.sentence()[:64]

                    cursor.execute(
                        sql.SQL("INSERT INTO transactions (transaction_id, account_id, transaction_type, amount, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)"),
                        (transaction_id, account_id, transaction_type, amount, description, transaction_timestamp)
                    )

            connection.commit()
    
    connection.close()

def main():
    create_customers(1)
    create_accounts(1)
    create_transactions()
if __name__ == '__main__':
    main()