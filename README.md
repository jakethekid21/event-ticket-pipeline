# event-ticket-pipeline

This project loads third-party ticket sales data from a CSV file into a MySQL database and displays the most popular tickets from the past month.

## Prerequisites

- Python 3
- MySQL Server
- MySQL Workbench
- A MySQL database named `ticket_system`
- A table named `sales`

## Setup

### 1. Install dependency

```bash
pip3 install -r requirements.txt
```

## UML Diagram

```mermaid
classDiagram
    class CSVFile {
        third_party_sales.csv
    }

    class MainPy {
        +get_db_connection()
        +load_third_party(connection, file_path_csv)
        +query_popular_tickets(connection)
        +display_results(records)
        +main()
    }

    class MySQLDatabase {
        ticket_system
    }

    class SalesTable {
        ticket_id : INT
        trans_date : INT
        event_id : INT
        event_name : VARCHAR(50)
        event_date : DATE
        event_type : VARCHAR(10)
        event_city : VARCHAR(20)
        customer_id : INT
        price : DECIMAL(10,2)
        num_tickets : INT
    }

    CSVFile --> MainPy
    MainPy --> MySQLDatabase
    MySQLDatabase --> SalesTable
    MainPy --> SalesTable
```
