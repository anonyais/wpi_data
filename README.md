# WPI Data Processing Script

This Python script automates the process of downloading, extracting, and loading data from an Access database (MDB file) into a PostgreSQL database. The script includes functionality for both Windows and Unix-like systems.

## Prerequisites

Before using the script, ensure you have the following dependencies installed:

- Python (3.6+)
- pandas
- requests
- sqlalchemy
- pyodbc
- mdb_parser (You may need to install this package separately)

You can install these packages using the following command:

```bash
pip install -r requirements.txt
```


## Usage

1. Clone this repository or download the script directly.

2. Modify the PostgreSQL database connection details in the script. Replace `postgres`, `001986`, `localhost`, and `5432` with your appropriate database credentials.

3. Update the Google Drive file ID (`file_id`) in the script with the desired MDB file's Google Drive ID.

4. Run the script using the following command:

```bash
python script_name.py
```


## Script Overview

The script defines functions to perform the following tasks:

- Download an MDB file from Google Drive.
- Unzip the downloaded file.
- Read data from the MDB file and load it into a PostgreSQL database.

The `run_upload()` function checks the operating system and selects the appropriate function to read and load the data, based on whether the system is Windows or Unix-like.

## Running the Script

1. The script first downloads the MDB file from Google Drive using the provided file ID.

2. The downloaded file is then unzipped to the current working directory.

3. Depending on the operating system, the script either uses the `mdb_parser` library to read and load data on Unix-like systems or uses `pyodbc` to read and load data on Windows systems.

4. The data from the MDB file is read into pandas DataFrames and then loaded into the PostgreSQL database using SQLAlchemy's `create_engine` and pandas' `to_sql` method.

## Note

- Ensure that you replace placeholder values in the script (such as database credentials and file paths) with your actual values.

- The script appends data to the PostgreSQL tables if they already exist. Modify the `if_exists` parameter in the `to_sql` method as needed.

- If you encounter any issues or errors while using the script, feel free to seek assistance.






