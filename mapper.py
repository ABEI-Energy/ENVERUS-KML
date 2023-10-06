import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
# %%
# Foldering
rootFolder = os.getcwd()
rootUser = rootFolder.split('\\')

ABEIUser = '\\'.join(rootUser[0:3]) + "\\ABEIOneDrive"
try:
    os.path.exists(ABEIUser)   
except Exception as e:
    ABEIUser = '\\'.join(rootUser[0:3])
# C:\Users\usuario\ABEI Energy\Prom. Estudios Técnicos - Documentos\01- ESPAÑA
if not os.path.exists(ABEIUser):
    ABEIUser = '\\'.join(rootUser[0:3])

rootRoomba = ABEIUser + "\\ABEI Energy\\OT-Digital - Documentos\\2. Out\\Roomba\\Mapas"

root_bash = rootFolder + '\\Excel' 

os.chdir("json files")

with open("REE_220.json",'r') as json_file_220:
    REE_220 = json.load(json_file_220)

dic_220 = {}

with open("REE_400.json",'r') as json_file_400:
    REE_400 = json.load(json_file_400)

dic_400 = {}

# %%
# Gather 220 

for entry in REE_220.keys():

    if entry == "data time":
        month = REE_220['data time']
        continue

    dic_220[entry] = {}
    dic_220[entry]['Latitude'] = REE_220[entry]['Latitude']
    dic_220[entry]['Longitude'] = REE_220[entry]['Longitude']
    for sub_entry in REE_220[entry]:
        


        if sub_entry == 'Total Generaciones (MW)':

            dic_220[entry]['Total Generaciones (MW)'] = pd.read_json(REE_220[entry][sub_entry])


