from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import sqlite3
import pandas as pd

@login_required
def index(request):
    """The home page for data"""
    return render(request, 'data/index.html')

@login_required
def upload(request):
    """The home page for data"""
    return render(request, 'data/upload.html')

@login_required
def view(request):
    """import and compare two csv files """
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        ds1 = pd.read_csv(csvfile)
        conn = sqlite3.connect("db.sqlite3")
        ds1.to_sql(name='test_table', con=conn, index=False, if_exists='replace')
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    else:
        conn = sqlite3.connect("db.sqlite3")
        ds1 = pd.read_sql(sql="select * from test_table", con=conn)
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}

    return render(request, 'data/view.html', context)