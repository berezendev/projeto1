import pandas as pd

dataset=pd.read_csv('https://www.irdx.com.br/media/uploads/paises.csv')
import plotly.express as px

fig=px.scatter_geo(dataset,
                   lat=dataset['latitude'],
                   lon=dataset['longitude'],
                   hover_name=dataset['nome'])
fig.update_layout(title='Coordenada dos Países no mapa',
                  geo_scope='world')
fig.show()
fig=px.choropleth(dataset,
                   locations=dataset['iso3'],
                   color=dataset['nome'],
                   hover_name=dataset['nome'])
fig.update_layout(title='Mapa coroplético dos países',
                  geo_scope='world')
fig.show()
