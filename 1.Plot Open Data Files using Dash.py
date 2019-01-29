
# coding: utf-8

# # Open Data Sabadell
# 
# 
# http://opendata.sabadell.cat/ca/
# 
# From main page **Catàleg** we select **Medi Ambient** (Environment) category.  
# In there, we can find a file related to municipal waste that can be downloaded from [here.](http://opendata.sabadell.cat/index.php?option=com_iasopendata&view=download&format=raw&urlOData=aHR0cDovL29kYXRhLnNhYmFkZWxsLmNhdC9vZGF0YTRQcm9kdWN0b3Ivb2RhdGE0UHJvZHVjdG9yLnN2Yy9NYXRlcmlhbHNSZXNpZHVzLz9mb3JtYXQ9Y3N2JmlkZGlzdD0xNDYyJiRzZWxlY3Q9T3JkcmUsQW55byxJZE1hdGVyaWFsLE5vbU1hdGVyaWFsLFF1YW50aXRhdCxVbml0YXRz) But you can find a copy of this file named **residus.csv** in this tutorial dataset in **DadesSabadell** folder.
# 
# The file obtained is in a CSV format (Comma Separated Value). This means that it is 
# like a table where the rows are registers and the columns are fields or values associated to this register. 
# 
# You can take a look into this file in table-like representation provided in the open data web page following this link: [OpenData Sabadell](http://opendata.sabadell.cat/ca/inici/odata?iddist=1462). Looking this table we can observe that every register represents an amount of waste origined in Sabadell in tones associated with a particular year and a waste type classification.
# 
# In this exercice we are going to follow this steps:
# * Read residus.csv file.
# * Group data to obtain more readable information. Every row will be a type of waste and the columns will be a year related to this data.
# * Represent data in an interactive way.
#     
# **Important:** Nan values indicate that there is no infomation related to this type of waste and year.
# 

# To read data and manage it we are going to use [pandas](https://pandas.pydata.org/) library:

# In[1]:

import pandas as pd

df = pd.read_csv("DadesSabadell/residus.csv",sep=';')
df.sort_values(by="Anyo",inplace = True)

df


# In[ ]:




# In[3]:

materials = list(df.NomMaterial.unique())
materials.remove("Resta")

print ('{} diferent types of wastes:'.format(len(materials)))
materials


# In[4]:

pd.pivot_table(df,columns="Anyo", index = "NomMaterial", values="Quantitat")


# All is prepared to plot our data. We are going to us Dash (web-based interfaces in Python) to plot information and give them interactivity.
# 
# If you are interested to learn more about Dash you can follow the offical [tutorial.](https://dash.plot.ly/)
# 
# [Dash installation:](https://dash.plot.ly/installation)
# 
# * **pip install dash**  # The core dash backend
# * **pip install dash-html-components**  # HTML components
# * **pip install dash-core-components**  # Supercharged components
# * **pip install dash-table**  # Interactive DataTable component (new!)

# In[5]:

get_ipython().run_cell_magic(u'writefile', u'my_app1.py', u"#Dash empty structure\nimport dash\nimport dash_core_components as dcc\nimport dash_html_components as html\n\napp = dash.Dash()\n\napp.layout = html.Div('Hello Dash!')\n\nif __name__ == '__main__':\n    app.run_server(debug=True)")


# In[6]:

get_ipython().system(u'python3 my_app1.py')


# In[7]:

get_ipython().run_cell_magic(u'writefile', u'my_app2.py', u'#Dash simple example\nimport dash\nimport dash_core_components as dcc\nimport dash_html_components as html\n\napp = dash.Dash()\n\napp.layout = html.Div([html.H1("Hello Dash!"),\n                       \n              html.Div(\'\'\'\n                Dash: A web application framework for Python.\n              \'\'\'),\n                      \n              dcc.Graph(id=\'exmaple-graph\',\n                        figure = {\n                            \'data\':[\n                                {\'x\': [1, 2, 3], \'y\': [4.2, 1.8, 2.7], \'type\': \'bar\', \'name\': \'Sabadell\'},\n                                {\'x\': [1, 2, 3], \'y\': [2.8, 4.9, 5.1], \'type\': \'bar\', \'name\': \'Barcelona\'},\n                            ],\n                            \'layout\':{\n                                \'title\' : \'Dash Data Visualisation\'\n                            }\n              })\n])\n\nif __name__ == \'__main__\':\n    app.run_server(debug=True)')


# In[8]:

get_ipython().system(u'python3 my_app2.py')


# In[20]:

