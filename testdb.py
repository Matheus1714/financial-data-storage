import psycopg2

# Database connection parameters
db_params = {
    "host": "localhost",
    "port": 2222,         # The mapped port from the Docker run command
    "database": "finantialdb",
    "user": "postgres",   # Default PostgreSQL user created by the image
    "password": "postgres"
}

def main():
    # Establish a connection to the database
    connection = psycopg2.connect(**db_params)

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Execute a sample query
        cursor.execute("SELECT * FROM finantial_user")
        version = cursor.fetchone()

        # Print the PostgreSQL version
        print("PostgreSQL version:", version[0])

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()