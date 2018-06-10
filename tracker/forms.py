from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': 'Topic name'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['blood_sugar','carbs','insulin_type','insulin','text']
        labels = {'text': 'Notes'}
        widgets = {'blood_sugar': forms.NumberInput()}
        widgets = {'carbs': forms.NumberInput()}
        widgets = {'insulin': forms.NumberInput()}
        widgets = {'insulin_type': forms.Select()}
        widgets = {'text': forms.Textarea(attrs = {'rows': '3'})}