get_ipython().run_cell_magic(u'writefile', u'my_app3.py', u'#Dash simple example\nimport pandas as pd\nimport dash\nimport dash_core_components as dcc\nimport dash_html_components as html\nimport plotly.graph_objs as go\nfrom plotly import tools\n\ndf = pd.read_csv("DadesSabadell/residus.csv",sep=\';\')\ndf.sort_values(by="Anyo",inplace = True)\n\nmaterials = list(df.NomMaterial.unique())\nmaterials.remove("Resta")\n\npd.pivot_table(df,columns="Anyo", index = "NomMaterial", values="Quantitat")\n\nminim = 0\nmaxim = 1000\npas = 100\n\napp = dash.Dash()\napp.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})\n\napp.layout = html.Div([html.Div([dcc.Graph(id=\'residus_graph\')],\n                                style={\'height\':\'80%\',\'padding\': \'0px 20px 20px 20px\'}),\n                                html.Div([html.H5("Materials amb mitjana de tones per any m\xe9s grans que:"),\n                                    dcc.Slider(id=\'avg-tones\',step = pas,min=minim,max=maxim,value=maxim/2,       \n                                            marks={ str(tones): {\'label\':str(tones)} for tones in range(minim,maxim+pas,pas)})],\n                       style={\'margin\':\'auto\',\'height\':\'20%\',\'width\': \'70%\', \'padding\': \'0px 0px 40px 40px\',"display":\'inline_block\'})])\n\n@app.callback(\n    dash.dependencies.Output(\'residus_graph\', \'figure\'),\n    [dash.dependencies.Input(\'avg-tones\', \'value\')])\n\ndef update_figure(avg_tones):\n    fig = tools.make_subplots(rows=2, cols=1,shared_xaxes=True, vertical_spacing=0.001)\n    traces = []\n    \n    filtered= df[df[\'NomMaterial\'] =="Resta"]\n    trace_Resta = go.Scatter(\n                            x=filtered[\'Anyo\'],y=filtered[\'Quantitat\'],text="Resta",\n                            mode=\'lines+markers\',\n                            opacity=0.7,\n                            marker={\n                                \'size\': 15,\n                                \'line\': {\'width\': 0.5, \'color\': \'white\'}\n                            },\n                            name="Resta"\n                        )  \n    \n    filtered = df[df[\'NomMaterial\'].isin(materials)].groupby("Anyo").sum()\n    trace_Total= go.Scatter(                      \n                            x=filtered.index,y=filtered[\'Quantitat\'],text="Total Materials",\n                            mode=\'lines+markers\',\n                            opacity=0.7,\n                            marker={\n                                \'size\': 15,\n                                \'line\': {\'width\': 0.5, \'color\': \'white\'}\n                            },\n                            name="Total Materials",\n                            \n                        )   \n    \n    fig.append_trace(trace_Resta, 1, 1)\n    fig.append_trace(trace_Total, 1, 1)\n    \n    for i in materials :\n        filtered= df[df[\'NomMaterial\'] == i]\n        y=filtered[\'Quantitat\']\n        if (y.mean()>avg_tones) :\n            x=filtered[\'Anyo\']\n            traces.append(go.Scatter(x=x,y=y,text=i,mode=\'markers\',opacity=0.7,\n                                marker={\n                                    \'size\': 15,\n                                    \'line\': {\'width\': 0.5, \'color\': \'white\'}\n                                }, name=i[0:30])) \n    for trace in traces:\n        fig.append_trace(trace, 2, 1)\n\n\n    fig[\'layout\'].update(height=600,title="Residus a Sabadell", margin={\'l\': 50, \'b\': 40, \'t\': 40, \'r\': 50},\n              yaxis1={"title":"Totals"}, yaxis2={"title":"Materials"},hovermode="closest")\n    return fig\n\n\nif __name__ == \'__main__\':\n    app.run_server()\n    \n    ')


# In[21]:

get_ipython().system(u'python3 my_app3.py')


# # Open Data Barcelona 
# 
# **EXERCICE**
# 
# Using information of 2017's births in Barcelona Districts that you can find at [Open Data Barcelona](http://opendata-ajuntament.barcelona.cat/en/) that you can download [here](http://opendata-ajuntament.barcelona.cat/data/en/dataset/est-demo-naixements-sexe), try to obtain a fancy plot showing girls and boys births per different Barcelona District(Slicer is not necessary). 
# 
# You also can find this the CSV file with this information in `DadesBarcelona/2017_naixements_sexe.csv`
# 
# 

# In[13]:

import pandas as pd

df = pd.read_csv("DadesBarcelona/2017_naixements_sexe.csv",sep=',')

df


# In[14]:

pd.pivot_table(df,columns="Sexe", index = "Nom_Barri", values="Nombre")


# In[41]:

import numpy as np
pd.pivot_table(df,columns="Sexe", index = "Nom_Districte", values="Nombre",aggfunc=np.sum)


# In[52]:

get_ipython().run_cell_magic(u'writefile', u'my_exercice.py', u'#Dash exercice\nimport pandas as pd\nimport dash\nimport dash_core_components as dcc\nimport dash_html_components as html\nimport plotly.graph_objs as go\nfrom plotly import tools\n\nimport numpy as np\n\ndf = pd.read_csv("DadesBarcelona/2017_naixements_sexe.csv",sep=\',\')\npv = pd.pivot_table(df,columns="Sexe", index = "Nom_Districte", values="Nombre",aggfunc=np.sum)\n\napp = dash.Dash()\napp.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})\n\napp.layout = html.Div([html.Div(\n    [dcc.Graph(id=\'birth_bcn\',figure = {\n                            \'data\':[\n                                {\'x\': pv.index, \'y\': pv["Nens"], \'type\': \'bar\', \'name\': \'Nens\'},\n                                {\'x\': pv.index,  \'y\': pv["Nenes"], \'type\': \'bar\', \'name\': \'Nenes\'},\n                                {\'x\': pv.index, \'y\': pv["Nens"], \'type\': \'lines+markers\', \'name\': \'Nens\', \'visible\' : "legendonly"},\n                                {\'x\': pv.index,  \'y\': pv["Nenes"], \'type\': \'lines+markers\', \'name\': \'Nenes\',\'visible\' : "legendonly"},\n                            ],\n                            \'layout\':{\n                                \'title\' : \'Births Data Visualisation\'\n                            }\n                              } )\n                                ],\n                                style={\'height\':\'80%\',\'padding\': \'0px 20px 20px 20px\'},\n                                \n                               )])\n\n\n\n\nif __name__ == \'__main__\':\n    app.run_server(debug=True)\n\n\nif __name__ == \'__main__\':\n    app.run_server()')


# In[53]:

get_ipython().system(u'python3 my_exercice.py')

