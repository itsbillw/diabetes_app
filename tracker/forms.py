from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['blood_sugar','carbs','text']
        labels = {'text': 'Notes'}
        widgets = {'blood_sugar': forms.NumberInput()}
        widgets = {'carbs': forms.NumberInput()}
        widgets = {'text': forms.Textarea()}
