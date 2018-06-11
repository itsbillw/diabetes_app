import pandas as pd
import numpy as np
import sqlite3

def load_saved_test():
    conn = sqlite3.connect("db.sqlite3")
    try:
        ds1 = pd.read_sql(sql="select * from temp_table", con=conn)
    except:
        ds1 = pd.DataFrame(np.random.randn(8, 4), index=pd.date_range('1/1/2000', periods=8), columns=['A', 'B', 'C', 'D'])
    return ds1

def load_store_test(ds1):
    conn = sqlite3.connect("db.sqlite3")
    ds1.to_sql(name='temp_table', con=conn, index=False, if_exists='replace')
    return ds1

def load_filtered_test():
    ds1 = load_saved_test()
    ds1 = ds1.loc[ds1['Event Type'].isin(['EGV'])]
    ds1 = ds1.rename(columns={"Timestamp (YYYY-MM-DDThh:mm:ss)": "Timestamp", "Glucose Value (mg/dL)":"GlucoseValue", "Event Type":"EventType"})
    ds1 = ds1.loc[:, ['Index','Timestamp', 'GlucoseValue','EventType']]
    ds1['Timestamp'] = pd.to_datetime(ds1['Timestamp'], format='%Y-%m-%dT%H:%M:%S')
    return ds1

def save_filtered_upload():
    ds1 = load_filtered_test()
    conn = sqlite3.connect("db.sqlite3")
    ds1.to_sql(name='cgms_table', con=conn, index=False, if_exists='replace')
    return ds1

