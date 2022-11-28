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

def test_dev1(request):
    sparql = SPARQLWrapper(
        "http://vocabs.ardc.edu.au/repository/api/sparql/"
        "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
    )
    sparql.setReturnFormat(JSON)

    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint
    sparql.setQuery("""
        PREFIX gts: <http://resource.geosciml.org/ontology/timescale/gts#>

        SELECT *
        WHERE {
            ?a a gts:Age .
        }
        ORDER BY ?a
        LIMIT 3
        """
    )

    try:
        ret = sparql.queryAndConvert()
        data = sparql.query()

        for r in ret["results"]["bindings"]:
            print(r)
    except Exception as e:
        data = None

    return HttpResponse(data, content_type="application/json")

def test_dev2(request):
    sparql = set_namespace("test")

    sparql.setQuery("""
        PREFIX :     <http://example.org/data/> 
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX v:    <http://example.org/vocab#> 
        PREFIX bds: <http://www.bigdata.com/rdf/search#>


        SELECT DISTINCT ?film ?filmTitle WHERE {
            
                ?film rdf:type v:Film ;
                    v:title ?filmTitle .
            
        } 
    """)

    try:
        # ret = sparql.queryAndConvert()
        data = sparql.query()

        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
        data = None

    return HttpResponse(data, content_type="application/json")

def test_dev3(request):
    sparql = set_namespace("test")

    sparql.setQuery("""
        PREFIX :     <http://example.org/data/> 
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX v:    <http://example.org/vocab#> 
        PREFIX bds: <http://www.bigdata.com/rdf/search#>


        SELECT DISTINCT ?film ?filmTitle WHERE {
            
                ?film rdf:type v:Film ;
                    v:title ?filmTitle .
            
        } 
    """)

    try:
        data = sparql.queryAndConvert()["results"]["bindings"]
        # data = sparql.query()

        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
        data = None

    return render(request, 'index.html', {'result': data})

def search(request):
    
    form = SearchForm()

    return render(request, 'base.html', {'form': form})

def test_dev4(request):
    form = SearchForm(request.POST or None)
    sparql = set_namespace("test")

    data = None

    if (form.is_valid() and request.method == 'POST'):
        search = form.cleaned_data['search']
        if search != '':
            query = """
                PREFIX :     <http://example.org/data/> 
                PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX v:    <http://example.org/vocab#> 
                PREFIX bds: <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT ?film ?filmTitle WHERE {
                    ?filmTitle bds:search """
            query += '"' + search + '" .'
            query += """
                    ?film rdf:type v:Film ;
                        v:title ?filmTitle .

                    }
            """
            
            try:
                # print(query)
                sparql.setQuery(query)
                data = sparql.queryAndConvert()["results"]["bindings"]
                # print(data)
            except Exception as e:
                print(e)
                data = None

            return render(request, 'index.html', {'result': data})
    
    else:
        form = SearchForm()

    return render(request, 'base.html', {'result': data, 'form': form})

def test_dev5(request):
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

                SELECT DISTINCT ?res ?restaurantName WHERE {
                    ?restaurantName bds:search """
            query += '"*' + search + '*" .'
            query += """
                    ?res a v:name ;
                        rdfs:label ?restaurantName .

                    }
            """
            
            try:
                # print(query)
                sparql.setQuery(query)
                data = sparql.queryAndConvert()["results"]["bindings"]
                # print(data)
            except Exception as e:
                print(e)
                data = None

            form = SearchForm() 
            return render(request, 'index.html', {'result': data, 'form': form, 'search': search})
    
    else:
        form = SearchForm()
        
    return render(request, 'base.html', {'result': data, 'form': form, 'search': search})