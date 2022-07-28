import pandas as pd
import numpy as np
import folium
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from math import cos, asin, sqrt, pi
from folium.plugins import HeatMap
from folium import plugins


lat = 49.284808779798745
lon = -123.12244539679432

def get_similar(df):
    df['amenity'] = df['amenity'].replace(['parking_entrance'], 'parking')
    df['amenity'] = df['amenity'].replace(['pub'], 'bar')
    df['amenity'] = df['amenity'].replace(['childcare'], 'kindergarten')
    df['amenity'] = df['amenity'].replace(['nightclub'], 'bar')
    df['amenity'] = df['amenity'].replace(['gambling'], 'casino')
    df['amenity'] = df['amenity'].replace(['atm;bank'], 'bank')
    df['amenity'] = df['amenity'].replace(['motorcycle_parking'], 'parking')
    df['amenity'] = df['amenity'].replace(['drinking_water'], 'fountain')
    df['amenity'] = df['amenity'].replace(['doctors'], 'hospital')
    df['amenity'] = df['amenity'].replace(['storage'], 'storage_rental')
    df['amenity'] = df['amenity'].replace(['internet_cafe'], 'cafe')
    df['amenity'] = df['amenity'].replace(['chiropractor'], 'hospital')
    df['amenity'] = df['amenity'].replace(['post_depot'], 'post_office')
    df['amenity'] = df['amenity'].replace(['Pharmacy'], 'pharmacy')
    return df

def handling_missingname(file):
    # Handeling missing restaurant name
    file = file.dropna(subset=['name']).reset_index(drop = True)
    return file 

def sort_chain(data):
    new_data = data[data.duplicated(subset=['name'])==True].reset_index(drop = True)
    return new_data

def build_map():
    newmap = folium.Map(location=[lat, lon], zoom_start=12)
    return newmap

def map_heat(map,location):
    map.add_child(plugins.HeatMap(location,blur=28))

def map_scatter_plot(file):
    # read file
    data = pd.read_csv(file, index_col=0)

    vanmap = build_map()

    # add every data point to the map
    for index, row in data.iterrows():
        folium.Circle(radius= 5,color = 'red',location=[row['lat'], row['lon']]).add_to(vanmap)

    return vanmap



def main():
    vanmap = build_map()
    
    raw_data= pd.read_json("amenities-vancouver.json.gz", lines=True)
    raw_data = raw_data[raw_data['name'].notna()]
    data = get_similar(raw_data)
    filt = ['restaurant']
    restaurant = data[data['amenity'].isin(filt) == True]

    restaurant = handling_missingname(restaurant)
    
    # get all restaurant in vancouver
    restaurant.to_csv('all_restaurant.csv')
    all_restaurant = pd.read_csv("all_restaurant.csv")
    all_restaurant.drop_duplicates()
    all_restaurant = all_restaurant[['lat','lon','name']]
    
    chain_restaurant = sort_chain(all_restaurant)
    chain_restaurant.to_csv('chain_restaurant.csv')
    chain_restaurant = pd.read_csv("chain_restaurant.csv")
    chain_restaurant = chain_restaurant[['lat','lon','name']] 
    
    location = []
    
    for index,row in all_restaurant.iterrows():
        location.append([row['lat'], row['lon']])
    map_heat(vanmap,location)
    
    vanmap.save(outfile= "all_restaurant_heat.html")
    all_resturant_map = map_scatter_plot("all_restaurant.csv")
    
    all_resturant_map.save(outfile= "all_restaurant_plot.html")
    for index,row in chain_restaurant.iterrows():
        location.append([row['lat'], row['lon']])
    map_heat(vanmap,location)

    vanmap.save(outfile= "chain_restaurant_heat.html")
    chain_resturant_map = map_scatter_plot("chain_restaurant.csv")
    
    chain_resturant_map.save(outfile= "chain_restaurant_plot.html")
    
if __name__=='__main__':
    main()
   