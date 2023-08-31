from faker import Faker
import psycopg2
from psycopg2 import sql
import uuid
import random
from datetime import datetime

fake = Faker(['en_US', 'pt_BR'])

def create_conn()->psycopg2.connect:
    return psycopg2.connect(
        host = "localhost",
        port = 2222,
        database = "finantialdb",
        user = "postgres",
        password = "postgres"
    )

def create_customers(n:int)->None:
    connection = create_conn()

    with connection.cursor() as cursor:

        for _ in range(n):
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

def create_accounts(n:int)->None:
    connection = create_conn()

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT customer_id FROM customers"))
        customer_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(10):
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
    connection = create_conn()

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT account_id FROM accounts"))
        account_ids = [row[0] for row in cursor.fetchall()]

        transaction_types = transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Refund', 'Purchase', 'Fee', 'Interest', 'Conversion', 'Adjustment',
                    'Loan', 'Dividend', 'Investment', 'Charge', 'Withdrawal', 'Reversal', 'Credit', 'Debit', 'Exchange', 'Earned']
        
        for account_id in account_ids:
            for month in range(1, 13):
                days_in_month = 30 if month in [4, 6, 9, 11] else 31
                if month == 2:
                    days_in_month = 28
                
                for _ in range(days_in_month):

                    last_year = datetime.now().year - 1

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
    create_customers(10)
    create_accounts(10)
    create_transactions()
if __name__ == '__main__':
    main()