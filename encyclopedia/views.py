from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewEntryForm
from . import util

from . import util

import random, markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)  # calls get_entry from util.py
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page {title} does not exist"
        })
    else:
        content_html = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "content": content_html
        })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()

    if query in entries:
        return redirect('entry', title=query)
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        if not results:
            return render(request, "encyclopedia/error.html", {
                "message": "No search results found for your query."
            })
        else:
            return render(request, 'encyclopedia/search.html', {'results': results})

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                messages.error(request, "An entry with this title already exists.")
            else:
                util.save_entry(title, content)
                return redirect("entry", title=title)
    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/create.html", {
        "form": form
    })

def edit(request, title):
        if request.method == 'POST':
            form = NewEntryForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return redirect('entry', title=title)
            else:
                return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "edit": True,
                    "title": title
                })

        else:
            page_content = util.get_entry(title)
            form = NewEntryForm(initial={'content': page_content})
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "edit": True,
                "title": title
            })


def random_entry(request):
    entries = util.list_entries()
    random_title = random.choice(entries) 
    return redirect('entry', title=random_title)