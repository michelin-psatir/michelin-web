from django.http.response import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from .forms import *

from SPARQLWrapper import SPARQLWrapper, JSON

NAMESPACE = "michelin-final"
URI = "http://www.example.org/"

def set_namespace(name):
    namespace = name
    sparql = SPARQLWrapper("http://localhost:9999/blazegraph/namespace/"+ namespace + "/sparql")
    sparql.setReturnFormat(JSON)
    return sparql


def search(request):
    
    form = SearchForm()

    return render(request, 'base.html', {'form': form})

def error404(request):
    
    form = SearchForm()

    return render(request, '404error.html', {'form': form})

def query(request):
    form = SearchForm(request.POST or None)
    sparql = set_namespace(NAMESPACE)

    data = None

    if (form.is_valid() and request.method == 'POST'):
        search = form.cleaned_data['search']
        if search != '':
            query = """
                PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX  owl: <http://www.w3.org/2002/07/owl#> 
                PREFIX  v: <http://www.example.org/vocab/> 
                PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX  foaf: <http://xmlns.com/foaf/0.1/> 
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

            if data is not None and data is not [] and data:
                return render(request, 'index.html', {'result': data, 'form': form, 'search': search})
        
        else:
            query = """
                PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX  owl: <http://www.w3.org/2002/07/owl#> 
                PREFIX  v: <http://www.example.org/vocab/> 
                PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX  foaf: <http://xmlns.com/foaf/0.1/> 
                PREFIX bds: <http://www.bigdata.com/rdf/search#>

                SELECT DISTINCT (?res AS ?restaurantID) ?restaurantName ?stars ?city ?year WHERE {
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

            if data is not None and data is not [] and data:
                return render(request, 'index.html', {'result': data, 'form': form, 'search': search})

    
    else:
        form = SearchForm()
        
    return error404(request)

def fetch_details(request, id):
    sparql = set_namespace(NAMESPACE)
    form = SearchForm()
    object_id = URI + id
    data_local = None
    data_remote = None

    if object_id != '':

        # Query for Local Data

        query = """
                PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                PREFIX  owl: <http://www.w3.org/2002/07/owl#> 
                PREFIX  v: <http://www.example.org/vocab/> 
                PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX  foaf: <http://xmlns.com/foaf/0.1/> 

                SELECT ?nameURI ?name ?year ?latitude ?longitude ?city ?region ?zipCode ?cuisine ?price ?url ?stars WHERE {
                ?nameURI a v:name;
                            rdfs:label ?name;
                            v:year ?year;
                            v:latitude ?latitude;
                            v:longitude ?longitude;
                            v:city ?cityURI;
                            v:cuisine ?cuisineURI;
                            v:url ?url;
                            v:stars ?stars;
                            v:searchableName ?searchableName.
                ?cityURI rdfs:label ?city;
                        v:region ?regionURI.
                OPTIONAL {
                    ?nameURI v:zipCode ?zipCode.
                }
                OPTIONAL {
                    ?nameURI v:price ?price.
                }
                ?cuisineURI rdfs:label ?cuisine.
                ?regionURI rdfs:label ?region.

                FILTER ( strstarts(str(?nameURI),"""
        query += '"' + object_id + '"'
        query += """) )
                } ORDER BY ?name
        """
        
        try:
            # print(query)
            sparql.setQuery(query)
            data_local = sparql.queryAndConvert()["results"]["bindings"]
        except Exception as e:
            print(e)
            data_local = None

        # Query for Remote Data

        name = data_local[0]['name']['value']

        if name is not None and name and name != '':
            query = """
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wds: <http://www.wikidata.org/entity/statement/>
            PREFIX wdv: <http://www.wikidata.org/value/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX wikibase: <http://wikiba.se/ontology#>
            PREFIX p: <http://www.wikidata.org/prop/>
            PREFIX ps: <http://www.wikidata.org/prop/statement/>
            PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX bd: <http://www.bigdata.com/rdf#>
            PREFIX schema: <http://schema.org/>
            
            
            SELECT DISTINCT ?resto (?restoLabel AS ?name) ?tripAdvisorID (?managerLabel AS ?manager) ?yearEstablished ?streetAddress ?officialWebsite ?imageURL WHERE {
            SERVICE <https://query.wikidata.org/sparql> {
                SELECT DISTINCT ?resto ?restoLabel ?tripAdvisorID ?managerLabel ?yearEstablished ?streetAddress ?officialWebsite ?imageURL WHERE {
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } {
                    SELECT DISTINCT ?resto ?restoLabel ?tripAdvisorID ?manager ?yearEstablished ?streetAddress ?officialWebsite ?imageURL WHERE {
                    ?resto p:P166 ?michelinAward.
                    ?michelinAward pq:P1114 ?stars;
                                    pq:P580 ?date.
                    BIND(YEAR(?date) AS ?year).
            
                    OPTIONAL {
                        ?resto wdt:P3134 ?tripAdvisorID.
                    }
                    OPTIONAL {
                        ?resto wdt:P1037 ?manager.
                    }
                    OPTIONAL {
                        ?resto wdt:P571 ?timeEstablished.
                        BIND(YEAR(?timeEstablished) AS ?yearEstablished).
                    }
                    OPTIONAL {
                        ?resto wdt:P6375 ?streetAddress.
                    }
                    OPTIONAL {
                        ?resto wdt:P856 ?officialWebsiteURI.
                        BIND(STR(?officialWebsiteURI) AS ?officialWebsite)
                    }
                    OPTIONAL {
                        ?resto wdt:P18 ?imageURI.
                        BIND(STR(?imageURI) AS ?imageURL).
                    }
            
                    FILTER(?year = 2019).
                    }
                }
                }
            }
            
            FILTER(REGEX(?restoLabel, """
            query += '"' + name + '"'
            query += """)). 
            }
            """
            
            try:
                # print(query)
                sparql.setQuery(query)
                data_remote = sparql.queryAndConvert()["results"]["bindings"]
            except Exception as e:
                print(e)
                data_remote = None


            # query = """
            #     PREFIX  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            #     PREFIX  owl: <http://www.w3.org/2002/07/owl#> 
            #     PREFIX  v: <http://www.example.org/vocab/> 
            #     PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            #     PREFIX  foaf: <http://xmlns.com/foaf/0.1/> 
            #     PREFIX bds: <http://www.bigdata.com/rdf/search#>

            #     SELECT DISTINCT (?res AS ?restaurantID) ?restaurantName ?stars ?city ?year WHERE {
            #         ?restaurantName bds:search """
            # query += '"*' + search + '*" .'
            # query += """
            #         ?res a v:name ;
            #             rdfs:label ?restaurantName ;
            #             v:stars ?stars ;
            #             v:city [ rdfs:label ?city ] ;
            #             v:year ?year .

            #         }
            # """
            
            # try:
            #     # print(query)
            #     sparql.setQuery(query)
            #     dataNearby = sparql.queryAndConvert()["results"]["bindings"]
            # except Exception as e:
            #     print(e)
            #     dataNearby = None

        local_valid = data_local is not None and data_local is not [] and data_local
        remote_valid = data_remote is not None and data_remote is not [] and data_remote

        if local_valid or remote_valid:
            return render(request, 'detail.html', {'resultLocal': data_local, 'resultRemote': data_remote, 'form': form,})

    return error404(request)