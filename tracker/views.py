from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import pandas as pd
import sqlite3

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from .cgms_import import load_saved_test, load_store_test, load_filtered_test, save_filtered_upload

@login_required
def index(request):
    """The home page for tracker"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'tracker/index.html', context)

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'tracker/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic, and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'tracker/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('tracker:topics'))

    context = {'form': form}
    return render(request, 'tracker/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new event for a particular topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('tracker:topic',
                                                args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'tracker/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing event."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Initial request; pre-fill form with the current event.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tracker:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'tracker/edit_entry.html', context)

@login_required
def upload(request):
    """The upload page for data"""
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        ds1 = pd.read_csv(csvfile)
        load_store_test(ds1)
        return HttpResponseRedirect(reverse('tracker:view'))
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
    return render(request, 'tracker/upload.html', context)

@login_required
def view(request):
    """import and compare two csv files """
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        ds1 = pd.read_csv(csvfile)
        ds1 = load_store_test(ds1)
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    else:
        ds1 = load_saved_test()
        ds1 = ds1.head()
        ds1 = ds1.to_html(index=False)
        context = {'ds1': ds1}
    return render(request, 'tracker/view.html', context)


@login_required
def cgms_save(request):
    uploads = load_saved_test()
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
                form = EntryForm(row['date_added'], row['blood_sugar'])
                # if form.is_valid():
                #     new_entry = form.save(commit=False)
                #     new_entry.topic = topic
                #     new_entry.date_added = row['date_added']
                #     print(new_entry.date_added)
                #     new_entry.blood_sugar = row['blood_sugar']
                #     print(new_entry.blood_sugar)
                #     new_entry.save()

            return HttpResponseRedirect(reverse('tracker:view'))

    uploads = uploads.head()
    uploads = uploads.to_html(index=False)

    context = {'uploads': uploads, 'form': form}
    return render(request, 'tracker/cgms_save.html', context)
