import mysql.connector
from mysql.connector import Error
import pandas as pd
class EPLTableData:
    """
        host:
        user:
        password:
        database: plmc
    """
    def __init__(self, host, user, password, database, port):
        
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database, 
                port=port
            )
            self.cursor = self.connection.cursor()
            print('Database connection established.')
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def create_table_for_season(self, season: str):
        # Sanitize table name: Replace invalid characters
        table_name = f"{season}_{season+1}"  # Replace hyphens with underscores

        # Define the table schema
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Team VARCHAR(255),
            Date DATE,
            Time TIME,
            Round VARCHAR(255),
            Day VARCHAR(255),
            Venue VARCHAR(255),
            Result VARCHAR(255),
            GF INT,
            GA INT,
            Opponent VARCHAR(255),
            xG FLOAT,
            xGA FLOAT,
            Possession FLOAT,
            Attendance VARCHAR(255),
            Captain VARCHAR(255),
            Formation VARCHAR(255),
            Opp_Formation VARCHAR(255),
            Referee VARCHAR(255),
            Match_Report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print(f"Table '{table_name}' is ready.")
 

    def insert_dataframe(self, dataframe: pd.DataFrame):
        """
        Insert all rows from the DataFrame into the corresponding season table.

        Args:
            season (str): The season name.
            dataframe (pd.DataFrame): The data to be stored.
        """
        dataframe = dataframe.fillna(0)
        season = int(dataframe['Date'][0][:4])
        table_name = f"{season}_{season+1}"  # Ensure valid table name

        # Create the table if it doesn't exist
        self.create_table_for_season(season)

        # Prepare data for insertion
        placeholders = ", ".join(["%s"] * len(dataframe.columns))
        columns = ", ".join([f"`{col.replace(' ', '_')}`" for col in dataframe.columns])

        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        data = [tuple(row) for row in dataframe.values]

        # Insert the data
        self.cursor.executemany(insert_query, data)
        self.connection.commit()
        print(f"Inserted {len(data)} rows into '{table_name}'.")

    def fetch_data(self, season: str):
        """
        Fetch all data from the table for the given season.

        Args:
            season (str): The season name.
        """
        # table_name = f"{season}_{season+1}"  # Ensure valid table name
        # fetch_query = f"SELECT * FROM {table_name}"
        # self.cursor.execute(fetch_query)
        # rows = self.cursor.fetchall()
        # return rows
        # table_name = f'{season}_{season+1}'
        query = f'select * from {season}'
        df = pd.read_sql(query, con=self.connection)
        return df

    def table_exists(self, table_name: str):
        query = f"SHOW TABLES LIKE '{table_name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None


    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
