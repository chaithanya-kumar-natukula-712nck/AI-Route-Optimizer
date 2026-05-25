import pandas as pd
import random
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2



# Load locations dataset
locations_df = pd.read_csv("data/locations.csv")

# Parameters
NUM_DRIVERS = 12
NUM_DAYS = 40

drivers = [f"D{i}" for i in range(1, NUM_DRIVERS + 1)]

# Date range
start_date = datetime(2026, 4, 1)

AVG_SPEED_KMPH = 40


def haversine_distance(selected_locations, i):

    # Last stop has no next location
    if i >= len(selected_locations) - 1:
        return 0

    current_location = selected_locations.iloc[i]

    next_location = selected_locations.iloc[i + 1]

    # Earth radius in KM
    R = 6371

    # Convert coordinates to radians
    lat1, lon1, lat2, lon2 = map(
        radians,
        [
            current_location["latitude"],
            current_location["longitude"],
            next_location["latitude"],
            next_location["longitude"]
        ]
    )

    # Coordinate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c

    return round(distance_km, 2)


def generate_trip_stops(
    selected_locations,
    current_time,
    driver,
    trip_id,
    current_date
):
    random.seed(trip_id)

    records = []

    stop_number = 1

    for i, location in selected_locations.iterrows():

        visit_duration = random.randint(10, 40)

        distance_km=haversine_distance(selected_locations,i)


        travel_time_min = (
            distance_km / AVG_SPEED_KMPH
        ) * 60

        travel_time_min = round(travel_time_min, 1)

        trip_record = {

            "trip_id": trip_id,
            "driver_id": driver,
            "date": current_date.date(),

            "stop_number": stop_number,

            "location_id": location["location_id"],
            "store_name": location["store_name"],

            "latitude": location["latitude"],
            "longitude": location["longitude"],

            "arrival_time": current_time.strftime("%H:%M"),

            "visit_duration_min": visit_duration,

            "distance_to_next_km": distance_km,

            "travel_time_to_next_min": travel_time_min,
        }
        records.append(trip_record)

        current_time += timedelta(
            minutes=(
                visit_duration
                + travel_time_min
                + random.randint(5, 15)
            )
        )

        stop_number += 1

    return records


trip_records = []

trip_id = 1

for day in range(NUM_DAYS):

    current_date = start_date + timedelta(days=day)
    random.seed(day)

    for driver in drivers:

        num_stops = random.randint(3, 7)

        selected_locations = (
            locations_df.sample(num_stops,random_state=day+num_stops)
            .reset_index(drop=True)
        )

        current_time = datetime.combine(
            current_date.date(),
            datetime.strptime(
                f"{random.randint(8,10)}:{random.choice([0,15,30,45])}",
                "%H:%M"
            ).time()
        )

        driver_trip_records = generate_trip_stops(
            selected_locations,
            current_time,
            driver,
            trip_id,
            current_date
        )

        trip_records.extend(driver_trip_records)

        trip_id += 1

print(len(trip_records))

for i in range(20):
  print(trip_records[i])


# Create dataframe
trips_df = pd.DataFrame(trip_records)

# Save dataset
trips_df.to_csv("data/historical_trips.csv", index=False)

print("Historical trips dataset generated successfully!")