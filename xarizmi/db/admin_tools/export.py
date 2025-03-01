import csv
from sqlalchemy import Engine
from sqlalchemy import text


def export_table_to_csv(table_name: str, output_file: str, engine: Engine) -> None:
    """
    Exports a PostgreSQL table to a CSV file using an existing SQLAlchemy
    engine.

    Args:
        table_name (str): Name of the table to export.
        output_file (str): Path to the output CSV file.
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine 
        connected to the database.
    """
    with engine.connect() as connection:
        # Query the table
        query = text(f'SELECT * FROM {table_name}')
        result = connection.execute(query)

        # Fetch column names (headers)
        headers = result.keys()

        # Export to CSV
        with open(output_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write headers
            writer.writerow(headers)

            # Write rows
            for row in result:
                writer.writerow(row)

    print(f'Table {table_name} has been exported to {output_file}')
