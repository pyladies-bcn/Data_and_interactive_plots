
# coding: utf-8

# # Sabadell cultural events in a map

# In Open Data Sabadell also we can find the agenda of events that take place in the city, organized by categories (science and tecnology, art, music, traditions, etc.) and can be donwloded easilly from [here.](http://opendata.sabadell.cat/ca/inici/fitxes-cataleg?option=com_iasmetadadesarticles&cod=OD,CT-03-&title=Cultura%20i%20oci) 
# 
# In our case, we already downloaded the agendas in XML format related to science and tecnology, art and music. If you take a look to these files you can observe that every event have different fields. We are going to use location (longitude and latitude) and some description fields to plot them in a map filtered by a date.  
# 
# Try to understand what following code do, try to modify data value (**data = "1/2/2019 18:00"**), modify data showed in the map and modify indicator maps color (**for type,color in [(musica,'blue'),(art,'red'),(ciencia,'green')]:**).

# In[1]:

import folium
import xml.etree.ElementTree as ET
from datetime import datetime as dt

ciencia = ET.parse('DadesSabadell/cienciaitecnologia2019.xml')
art = ET.parse('DadesSabadell/artipatrimoni2019.xml')
musica = ET.parse('DadesSabadell/musica2019.xml')

map = folium.Map(location=[41.54329, 2.10942],zoom_start=13)

data = "1/2/2019 18:00"
data_input = dt.strptime(data, "%d/%m/%Y %H:%M")

for type,color in [(musica,'blue'),(art,'red'),(ciencia,'green')]:
    
    root = type.getroot()

    for activitat in root.findall('activitat'):
    
        data = activitat.find('dataInici').text
        data_event = dt.strptime(data,"%d/%m/%Y %H:%M")
    
        if activitat.find('.//lon') != None and data_input < data_event:
            
            titol= activitat.find('titol').text
            data = activitat.find('dataInici').text
            lat = float(activitat.find('.//lat').text)
            lon = float(activitat.find('.//lon').text)
            info = titol + ' '+ data
            folium.Marker([lat, lon], popup=folium.Popup(info),icon=folium.Icon(color=color)).add_to(map)
    
map.save("DadesSabadell/agenda.html")


# You can find your map creation in the following link:
# 
# [Link to generated Map... ](DadesSabadell/agenda.html)

# # Barcelona bike path under construction in a map

# There is a geolocated information file format that most of map aplications can undestand directelly. Try to execute this example using a geojson file and take a look how this file looks [like.](DadesBarcelona/CARRIL_BICI_CONSTRUCCIO.geojson)

# In[7]:

map = folium.Map(location=[41.3851, 2.1734],zoom_start=13)
folium.GeoJson("DadesBarcelona/CARRIL_BICI_CONSTRUCCIO.geojson",name='geojson').add_to(map)

map.save("DadesBarcelona/carrilbici.html")


# You can find your map creation in the following link:
# 
# [Link to generated Map... ](DadesBarcelona/carrilbici.html)

# # Poblation per district in Sabadell  

# In this example we are going to use infomartion related to Sabadell census from 2015 (population per distric, gender and year of birth). This information can be dowloaded from [here](http://opendata.sabadell.cat/ca/?option=com_content&view=article&id=4729&Itemid=209) but you can find the file used in **DadesSabadell/PadroDistricteSexeAnyNaixement2015.csv**. 
# 
# As other examples, we have to modify and group this information to obtain data of our interest: women average age, men average age, number of women, number of men and total population per district.
# 
# Take a look that how we transform this information to obtain desired table:

# In[31]:

import folium
import geojson
import pandas as pd
import seaborn
import numpy as np

df = pd.read_csv('DadesSabadell/PadroDistricteSexeAnyNaixement2015.csv')
df


# In[32]:

df['Edat'] = 2018 - df['Any_Naixement']
df = df.drop(['Any_Naixement'], axis=1)

df


# In[33]:

avg_age_df = pd.pivot_table(df,columns=["Sexe"], index=["Districte"], values=["Edat"])
avg_age_df


# In[34]:

count_df = habitants_Df = pd.pivot_table(df,columns=["Sexe"], index=["Districte"], values=["Total"],aggfunc=np.sum)
count_df


# In[37]:

total_df = pd.concat([avg_age_df, count_df], axis=1)
total_df['Districte'] = total_df.index.astype(str)

total_df.columns=[' '.join(col).strip() for col in total_df.columns.values]
total_df['Total'] = total_df['Total H'] + total_df['Total D']

total_df


# We are going to use the obtained table to plot this information in a map. The Open Data Sabadell Web Page also give us geographic information about districts that you can be downloaded [here]() or get from folder **/DadesSabadell/districte.geojson**. This file allow us to draw districts contourns and use different intensity colours to represent values obtained in previous table. This kind of representations in maps are know as chropleths.
# 
# You can try to change represented values changing **'Total'** in **columns = ['Districte', 'Total']** for per exemple **'Edat D'**,**'Edat H'**,**'Total D'** or **'Total H'**.
# 
# You can also change graph color **'YlOrRd'** and use **'BuPu'**, **'GnBu'**, **'OrRd'**, **'PuBu'**, **'PuBuGn'**, **'PuRd'**, **'RdPu'**, **'YlGn'** or **'YlGnBu'**.

# In[41]:

district_geo = 'DadesSabadell/districtes.geojson'

map1 = folium.Map(location=[41.54329, 2.10942],zoom_start=13)
map1.choropleth(geo_data=district_geo, 
              data = total_df,
              columns = ['Districte', 'Total'],
              key_on = 'feature.properties.description',
              fill_color='YlOrRd', 
              fill_opacity= 0.7,
              legend_name = 'Poblacio per districte')


map1.save('DadesSabadell/mapapoblacio.html')


# You can find your map creation in the following link:
# 
# [Link to generated Map... ](DadesSabadell/mapapoblacio.html)

# In[ ]:



