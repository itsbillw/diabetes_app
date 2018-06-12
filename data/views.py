from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import sqlite3

from data.cgms_import import load_saved_test, load_store_test, load_filtered_test, save_filtered_upload

@login_required
def index(request):
    """The home page for data"""
    if request.POST:
        ds1 = load_saved_test()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    else:
        ds1 = load_saved_test()
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    return render(request, 'data/index.html', context)

@login_required
def upload(request):
    """The upload page for data"""
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        ds1 = pd.read_csv(csvfile)
        ds1 = load_store_test(ds1)
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    elif request.POST:
        ds1 = save_filtered_upload()
        conn = sqlite3.connect("db.sqlite3")
        ds1 = pd.read_sql(sql="select * from cgms_table", con=conn)
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    elif request.GET:
        ds1 = load_saved_test()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    else:
        ds1 = load_saved_test()
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    return render(request, 'data/upload.html', context)

@login_required
def view(request):
    """import and compare two csv files """
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        ds1 = pd.read_csv(csvfile)
        ds1 = load_store_test(ds1)
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    else:
        ds1 = load_saved_test()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    return render(request, 'data/view.html', context)

@login_required
def cgms_data(request):
    conn = sqlite3.connect("db.sqlite3")
    entries = pd.read_sql(sql="select * from cgms_table", con=conn)
    entries = entries.drop(['Index','EventType'], axis=1)
    entries = entries.head()
    entries = entries.to_html(index=False)
    context = {'entries': entries}
    return render(request, 'data/cgms_data.html', context)