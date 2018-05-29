from django.contrib import admin

from tracker.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)