df_aux = pd.DataFrame(columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso'])
df_220 = pd.DataFrame(columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso'])

for key, inner_dic in dic_220.items():
    df_aux = inner_dic['Total Generaciones (MW)']
    df_aux.columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso']
    df_aux.reset_index(inplace=True, drop = True)
    df_aux['Nudo'] = key
    df_aux['Latitude'] = inner_dic['Latitude']
    df_aux['Longitude'] = inner_dic['Longitude']

    df_220 = pd.concat([df_220,df_aux])
    df_220.reset_index(inplace=True, drop = True)


df_220_RdD = df_220.loc[df_220['[MW]']=="RdD"]
df_220_RdT = df_220.loc[df_220['[MW]']=="RdT"]
df_220_RdD.reset_index(inplace = True, drop = True)
df_220_RdT.reset_index(inplace = True, drop = True)

df_220_RdD['Latitude'] = df_220_RdD['Latitude'].astype(float)
df_220_RdD['Longitude'] = df_220_RdD['Longitude'].astype(float)
df_220_RdD['PES RdD 220'] = df_220_RdD['PES'].astype(float)
df_220_RdD['Aut.Acc. y Aut.Conex. Pte. PES RdD 220'] = df_220_RdD['Aut.Acc. y Aut.Conex. Pte. PES'].astype(float)
df_220_RdD['Aut.Acc. sin Aut.Conex. Pte. PES RdD 220'] = df_220_RdD['Aut.Acc. sin Aut.Conex. Pte. PES'].astype(float)
df_220_RdD['Total Aut. Pte. PES RdD 220'] = df_220_RdD['Total Aut. Pte. PES'].astype(float)
df_220_RdD['PES ÷ Aut.Acc. Pte. PES RdD 220'] = df_220_RdD['PES ÷ Aut.Acc. Pte. PES'].astype(float)
df_220_RdD['Sol.Acc. en curso RdD 220'] = df_220_RdD['Sol.Acc. en curso'].astype(float)

df_220_RdT['Latitude'] = df_220_RdT['Latitude'].astype(float)
df_220_RdT['Longitude'] = df_220_RdT['Longitude'].astype(float)
df_220_RdT['PES RdT 220'] = df_220_RdT['PES'].astype(float)
df_220_RdT['Aut.Acc. y Aut.Conex. Pte. PES RdT 220'] = df_220_RdT['Aut.Acc. y Aut.Conex. Pte. PES'].astype(float)
df_220_RdT['Aut.Acc. sin Aut.Conex. Pte. PES RdT 220'] = df_220_RdT['Aut.Acc. sin Aut.Conex. Pte. PES'].astype(float)
df_220_RdT['Total Aut. Pte. PES RdT 220'] = df_220_RdT['Total Aut. Pte. PES'].astype(float)
df_220_RdT['PES ÷ Aut.Acc. Pte. PES RdT 220'] = df_220_RdT['PES ÷ Aut.Acc. Pte. PES'].astype(float)
df_220_RdT['Sol.Acc. en curso RdT 220'] = df_220_RdT['Sol.Acc. en curso'].astype(float)



# %%
# Gather 400 

for entry in REE_400.keys():

    if entry == "data time":
        month = REE_400['data time']
        continue

    dic_400[entry] = {}
    dic_400[entry]['Latitude'] = REE_400[entry]['Latitude']
    dic_400[entry]['Longitude'] = REE_400[entry]['Longitude']
    for sub_entry in REE_400[entry]:
        


        if sub_entry == 'Total Generaciones (MW)':

            dic_400[entry]['Total Generaciones (MW)'] = pd.read_json(REE_400[entry][sub_entry])


df_aux = pd.DataFrame(columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso'])
df_400 = pd.DataFrame(columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso'])

for key, inner_dic in dic_400.items():
    df_aux = inner_dic['Total Generaciones (MW)']
    df_aux.columns = ['[MW]', 'PES', 'Aut.Acc. y Aut.Conex. Pte. PES', 'Aut.Acc. sin Aut.Conex. Pte. PES', 'Total Aut. Pte. PES', 'PES ÷ Aut.Acc. Pte. PES', 'Sol.Acc. en curso']
    df_aux.reset_index(inplace=True, drop = True)
    df_aux['Nudo'] = key
    df_aux['Latitude'] = inner_dic['Latitude']
    df_aux['Longitude'] = inner_dic['Longitude']

    df_400 = pd.concat([df_400,df_aux])
    df_400.reset_index(inplace=True, drop = True)


df_400_RdD = df_400.loc[df_400['[MW]']=="RdD"]
df_400_RdT = df_400.loc[df_400['[MW]']=="RdT"]
df_400_RdD.reset_index(inplace = True, drop = True)
df_400_RdT.reset_index(inplace = True, drop = True)

df_400_RdD['Latitude'] = df_400_RdD['Latitude'].astype(float)
df_400_RdD['Longitude'] = df_400_RdD['Longitude'].astype(float)
df_400_RdD['PES RdD 400'] = df_400_RdD['PES'].astype(float)
df_400_RdD['Aut.Acc. y Aut.Conex. Pte. PES RdD 400'] = df_400_RdD['Aut.Acc. y Aut.Conex. Pte. PES'].astype(float)
df_400_RdD['Aut.Acc. sin Aut.Conex. Pte. PES RdD 400'] = df_400_RdD['Aut.Acc. sin Aut.Conex. Pte. PES'].astype(float)
df_400_RdD['Total Aut. Pte. PES RdD 400'] = df_400_RdD['Total Aut. Pte. PES'].astype(float)
df_400_RdD['PES ÷ Aut.Acc. Pte. PES RdD 400'] = df_400_RdD['PES ÷ Aut.Acc. Pte. PES'].astype(float)
df_400_RdD['Sol.Acc. en curso RdD 400'] = df_400_RdD['Sol.Acc. en curso'].astype(float)

df_400_RdT['Latitude'] = df_400_RdT['Latitude'].astype(float)
df_400_RdT['Longitude'] = df_400_RdT['Longitude'].astype(float)
df_400_RdT['PES RdT 400'] = df_400_RdT['PES'].astype(float)
df_400_RdT['Aut.Acc. y Aut.Conex. Pte. PES RdT 400'] = df_400_RdT['Aut.Acc. y Aut.Conex. Pte. PES'].astype(float)
df_400_RdT['Aut.Acc. sin Aut.Conex. Pte. PES RdT 400'] = df_400_RdT['Aut.Acc. sin Aut.Conex. Pte. PES'].astype(float)
df_400_RdT['Total Aut. Pte. PES RdT 400'] = df_400_RdT['Total Aut. Pte. PES'].astype(float)
df_400_RdT['PES ÷ Aut.Acc. Pte. PES RdT 400'] = df_400_RdT['PES ÷ Aut.Acc. Pte. PES'].astype(float)
df_400_RdT['Sol.Acc. en curso RdT 400'] = df_400_RdT['Sol.Acc. en curso'].astype(float)




html_folder = str(month)
# C:\Users\GonzalodeCáceres\ABEIOneDrive\ABEI Energy\Prom. Estudios Técnicos - Documentos\01- ESPAÑA\08.- NUEVOS PROYECTOS\PDFs REE y Distribuidoras\21.-Marzo 23 - Copy
rootHtmls = Path(rootRoomba, html_folder)
rootHtmls.mkdir(parents=True, exist_ok=True)
os.chdir(rootHtmls)

fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='PES RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("PES RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='PES RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("PES RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='PES RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("PES RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='PES RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("PES RdD 400.html")



fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='Aut.Acc. y Aut.Conex. Pte. PES RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Aut.Acc. y Aut.Conex. Pte. PES RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='Aut.Acc. y Aut.Conex. Pte. PES RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Aut.Acc. y Aut.Conex. Pte. PES RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='Aut.Acc. y Aut.Conex. Pte. PES RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Aut.Acc. y Aut.Conex. Pte. PES RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='Aut.Acc. y Aut.Conex. Pte. PES RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Aut.Acc. y Aut.Conex. Pte. PES RdD 400.html")



fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='Aut.Acc. sin Aut.Conex. Pte. PES RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Aut.Acc. sin Aut.Conex. Pte. PES RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='Aut.Acc. sin Aut.Conex. Pte. PES RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Aut.Acc. sin Aut.Conex. Pte. PES RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='Aut.Acc. sin Aut.Conex. Pte. PES RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Aut.Acc. sin Aut.Conex. Pte. PES RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='Aut.Acc. sin Aut.Conex. Pte. PES RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Aut.Acc. sin Aut.Conex. Pte. PES RdD 400.html")



fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='Total Aut. Pte. PES RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Total Aut. Pte. PES RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='Total Aut. Pte. PES RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Total Aut. Pte. PES RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='Total Aut. Pte. PES RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Total Aut. Pte. PES RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='Total Aut. Pte. PES RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Total Aut. Pte. PES RdD 400.html")



fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='PES ÷ Aut.Acc. Pte. PES RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("PES ÷ Aut.Acc. Pte. PES RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='PES ÷ Aut.Acc. Pte. PES RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("PES ÷ Aut.Acc. Pte. PES RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='PES ÷ Aut.Acc. Pte. PES RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("PES ÷ Aut.Acc. Pte. PES RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='PES ÷ Aut.Acc. Pte. PES RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("PES ÷ Aut.Acc. Pte. PES RdD 400.html")



fig_RdT_PES = px.density_mapbox(df_220_RdT, lat='Latitude', lon='Longitude', z='Sol.Acc. en curso RdT 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Sol.Acc. en curso RdT 220.html")


fig_RdT_PES = px.density_mapbox(df_400_RdT, lat='Latitude', lon='Longitude', z='Sol.Acc. en curso RdT 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdT_PES.write_html("Sol.Acc. en curso RdT 400.html")


fig_RdD_PES = px.density_mapbox(df_220_RdD, lat='Latitude', lon='Longitude', z='Sol.Acc. en curso RdD 220',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Sol.Acc. en curso RdD 220.html")


fig_RdD_PES = px.density_mapbox(df_400_RdD, lat='Latitude', lon='Longitude', z='Sol.Acc. en curso RdD 400',
                        mapbox_style="stamen-terrain", center = dict(lat = 40.463667, lon = -3.74922 ), zoom = 5, radius = 20, hover_name = 'Nudo')

fig_RdD_PES.write_html("Sol.Acc. en curso RdD 400.html")





'''
# Load your DataFrame containing coordinates and values
# Replace 'your_data.csv' with the actual file path or load your data accordingly.
# Let's assume your DataFrame is named 'df' with columns 'latitude', 'longitude', and 'value'.
# df_aux = pd.read_excel(rootRoomba)

# Load the shapefile or GeoJSON file of Spain's boundaries
# Replace 'spain_shapefile.shp' with the path to your Spain boundaries shapefile or GeoJSON file.
spain_shape = gpd.read_file('C:\\Users\\GonzalodeCáceres\\GitHub\\roomba-REE\\gadm36_ESP_shp\\gadm36_ESP_0.shp')
spain_shape['Latitude'] = df_220_RdT['Latitude']
# Convert your DataFrame to a GeoDataFrame using latitude and longitude columns

gdf = gpd.GeoDataFrame(df_220_RdD, geometry=gpd.points_from_xy(df_220_RdD['Longitude'], df_220_RdD['Latitude']))

# Perform a spatial join to keep only the points within Spain's boundaries
gdf_within_spain = gpd.sjoin(gdf, spain_shape, how="inner", op="within")

# Normalize the values to map them to colors in the heatmap
min_value = gdf_within_spain['PES'].min()
max_value = gdf_within_spain['PES'].max()
gdf_within_spain['normalized_value'] = (gdf_within_spain['PES'] - min_value) / (max_value - min_value)

# Create the heatmap using matplotlib
fig, ax = plt.subplots(figsize=(12, 8))

# Plot Spain's boundaries
spain_shape.plot(ax=ax, color='white', edgecolor='black')

# Plot the heatmap
sc = ax.scatter(
    gdf_within_spain['Longitude'],
    gdf_within_spain['Latitude'],
    c=gdf_within_spain['normalized_value'],
    cmap='coolwarm',  # You can choose another colormap if you prefer.
    s=20,  # Adjust the size of the points.
    edgecolor='k',  # Add black edges to the points for better visibility.
)

# Add colorbar
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Normalized Value')

plt.title('Heatmap of Values within Spain')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()

'''