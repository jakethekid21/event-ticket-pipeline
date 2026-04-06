import csv
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            # place password to sql workbench here 
            password="",
            port=3306,
            database="ticket_system"
        )
    except Error as error:
        print("Error while connecting to database:", error)
    return connection


def load_third_party(connection, file_path_csv):
    cursor = connection.cursor()

    insert_sql = """
        INSERT INTO sales (
            ticket_id,
            trans_date,
            event_id,
            event_name,
            event_date,
            event_type,
            event_city,
            customer_id,
            price,
            num_tickets
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    rows_loaded = 0

    with open(file_path_csv, mode="r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)

        # Skip header row if the CSV has one
        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            cursor.execute(insert_sql, row)
            rows_loaded += 1

    connection.commit()
    cursor.close()

    print(f"Loaded {rows_loaded} rows into sales table.")


def query_popular_tickets(connection):
    cursor = connection.cursor()

    # If trans_date is stored like YYYYMMDD as an INT, convert it to a real date
    sql_statement = """
        SELECT
            event_name,
            SUM(num_tickets) AS total_tickets_sold
        FROM sales
        WHERE STR_TO_DATE(CAST(trans_date AS CHAR), '%Y%m%d') >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
        GROUP BY event_name
        ORDER BY total_tickets_sold DESC
        LIMIT 3
    """

    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()

    return records


def display_results(records):
    print("Here are the most popular tickets in the past month:")
    for record in records:
        event_name = record[0]
        print(f"- {event_name}")


def main():
    csv_file_path = "third_party_sales.csv"

    connection = get_db_connection()

    if connection is None:
        print("Failed to connect to database.")
        return

    try:
        load_third_party(connection, csv_file_path)
        records = query_popular_tickets(connection)
        display_results(records)
    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()