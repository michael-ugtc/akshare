import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from arcticdb import Arctic

NUM_COLUMNS=10
NUM_ROWS=100_000
df = pd.DataFrame(np.random.randint(0,100,size=(NUM_ROWS, NUM_COLUMNS)), columns=[f"COL_{i}" for i in range(NUM_COLUMNS)], index=pd.date_range('1678', periods=NUM_ROWS, freq='h'))

ac = Arctic('lmdb:///ArcticDBStore')
lib=ac.get_library('AStock')
lib.write("my_data", df)
dd = lib.read("my_data")

np.set_printoptions(threshold=np.inf)
print(dd.data)


def read_data(path):
    # Use read_csv function to read data, convert datetime string to datetime type, and set it as the index of DataFrame
    df = pd.read_csv(path, parse_dates=['datetime'], index_col='datetime', engine = "pyarrow")
    # Convert column names to start with an uppercase letter
    df = df.rename(columns=lambda x: x.capitalize())
    df = df[['Open', 'High', 'Low', 'Close', 'Amount']]

    # Extract filename as stock ID
    base = os.path.basename(path)
    stock_id = os.path.splitext(base)[0]  # Remove file extension to get stock ID

    # Add the stock ID to the DataFrame
    df["id"] = stock_id

    return df, stock_id

def process_file(file_path, library):
    df, stock_id = read_data(file_path)
    try:
        # Try to update
        library.update(stock_id, df)
        print(f"Successfully updated {stock_id}")
    except:
        # If update fails, try to write
        print(f"Failed to update, trying to write {stock_id}")
        library.write(stock_id, df)

def process_directory(directory_path, library):
    # Get all files in the directory
    files = os.listdir(directory_path)
    csv_files = [f for f in files if f.endswith('.csv')]

    # Use tqdm to create a progress bar
    for csv_file in tqdm(csv_files):
        # Call process_file function for each file
        process_file(os.path.join(directory_path, csv_file), library)

# Process all directories within a specified range of years
#start_year = 2005
#end_year = 2020
#for year in range(start_year, end_year + 1):
#    directory_path = os.path.join(r"C:\ArcticDBStore", str(year))
 #   if(~os.path.isfile(directory_path)):
 #       os.mkdir(directory_path);    
#    process_directory(directory_path, aStock)