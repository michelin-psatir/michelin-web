# michelin-web

Lorem Ipsum

---

### Setup Guide

**First Time**
1. Clone the repository and create a new branch.
2. Install Django. I will not go further, you've done this before.
3. Install node.js. You can search it up yourself. Note to make sure the installation path is on `"C:\Program Files\nodejs\npm.cmd"`
4. `python -m pip install django-tailwind`
5. `python manage.py tailwind install`
6. `pip install sparqlwrapper`

---

### Running Guide
On 2 separate windows pointing towards the project's directory
1. `python manage.py tailwind start`
2. `py manage.py runserver`
3. [Optional] `java -server -Xmx4g -jar blazegraph.jar`

> **Special Note:**    
> Currently, there are 2 apps, `michelin` and `theme`. `theme` is the development, experimental, and testing zone. Use it to develop and try out feature. Once you're sure of a feature, move it to `michelin` and change `TAILWIND_APP_NAME` on `michelinweb/settings.py`, and then proceed to do `python manage.py tailwind install`. This will prepare the `michelin` tailwind app.

---

### References
https://github.com/blazegraph/database/wiki/REST_API    
https://github.com/blazegraph/database    
https://github.com/blazegraph/blazegraph-samples    
https://github.com/blazegraph/database/wiki/REST_API    
https://github.com/blazegraph/database/wiki/FullTextSearch    
https://django-tailwind.readthedocs.io/en/latest/installation.html    
https://sparqlwrapper.readthedocs.io/en/latest/main.html     
https://wiki.app.uib.no/info216/index.php/Lab:_SPARQL_Programming    
https://github.com/RDFLib/rdflib    
https://github.com/RDFLib/sparqlwrapper    
