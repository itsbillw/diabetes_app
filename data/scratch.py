import pandas as pd
import numpy as np

def cgms_upload():
    # ds1 = pd.DataFrame(np.random.randn(8, 4), index=pd.date_range('1/1/2000', periods=8), columns=['A', 'B', 'C', 'D'])
    ds1 = pd.read_csv("/home/bill/Downloads/CLARITY_Export test.csv")
    ds1 = ds1.loc[ds1['Event Type'].isin(['EGV'])]
    ds1 = ds1.rename(columns={"Timestamp (YYYY-MM-DDThh:mm:ss)": "date_added", "Glucose Value (mg/dL)":"blood_sugar", "Event Type":"EventType"})
    ds1 = ds1.loc[:, ['date_added', 'blood_sugar']]
    ds1['date_added'] = pd.to_datetime(ds1['date_added'], format='%Y-%m-%dT%H:%M:%S')
    ds1 = ds1.reset_index(drop=True)
    for index, row in ds1.iterrows():
        print(row['date_added'], row['blood_sugar'])
    return ds1

cgms_upload()