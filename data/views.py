from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import pandas as pd
import sqlite3

from tracker.models import Topic, Entry
from tracker.forms import TopicForm, EntryForm
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
    entries = entries.head()
    entries = entries.to_html(index=False)
    context = {'entries': entries}
    return render(request, 'data/cgms_data.html', context)

@login_required
def cgms_save(request):
    uploads = load_filtered_test()
    uploads = uploads.reset_index(drop=True)
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            
            topic = Topic.objects.filter(text=new_topic)
            for index, row in uploads.iterrows():
                form = EntryForm(row)
                if form.is_valid():
                    new_entry = form.save(commit=False)
                    new_entry.topic = topic
                    new_entry.date_added = row['date_added']
                    print(new_entry.date_added)
                    new_entry.blood_sugar = row['blood_sugar']
                    print(new_entry.blood_sugar)
                    new_entry.save()

            return HttpResponseRedirect(reverse('tracker:topics'))

    uploads = uploads.head()
    uploads = uploads.to_html(index=False)

    context = {'uploads': uploads, 'form': form}
    return render(request, 'data/cgms_save.html', context)
