from django.http.response import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from .forms import *

from SPARQLWrapper import SPARQLWrapper, JSON

def set_namespace():
    namespace = "test"
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
    namespace = "test"
    sparql = SPARQLWrapper("http://localhost:9999/blazegraph/namespace/"+ namespace + "/sparql")
    sparql.setReturnFormat(JSON)

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
    namespace = "test"
    sparql = SPARQLWrapper("http://localhost:9999/blazegraph/namespace/"+ namespace + "/sparql")
    sparql.setReturnFormat(JSON)

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
    sparql = set_namespace()

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