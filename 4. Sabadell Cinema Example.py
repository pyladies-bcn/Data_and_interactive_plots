
# coding: utf-8

# # Scrapping de dades d'internet
# 
# Finalment veurem com fer scrapping de dades de pàgines web. Fer scrapping vol dir agafar informació directament de les pàgines web, sense passar per un fitxer de dades ni per un API. En aquest cas el que fem és obrir una pàgina web i amb l'ajuda de python el que fem és buscar les dades que necessitem en el document HTML que ens envia el servidor web. 
# Fer scrapping no és senzill i hi ha certes pàgines web que no deixen que es pugui fer, intenten posar-vos-ho difícil. 
# 
# En el nostre cas anirem a la web dels cinemes eix macià de sabadell i consultarem la cartellera per avui. Buscarem les pelis que comencen a l'hora que ens interessa (amb 1.30h de marge!) i mirarem que sigui apte per la nostra edat. De les pel·lícules seleccionades obrirem el trailer de la peli que millor valorada estigui en la base de dades que hem usat abans (l'api ens donarà més informació que la de la pàgina del cinema!!!)
# 
# Per fer això el que farem serà controlar de forma automàtica un nou navegador que s'obrirà sol i farà les accions necessàries. Mireu ben bé com es va movent el nou navegador de forma autònoma i gaudiu del trailer!
# 
# 

# In[8]:

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import requests 
import datetime
import urllib
import time


edat = 18
hora = "18:00"


cinema = 'http://www.cinemeseixmacia.com/' #Poseu el nom de la pàgina web
navegador = webdriver.Chrome(ChromeDriverManager().install())
navegador.get(cinema)

hora = datetime.datetime.strptime(hora, '%H:%M')
pelis_seleccionades=[]

elements = navegador.find_elements_by_xpath('//*[@id="rt-mainbody"]/div/div[3]/div')
print("A la cartellera hi ha...:")
for e in elements:
     if e.is_displayed():   
        e = e.find_element_by_class_name("text")
        peli={}
        peli["puntuacio"] = 0
        peli["release"] = ""
        peli["classi"] = e.find_element_by_id("dadespeli").find_element_by_class_name("classi").get_attribute('textContent')
        horaris = e.find_elements_by_class_name("horasessio")
        peli["horaris"] = [datetime.datetime.strptime(h.find_element_by_tag_name("button").get_attribute('textContent').strip(), '%H:%M') for h in horaris]
        peli["nom"] = e.find_element_by_tag_name("a").get_attribute("name").strip()
        if any ([( datetime.timedelta(minutes=0, hours=0)  <= x-hora <= datetime.timedelta( hours=1, minutes=30)) for x in peli["horaris"]]):
            if peli["classi"] == "APTA" or edat > int(peli["classi"][0:2]) :
                peli["trailer"] = e.find_element_by_class_name("peli-boto-trailer")
                pelis_seleccionades.append(peli)
        url_google = 'http://www.google.es/search?q='+ urllib.parse.quote(peli["nom"].lower()+" site:imdb.com") 
        print(url_google)

print("Seleccionades...:")
for peli in pelis_seleccionades:
    
    url = "https://api.themoviedb.org/3/search/movie"
    parameters = {"include_adult":False, "page":1, "region": "ES", "query": peli["nom"],"language":"es-ES", "api_key":"ad38c5a701d46fed6b0ebc7c3d25dd49"  }
    response = requests.get(url,params=parameters)
    if (int(response.headers["x-ratelimit-remaining"])) > 0:
        data = response.json()
        if len(data["results"]) > 0 :
            millor_result = data["results"][0]
            peli["puntuacio"] = millor_result["vote_average"]
            peli["release"] = millor_result["release_date"]
    else:
        print("Torna-ho a intentar")
    print(peli["release"]+" - "+peli["nom"]+ "("+peli["classi"]+") "+ str([ y.time().strftime("%H:%M") for y in peli["horaris"]]) + "*** " + str(peli["puntuacio"]))


ordenada = sorted(pelis_seleccionades, key=lambda k: k['puntuacio'], reverse=True)
ActionChains(navegador).move_to_element(ordenada[0]["trailer"]).perform()
time.sleep(5)
navegador.execute_script("arguments[0].click();", ordenada[0]["trailer"])
elm = navegador.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]')
urlStr = elm.get_attribute("src");
elm.click()
print("Clicka!")
print(urlStr)
print("He acabat!")


