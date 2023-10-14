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
import streamlit as st
import requests
from geopy.geocoders import Nominatim
import utm
global zoneVal
import geopandas as gpd

st.cache_data
def locator_json(df_stateless, df_statefull, df_stateless_countiless, df_full, rootFileShp):
    # Check where the point lays within the polygons

    # Get the lat long of the nodes into a geodataframe
    gdf_points_nodes = gpd.GeoDataFrame(df_stateless_countiless, geometry = gpd.points_from_xy(df_stateless_countiless.Longitude, df_stateless_countiless.Latitude), crs = 'EPSG:4236')

    # Read the shapefile into a GeoDataFrame
    gdf_polygons_states = gpd.read_file(rootFileShp)
    gdf_polygons_states = gdf_polygons_states.to_crs('EPSG:4236')

    gdf_polygons_states = gdf_polygons_states[['NAME', 'STUSPS', 'geometry']]

    # Perform a spatial join to identify points within polygons
    spatial_join_gdf = gpd.sjoin(gdf_points_nodes, gdf_polygons_states, op='within', how='inner')

    spatial_join_gdf = spatial_join_gdf[['Node', 'ISO', 'Period From', 'Latitude', 'Longitude', 'Average LMP', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average Max - Min Daily LMP Spread', 'LMP negative hours', 'Price type', 'NAME', 'STUSPS']]

    spatial_join_gdf.rename(columns = {'STUSPS': 'State', 'NAME':'County'}, inplace = True)

    spatial_join_gdf = spatial_join_gdf[['Node', 'ISO', 'State', 'County','Period From', 'Latitude', 'Longitude', 'Average LMP', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average Max - Min Daily LMP Spread', 'LMP negative hours', 'Price type']]

    df_stateless = pd.DataFrame(spatial_join_gdf)

    df = pd.concat([df_full, df_stateless])

    flag_adequacy= True

    # st.write(df)

    return df, flag_adequacy


# %%
st.cache_data
def html_maker(df):

    df_copy = df.copy()

    df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']] = df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']].astype(str) + ' $/MWh'

    centroid = [df_copy['Latitude'].sum(), df_copy['Longitude'].sum()]/df_copy['Latitude'].count()
    
    html_made = px.density_mapbox(df_copy, lat='Latitude', lon='Longitude', z='Average Max - Min Daily LMP Spread', mapbox_style="stamen-terrain", center = dict(lat = centroid[0], lon = centroid[1]), zoom = 2.3, radius = 8, hover_name = 'Node')

    return html_made

st.cache_data
def html_display_spread(df):

    df_copy = df.copy()

    df_copy['Average Max - Min Daily LMP  Spread'] = df_copy['Average Max - Min Daily LMP Spread'] 
    
    df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']] = df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']].astype(str) + ' $/MWh'
    


    centroid = [df_copy['Latitude'].sum(), df_copy['Longitude'].sum()]/df_copy['Latitude'].count()

    html_show = px.density_mapbox(df_copy, lat='Latitude', lon='Longitude', z='Average Max - Min Daily LMP  Spread', mapbox_style="open-street-map", center = dict(lat = centroid[0], lon = centroid[1] ), zoom = 3, radius = 8, hover_name= 'Node', height = 800, width = 1800, hover_data = ['State', 'Period From', 'ISO','Average LMP', 'Average Max - Min Daily LMP Spread'], color_continuous_scale=px.colors.sequential.Magma)

    return html_show

st.cache_data
def html_display_indexed(df):

    df_copy = df.copy()

    df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']] = df_copy[['Average Max - Min Daily LMP Spread', 'Average Min Daily LMP', 'Average Max Daily LMP', 'Average LMP']].astype(str) + ' $/MWh'
    
    centroid = [df_copy['Latitude'].sum(), df_copy['Longitude'].sum()]/df_copy['Latitude'].count()

    html_show = px.scatter_mapbox(df_copy, lat='Latitude', lon='Longitude', mapbox_style="open-street-map", center = dict(lat = centroid[0], lon = centroid[1] ), zoom = 3, hover_name= 'Node', height = 800, width = 1800, hover_data = ['State', 'Period From', 'ISO','Average LMP', 'Average Max - Min Daily LMP Spread'], color_continuous_scale=px.colors.sequential.Turbo, color='Heat map scale')
    
    return html_show

#@todo - Que haga zoom sobre la parte del mapa que nos interesa.
'''
def zoom(df):

    # Find the minimum and maximum latitude and longitude
    min_lat = df['Latitude'].min()
    max_lat = df['Latitude'].max()
    min_lon = df['Longitude'].min()
    max_lon = df['Longitude'].max()

    # Define the four corners of the square
    corners = [(min_lat, min_lon),  # Minimum latitude, minimum longitude
           (max_lat, max_lon),  # Maximum latitude, maximum longitude
           (min_lat, max_lon),  # Minimum latitude, maximum longitude
           (max_lat, min_lon)]  # Maximum latitude, minimum longitude
 
           
    # https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
    zooming = 11.5 - np.log(max(abs(),abs())*111)

    return zooming



'''

st.cache_data
def kml_maker(df):
    pass

