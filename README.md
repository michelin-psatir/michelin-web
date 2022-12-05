# michelin-web

This is a website to search Michelin Restaurant based on the dataset provided by [Kaggle](https://www.kaggle.com/datasets/jackywang529/michelin-restaurants) using SPARQL query, thus implementing a semantic-based search engine on an RDF graph.    
    
This project is part of a final project from the Semantic Web Course on Universitas Indonesia Faculty of Computer Science.

---

## Setup Guide

### First Time Setup

**Cloning Repository**
1. Clone the repository
2. Create a new branch for development `git checkout -b dev`
3. Pull from remote by `git pull origin dev`

**Special Note for Collaborators Regarding Git**
It is **HIGHLY** recommended for you to create your own branch to do development. You can obtain the most updated content by pulling from the `dev` branch, and then once finished, push towards your branch and create a pull request towards the `dev` branch to avoid conflicts.
    
**Setting Up Dependencies**
Option 1 - Untested but using `requirements.txt`
1. `pip install -r requirements.txt`
    
Option 2 - Manual
1. Install Django and Node.JS.
2. `python -m pip install django-tailwind`
3. `pip install sparqlwrapper`
4. `python manage.py tailwind install`

> Note to check on `michelinweb/settings.py` and make sure the directory for node.JS binary is listed according to your OS:    
> Windows   : `r"C:\Program Files\nodejs\npm.cmd"`    
> Linux     : `r"/usr/bin/npm"`    
> _But note also, this depends on your node.JS installation directory_    

**Setting Up Blazegraph Locally**
1. Download the `jar` file for BlazeGraph and BigData
2. Open a command window pointing to the directory
3. Run the Blazegraph database locally using `java -server -Xmx4g -jar blazegraph.jar`
4. Go towards namespace tab and add new namespace titled `michelin-final` with the default settings
5. Select the newly created namespace by pressing `use` until the namespace used is the same as the namespace title on the top right
6. Open the update tab and upload the corresponding `ttl` file
7. Go back towards the namespace tab and click `Rebuild Full Text Index` and press `OK` on all dialogue
8. Blazegraph should be done. Go back towards the command window and press `CTRL+C` to stop the database instance


---

### Running Guide
On 2 separate windows pointing towards the project's directory:    
Window A: `python manage.py tailwind start`    
Window B: `py manage.py runserver`    
    
[Optional] Then, open another window pointing towards the Blazegraph directory and run the command tu initiate the database   
Window Blazegraph: `java -server -Xmx4g -jar blazegraph.jar`

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
