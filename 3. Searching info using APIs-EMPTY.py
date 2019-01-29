
# coding: utf-8

# # API to search film information 
# 
# APIs are services made by developers to make queries to servers and data bases open to all people that want to use it. Usually is as easy as Google search engine but you have to know which queries are available and how to make it. 
# 
# Usually some kind of identifier or key is needed to use API and make queries to an API. In this case, this identifier is usually used to limitate number of queries per minute and to have some kind of control about people using this API. APIs are widely used in web pages and mobile apps to look for updated data they need.
# 
# We are going to use an API about films information that is used by some cinemas web pages, cinema listings mobile apps, etc. 
# 
# Web page where you have to register to use this API is [The Movie Data Base](https://www.themoviedb.org/). After your registration you have to ask for a key to be able to us their API. All information related to this API usage can be find [here.](https://developers.themoviedb.org/3/getting-started/introduction) in this web page you can also try the API directly on **Try it out** tab.
# For exemple, if you want to discover about films you can look for documentation about movie discover [here.](https://developers.themoviedb.org/3/discover/movie-discover)

# Try an easy example about 'trending' where you can find information [here:](https://developers.themoviedb.org/3/trending/get-trending)

# In[ ]:

import requests

#response = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=<<API_KEY>>)
#response.text


# In[ ]:

import requests

api_key = #PUT HERE YOUR API KEY
parameters = {"api_key":api_key }

response = requests.get('https://api.themoviedb.org/3/trending/movie/week',params=parameters)
response.url


# In[ ]:

response.text


# Let see some more films API usage examples:
# 
# 1. Best films of the year. Films can be ordered by score, popularity or revenues. You can change **sort_by** parameter for: **mes_populars**, **mes_ben_valorades** or **mes_guanys**. You can also change the type of film certification: **APTA**,**7**,**12**,**16** or **18** years.
# 
# 2. Most popular films where a concret actor appears. Put the name of the actor or actress and obtain information about his/her most popular films. 
# 
# 3. Films where two actors or actresses appears. Put the name of two actor or actresses to know if they worked together in a film.
# 
# 4. Obtain films recomendations introducing a film that you have already watch. 

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import requests
import urllib
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def mostraInfoPelis(pelis):
    if (len(pelis)==0):
        print("No hi ha cap peli per mostar")
    for peli in pelis:
            print(peli['title'] +" ("+peli['release_date']+")\t***"+str(peli["vote_average"])+"***")
            im = Image.open(urllib.request.urlopen("https://image.tmdb.org/t/p/w500/"+peli['poster_path']))
            plt.figure()
            plt.title(peli['title'],size=16)
            plt.imshow(np.asarray(im))
            plt.axis('off')
            plt.show()

url_Pelis = "https://api.themoviedb.org/3/discover/movie"
url_Persones = "https://api.themoviedb.org/3/search/person"

mes_populars = "popular.desc"
mes_ben_valorades = "vote_average.desc"
mes_guanys = "revenue.desc"  
certificacio = {"APTA":"APTA","7":"7","12":"12","16":"16","18":"18"}
api_key = #PUT HERE YOUR API KEY


# In[ ]:

##### BEST FILMS!

any_ = 2018


print("Les pel·lícules de l'any: " + str(any_))

parameters = {"sort_by":mes_guanys,
              "certification_country":"ES", "page":1,
              "certification.lte":certificacio["16"],"language":"es-ES","region":"ES",
              "release_date.gte":str(any_)+("-01-01"),
              "api_key":api_key }
response = requests.get(url_Pelis,params=parameters)

if (int(response.headers["x-ratelimit-remaining"])) > 0:
    data = response.json()
    mostraInfoPelis(data["results"])
else:
    print("Intenta-ho més tard")
            


# In[ ]:

##### Most popular films from an actos/actress
actor = "Radcliffe"

parameters = {"query":actor, "page":1, 
              "language":"es-ES",
              "api_key":api_key  }

response = requests.get(url_Persones,params=parameters)
if (int(response.headers["x-ratelimit-remaining"])) > 0:
    data = response.json()
    if data["total_results"]>0:
        result = data["results"][0]
        print("Les pelis més conegudes de l'actor/actriu: " +result["name"])
        mostraInfoPelis(result["known_for"])
    else:
        print("No he trobat cap actor amb aquest nom: " +actor)
else:
    print("Intenta-ho més tard")


# In[ ]:

##### Are two actors worked together?

actor1 = "Depp"
actor2 = "DiCaprio"

escapa = False
parameters = {"query":actor1, "page":1, 
              "language":"es-ES",
              "api_key":api_key  }

response = requests.get(url_Persones,params=parameters)
if (int(response.headers["x-ratelimit-remaining"])) > 0:
    data = response.json()
    if data["total_results"]>0:
        actor1_json = data["results"][0]
    else:
        print("No he trobat cap actor amb aquest nom: " + actor1)
        escapa = True
    
    
parameters = {"query":actor2, "page":1, 
              "language":"es-ES",
              "api_key": api_key  }
response = requests.get(url_Persones,params=parameters)
if (int(response.headers["x-ratelimit-remaining"])) > 0:
    data = response.json()
    if data["total_results"]>0:
        actor2_json = data["results"][0]
    else:
        print("No he trobat cap actor amb aquest nom: " + actor2)
        escapa = True

if not escapa:  
    print("Les pelis de l'actor: " +actor1_json["name"] + " juntament amb l'actor: " +actor2_json["name"])

    parameters = {"with_people": str(actor1_json["id"]) +", "+ str(actor2_json["id"]), "page":1, 
                  "sort_by":mes_guanys,
                  "language":"es-ES",
                  "api_key": api_key}

    response = requests.get(url_Pelis,params=parameters)
    if (int(response.headers["x-ratelimit-remaining"])) > 0:
        data = response.json()
        mostraInfoPelis(data["results"])


# In[ ]:

## Digues-me recomanacions de pel·lícules que siguin tipus aquesta altra peli: ...

peli = "Bohemian Rhapsody"

escapa = False
parameters = {"query":peli, "page":1, 
              "language":"es-ES", "region": "ES",
              "api_key":api_key  }

response = requests.get("https://api.themoviedb.org/3/search/movie",params=parameters)
if (int(response.headers["x-ratelimit-remaining"])) > 0:
    data = response.json()
    if data["total_results"]>0:
        peli_json = data["results"][0]
    else:
        print("No he trobat cap peli amb aquest nom: " + peli)
        escapa = True
        
if not escapa:
    print("Recomenacions per si t'ha agradat la peli: "+peli_json["title"])
    parameters = {"page":1, 
              "language":"es-ES", "region": "ES",
              "api_key":api_key  }
    response = requests.get("https://api.themoviedb.org/3/movie/"+str(peli_json["id"])+"/recommendations",params=parameters)
    if (int(response.headers["x-ratelimit-remaining"])) > 0:
        data = response.json()
        pelis = data["results"]
        mostraInfoPelis(pelis)

