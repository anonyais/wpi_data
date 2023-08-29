import pandas as pd
import requests
from sqlalchemy import create_engine
import zipfile
import subprocess
from io import StringIO
from mdb_parser import MDBParser
import platform
import pyodbc



engine = create_engine('postgresql://postgres:001986@localhost:5432/wpi_data')

def download_covid_data(file_id, ):
    file_url = f'https://drive.google.com/uc?id={file_id}'
    output_path = 'WPI.zip'
    
    response = requests.get(file_url)

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file to '{output_path}'")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
    
    return output_path

def unzip_download(file_name):
    zip_file_path = file_name

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all contents to the current working directory
        zip_ref.extractall()
        print(f"{file_name} successfully unzipped")


def read_accessdb_and_load_unix():
    db = MDBParser(file_path="WPI.mdb")

    mdb_file = "WPI.mdb"

    # Replace with the path to your MDB file and the table name
    #table_name = "Country Codes"

    table_names = db.tables

    for table_name in table_names:

        # Construct the mdb-export command
        command = ["mdb-export", mdb_file, table_name]

        # Run the command and capture the output
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=False)
            decoded_output = output.decode("utf-8")

            # Convert the output into a pandas DataFrame
            # Assuming your output is CSV-like
            df = pd.read_csv(StringIO(decoded_output))
            print()
            print(f"table_name: {table_name}")
            print(df)
        except subprocess.CalledProcessError as e:
            print("Error:", e.output.decode("utf-8"))

def read_accessdb_and_load_win():
    # Replace 'YourMDBFile.mdb' with the path to your MDB file
    mdb_file = r'C:\Users\sanon\OneDrive\Desktop\sunny_capstone\WPI.mdb'

    # Define a connection string
    conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={mdb_file};"

    try:
        # Connect to the database
        connection = pyodbc.connect(conn_str)

        cursor = connection.cursor()

            # Construct a SQL query to select all user-defined table names
        table_names = []
        for i in cursor.tables(tableType='Table'):
            table_names.append(i[2])
            # print(i[2])

        # print(table_names)

        for table_name in table_names:
            # Construct a SQL query to select all rows from the table
            query = f"SELECT * FROM [{table_name}]"

            # Use pandas to read the query result directly into a DataFrame
            df = pd.read_sql(query, connection)
            df.to_sql(table_name,engine,if_exists='append', index=False)
            # Print the DataFrame with column names
            # print(df)

    except Exception as e:
        pass

def run_upload():
    if platform.system() == 'Windows':
        read_accessdb_and_load_win()
    else:
        read_accessdb_and_load_unix()




if __name__ == "__main__":
    file_id = '1VyCGCAfFuEK7vB1C9Vq8iPdgBdu-LDM4'
    file_name = download_covid_data(file_id)
    output = unzip_download(file_name)
    run_upload()