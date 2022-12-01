from django.http.response import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from .forms import *

from SPARQLWrapper import SPARQLWrapper, JSON

def set_namespace(name):
    namespace = name
    sparql = SPARQLWrapper("http://localhost:9999/blazegraph/namespace/"+ namespace + "/sparql")
    sparql.setReturnFormat(JSON)
    return sparql


def search(request):
    
    form = SearchForm()

    return render(request, 'base.html', {'form': form})

def query(request):
    form = SearchForm(request.POST or None)
    sparql = set_namespace("michelin-prelim-v1")

    data = None

    if (form.is_valid() and request.method == 'POST'):
        search = form.cleaned_data['search']
        if search != '':
            query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX owl: <http://www.w3.org/2002/07/owl#> 
                PREFIX v: <http://www.example.org/> 
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
                PREFIX bds: <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT (?res AS ?restaurantID) ?restaurantName ?stars ?city ?year WHERE {
                    ?restaurantName bds:search """
            query += '"*' + search + '*" .'
            query += """
                    ?res a v:name ;
                        rdfs:label ?restaurantName ;
                        v:stars ?stars ;
                        v:city [ rdfs:label ?city ] ;
                        v:year ?year .

                    }
            """
            
            try:
                # print(query)
                sparql.setQuery(query)
                data = sparql.queryAndConvert()["results"]["bindings"]
            except Exception as e:
                print(e)
                data = None

            form = SearchForm() 
            return render(request, 'index.html', {'result': data, 'form': form, 'search': search})
    
    else:
        form = SearchForm()
        
    return render(request, 'base.html', {'result': data, 'form': form, 'search': search})