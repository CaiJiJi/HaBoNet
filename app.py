import math
import re
import time
import urllib2
from flask import Flask, request, render_template
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
ROWS_PER_PAGE = 20

def search_mongodb_by_es(keywords, page):
    from elasticsearch import Elasticsearch

    page_info = {'current': page, 'total': 0,
                 'total_rows': 0, 'rows': []}
    # get the page rows
    if page >= 1 :
        row_start = (page - 1) * ROWS_PER_PAGE
        es = Elasticsearch()
        res = es.search(
        index='databases',
        body={
            "from" : row_start, "size" : ROWS_PER_PAGE,
            'query' :{
                'query_string' :{
                    'query' : keywords,
                }
            },
            'highlight':{
                'fields':{
                    'ip':{}
                }
            }
        }
        )

        #get total rows and pages
        page_info['total_rows'] = res['hits']['total']
        page_info['total'] = int(math.ceil(page_info['total_rows'] / (ROWS_PER_PAGE * 1.0)))
        #get everyone row set
        for doc in res['hits']['hits']:
            c = doc['_source']
            page_info['rows'].append(c)   
    return page_info


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['get'])
def search():
    keywords = request.args.get('query')
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1
    page_info = search_mongodb_by_es(keywords, page)
    return render_template('search.html', keywords=keywords, page_info=page_info)


def main():
    port = 5000
    app.run(host='0.0.0.0', port = port, debug=False, threaded=True)

if __name__ == '__main__':
    main()
