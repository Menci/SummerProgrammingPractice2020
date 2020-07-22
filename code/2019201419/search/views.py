from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

import datetime

from .search import do_search


def index(request):
    return render(request, 'search/index.html', {
        'server_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


def search(request):
    query_str = request.GET['query']
    if query_str == '':
        return redirect('index')
    return render(request, 'search/result.html', {
        'server_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'query_text': query_str,
        'search_results': do_search(query_str)
    })


def auto_search(request):
    query_str = request.GET['query']
    res_str = ''
    for url in do_search(query_str, True):
        res_str += url + '\n'
    return HttpResponse(res_str)
