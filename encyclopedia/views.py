from django.shortcuts import render, redirect
import re
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    content = util.get_entry(title)
    if content:
        re_html_content = util.convert_markdown_to_html(content)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "title_content": re_html_content
        })
    return render(request, "encyclopedia/page_not_found.html", {
        "title": title
    })

def search(request):
    query = request.GET.get('q', '').strip().lower()
    content = util.get_entry(query)
    if content:
        return title(request, query)

    results_list = [entry for entry in util.list_entries() if query in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results_list": results_list
    })

def random_page(request):
    random_entry = random.choice(util.list_entries())
    return redirect('wiki:title', title=random_entry)

def create_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Проверка, существует ли страница с таким заголовком
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/create.html", {
                "error": "A page with this title already exists.",
                "title": title,
                "content": content
            })

        # Сохраняем новую страницу
        util.save_entry(title, content)
        return redirect('wiki:title', title=title)

    return render(request, "encyclopedia/create.html")


def edit_page(request, title):
    new_title = title
    if request.method == "POST":
        new_title = request.POST.get('new_title')
        content = request.POST.get('content')
        content = re.sub(r'\n{2,}', '\n', content.replace('\r\n', '\n').replace('\r', '\n'))
        util.save_entry(new_title, content)
        return redirect('wiki:title', title=new_title)

    content = util.get_entry(new_title)
    content = re.sub(r'\n{2,}', '\n', content)

    return render(request, "encyclopedia/edit.html", {
        "title": new_title,
        "content": content
    })

def delete_page(request, title):
    if request.method == "POST":
        util.delete_entry(title)
        return redirect('wiki:index')

    return render(request, "encyclopedia/delete.html", {
        "title": title
    })