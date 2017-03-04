from django.shortcuts import render
from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch
import math


ROWS_PER_PAGE = 20

def home(request):
    return render_to_response('index.html')

def search(request):
    page_info = {'current': page, 'total': 0,
                 'total_rows': 0, 'rows': []}
    query = request.GET.get('query')
    start = request.GET.get('start')
    if not start:
        start = 0
    es=Elasticsearch()
    res = es.search(
        index='databases',
        body={
            "from" : start, "size" : ROWS_PER_PAGE,
            'query' :{
                'query_string' :{
                    'query' : query,
                }
            },
            'highlight':{
                'fields':{
                    'ip':{}
                }
            }
        }
    )
    page_info['total_rows'] = res['hits']['total']
    page_info['total'] = int(math.ceil(page_info['total_rows'] / (ROWS_PER_PAGE * 1.0)))
    for source in res['hits']['hits']:
        result = source['_source']
        page_info['rows'].append(c)
    return render_to_response('result.html',{'query':query,'result':page_info})
