import pandas as pd
import numpy as np

import random
random.seed(42)

from datetime import datetime, timedelta

# Number of locations
NUM_LOCATIONS = 60

# Hyderabad coordinate boundaries
LAT_MIN = 17.20
LAT_MAX = 17.60

LON_MIN = 78.20
LON_MAX = 78.70

zones = ["North", "South", "East", "West", "Central"]

# 1. Define the 60 unique Hyderabad store names
hyderabad_stores = [
    "Ratnadeep Supermarket", "Vijetha Supermarket", "Heritage Fresh", "D-Mart Begumpet", "Reliance Smart Jubilee",
    "Ghanshyam Supermarket", "Q-Mart Gachibowli", "Nature's Basket", "Spencer's Retail", "Metro Cash & Carry",
    "Inorbit Mall Shoppers Stop", "GVK One Lifestyle", "Forum Sujana Zara", "Sarath City Capital H&M", "Hyderabad Central",
    "Neeru's Emporio", "Mebaz Banjara Hills", "Kalanikethan Kukatpally", "South India Shopping Mall", "Chennai Shopping Mall",
    "Bajaj Electronics", "Croma Jubilee Hills", "Reliance Digital", "Darpan Furnishings", "IKEA Hyderabad",
    "Fabindia Gachibowli", "Chutneys Restaurant", "Paradise Biryani Secunderabad", "Bawarchi RTC X Roads", "Shah Ghouse Gachibowli",
    "Cafe Niloufer", "Karachi Bakery", "Pista House", "Concu Jubilee Hills", "Roastery Coffee House",
    "Aroma Boutique", "Alankrita Boutique", "MedPlus Madhapur", "Apollo Pharmacy", "Apollo Health City",
    "Kimmee's Salon", "Green Trends", "Naturals Salon", "Page 3 Luxury Salon", "Lakme Salon",
    "Crossword Bookstore", "Himalaya Book World", "Decathlon Madhapur", "Wildcraft Store", "Nike Exclusive Store",
    "Adidas Originals", "Puma Store", "Bata Shoe Store", "Metro Shoes", "Khazana Jewellers",
    "Malabar Gold & Diamonds", "Joyalukkas", "Jos Alukkas", "GRT Jewellers", "Lalitha Jewellery"
]

def generate_locations(num_locations, lat_min, lat_max, lon_min, lon_max,
                       zones_list):
    # random.seed(42)
    locations_list = []
    for i in range(1, num_locations + 1):
        location = {
            "location_id": f"L{i}",
            "store_name": hyderabad_stores[i-1],
            "latitude": round(random.uniform(lat_min, lat_max), 6),
            "longitude": round(random.uniform(lon_min, lon_max), 6),
            "zone": random.choice(zones_list),
        }
        locations_list.append(location)
    return locations_list

locations = generate_locations(
    NUM_LOCATIONS, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, zones
)


for i in range(len(locations)):
  print(locations[i])

# Convert to dataframe
locations_df = pd.DataFrame(locations)

# Save CSV
locations_df.to_csv("data/locations.csv", index=False)

print("Locations dataset generated successfully!")