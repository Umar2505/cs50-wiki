from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
import random

class Search(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'search'}), label="")

class Create(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'id': 'search'}),label='')
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text', 'cols': '30','rows':'5'}),label='')
    button = forms.CharField(widget=forms.TextInput(attrs={'type':'submit','value':'Submit', 'class': 'btn btn-dark', 'id':'button'}),label='')

class Change(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text', 'cols': '30','rows':'5'}),label='')
    button = forms.CharField(widget=forms.TextInput(attrs={'type':'submit','value':'Submit', 'class': 'btn btn-dark', 'id':'button'}),label='')


def make_it_upper(list):
    new_list = []
    for value in list:
        new_list.append(value.upper())
    return new_list

def it_has(list,search):
    new_list = []
    for values in list:
        if(search.upper() in values.upper()):
            new_list.append(values)
    return new_list

def index(request):
    lists = util.list_entries()
    rand = random.choice(lists)
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            value = form.cleaned_data['search']
            if value.upper() not in make_it_upper(util.list_entries()):
                list = it_has(util.list_entries(),value)
                return render(request, "encyclopedia/search.html", {
                    "entries": list,
                    "search": value,
                    "form": Search,
                    "value": rand
                })
            return HttpResponseRedirect(f"{value}")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search,
        "value": rand
    })
    

def get_page(request, title):
    lists = util.list_entries()
    rand = random.choice(lists)
    markdowner = Markdown()
    text =markdowner.convert(util.get_entry(str(title)))
    if request.method=='POST':
        form=Change(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title,text)
            text =markdowner.convert(util.get_entry(str(title)))
            if title.upper() in make_it_upper(util.list_entries()):
                return render(request, "encyclopedia/pages.html", {
                    "text": text,
                    "form": Search,
                    "formChange": form,
                    "value": rand
                })
            return HttpResponseRedirect('f{title}')
    else:
        form = Change(initial={'title':title,'text':util.get_entry(title)})

    return render(request, "encyclopedia/pages.html", {
        "text": text,
        "form": Search,
        "formChange": form,
        "value": rand
    })

def create_page(request):
    lists = util.list_entries()
    rand = random.choice(lists)
    isThere = False
    if request.method == 'POST':
        form = Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            if title.upper() in make_it_upper(util.list_entries()):
                isThere = True
                return render(request, "encyclopedia/create.html", {
                    "form_to_create": form,
                    "form": Search,
                    "class": isThere,
                    "value": rand
                })
            util.save_entry(title,text)
            return HttpResponseRedirect('/wiki')
    return render(request, "encyclopedia/create.html", {
        "form_to_create": Create,
        "form": Search,
        "value": rand
    })

