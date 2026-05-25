import sys
import os

# Get project root
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# Add project root to Python path
sys.path.append(project_root)

import pandas as pd

from services.google_routes_service import *
from services.route_optimizer import *


trips_path = os.path.join(
    project_root,
    "data",
    "historical_trips.csv"
)

trips_df = pd.read_csv(trips_path)


print(trips_df.head())



# Cache file path
CACHE_FILE = os.path.join(
    project_root,
    "data",
    "route_cache.csv"
)

# Load existing cache if exists
if os.path.exists(CACHE_FILE):

    cache_df = pd.read_csv(CACHE_FILE)

else:

    cache_df = pd.DataFrame(columns=[

        "origin_id",
        "destination_id",

        "origin_store",
        "destination_store",

        "distance_meters",

        "duration_seconds",

        "duration_minutes"
    ])

print("Trips Loaded:", len(trips_df))
print("Cached Routes:", len(cache_df))

# grouped_trips = trips_df.groupby("trip_id")



cached_routes = set(

    zip(
        cache_df["origin_id"],
        cache_df["destination_id"]
    )
)

def is_route_cached(
    origin_id,
    destination_id
):

    return (
        origin_id,
        destination_id
    ) in cached_routes




# for trip_id, trip_data in grouped_trips:
#     locations = list(

#         zip(
#             trip_data["latitude"],
#             trip_data["longitude"]
#         )
#     )
#     location_ids = list(
#         trip_data["location_id"]
#     )
#     print(location_ids)

#     all_new_rows = []



# for trip_id, trip_data in grouped_trips:

#     print(f"\nProcessing Trip: {trip_id}")

#     # -----------------------------------
#     # SORT STOPS
#     # -----------------------------------

#     trip_data = trip_data.sort_values(
#         by="stop_number"
#     )

#     # -----------------------------------
#     # EXTRACT LOCATIONS
#     # -----------------------------------

#     locations = list(

#         zip(
#             trip_data["latitude"],
#             trip_data["longitude"]
#         )
#     )

#     # -----------------------------------
#     # STORE IDS/NAMES
#     # -----------------------------------

#     location_ids = list(
#         trip_data["location_id"]
#     )

#     store_names = list(
#         trip_data["store_name"]
#     )

#     # -----------------------------------
#     # CHECK IF ALL ROUTES EXIST
#     # -----------------------------------

#     missing_routes = False

#     n = len(location_ids)

#     for i in range(n):

#         for j in range(n):

#             if i == j:
#                 continue

#             if not is_route_cached(

#                 location_ids[i],
#                 location_ids[j]
#             ):

#                 missing_routes = True
#                 break

#     # -----------------------------------
#     # SKIP API IF FULLY CACHED
#     # -----------------------------------

#     if not missing_routes:

#         print("Already Cached")
#         continue

#     # -----------------------------------
#     # GOOGLE API CALL
#     # -----------------------------------

#     print("Calling Google API...")

#     response = get_route_matrix(
#         locations
#     )

#     # -----------------------------------
#     # STORE MATRIX PAIRS
#     # -----------------------------------

#     for item in response:

#         # -----------------------------------
#         # VALIDATE RESPONSE ITEM
#         # -----------------------------------

#         if "originIndex" not in item:
#             continue

#         if "destinationIndex" not in item:
#             continue

#         if "distanceMeters" not in item:
#             continue

#         if "duration" not in item:
#             continue

#         origin_index = item[
#             "originIndex"
#         ]

#         destination_index = item[
#             "destinationIndex"
#         ]

#         # Skip same-node routes
#         if origin_index == destination_index:
#             continue

#         origin_id = location_ids[
#             origin_index
#         ]

#         destination_id = location_ids[
#             destination_index
#         ]

#         # Skip already cached
#         if is_route_cached(
#             origin_id,
#             destination_id
#         ):
#             continue

#         try:

#             distance_meters = item[
#                 "distanceMeters"
#             ]

#             duration_seconds = int(
#                 item["duration"].replace(
#                     "s",
#                     ""
#                 )
#             )

#             duration_minutes = round(
#                 duration_seconds / 60,
#                 2
#             )

#             row = {

#                 "origin_id":
#                     origin_id,

#                 "destination_id":
#                     destination_id,

#                 "origin_store":
#                     store_names[origin_index],

#                 "destination_store":
#                     store_names[destination_index],

#                 "distance_meters":
#                     distance_meters,

#                 "duration_seconds":
#                     duration_seconds,

#                 "duration_minutes":
#                     duration_minutes
#             }

#             all_new_rows.append(row)
#             cached_routes.add(
#                 (
#                     origin_id,
#                     destination_id
#                 )
#             )

#         except Exception as e:

#             print(
#                 f"Failed pair "
#                 f"{origin_id} → {destination_id}"
#             )

#             print(e)


# if len(all_new_rows) > 0:

#     new_cache_df = pd.DataFrame(
#         all_new_rows
#     )

#     cache_df = pd.concat(

#         [cache_df, new_cache_df],

#         ignore_index=True
#     )
#     all_new_rows=[]
#     cache_df.to_csv(
#         CACHE_FILE,
#         index=False
#     )

# print("\nRoute cache updated!")

# print(
#     f"Total cached routes: "
#     f"{len(cache_df)}"
# )


trip_ids = trips_df["trip_id"].unique()

print("Total Trips:", len(trip_ids))

batch_size = 10



for start in range(
    0,
    len(trip_ids),
    batch_size
):

    print("\n" + "=" * 50)

    print(
        f"Processing Batch: "
        f"{start} → {start + batch_size}"
    )

    print("=" * 50)

    # -----------------------------------
    # TAKE 10 TRIPS
    # -----------------------------------

    batch_trip_ids = trip_ids[
        start:start + batch_size
    ]

    # -----------------------------------
    # FILTER DATAFRAME
    # -----------------------------------

    batch_df = trips_df[

        trips_df["trip_id"].isin(
            batch_trip_ids
        )
    ]

    # -----------------------------------
    # GROUP TRIPS
    # -----------------------------------

    grouped_trips = batch_df.groupby(
        "trip_id"
    )

    # -----------------------------------
    # LOAD FRESH CACHE
    # -----------------------------------

    cache_df = pd.read_csv(
        CACHE_FILE
    )

    # -----------------------------------
    # BUILD CACHE SET
    # -----------------------------------

    cached_routes = set(

        zip(
            cache_df["origin_id"],
            cache_df["destination_id"]
        )
    )

    # -----------------------------------
    # STORE NEW ROWS
    # -----------------------------------

    all_new_rows = []

    # ===================================
    # PROCESS TRIPS
    # ===================================

    for trip_id, trip_data in grouped_trips:

        print(f"\nTrip: {trip_id}")

        trip_data = trip_data.sort_values(
            by="stop_number"
        )

        # -------------------------------
        # EXTRACT LOCATIONS
        # -------------------------------

        locations = list(

            zip(
                trip_data["latitude"],
                trip_data["longitude"]
            )
        )

        location_ids = list(
            trip_data["location_id"]
        )

        store_names = list(
            trip_data["store_name"]
        )

        # -------------------------------
        # GOOGLE API CALL
        # -------------------------------

        response = get_route_matrix(
            locations
        )

        # -------------------------------
        # STORE ROUTES
        # -------------------------------

        for item in response:

            origin_index = item.get(
                "originIndex"
            )

            destination_index = item.get(
                "destinationIndex"
            )

            distance_meters = item.get(
                "distanceMeters"
            )

            duration = item.get(
                "duration"
            )

            # ---------------------------
            # VALIDATION
            # ---------------------------

            if (
                origin_index is None or
                destination_index is None or
                distance_meters is None or
                duration is None
            ):
                continue

            # Skip self routes
            if origin_index == destination_index:
                continue

            origin_id = location_ids[
                origin_index
            ]

            destination_id = location_ids[
                destination_index
            ]

            # ---------------------------
            # CACHE CHECK
            # ---------------------------

            route_key = (
                origin_id,
                destination_id
            )

            if route_key in cached_routes:
                continue

            duration_seconds = int(
                duration.replace("s", "")
            )

            duration_minutes = round(
                duration_seconds / 60,
                2
            )

            row = {

                "origin_id":
                    origin_id,

                "destination_id":
                    destination_id,

                "origin_store":
                    store_names[origin_index],

                "destination_store":
                    store_names[destination_index],

                "distance_meters":
                    distance_meters,

                "duration_seconds":
                    duration_seconds,

                "duration_minutes":
                    duration_minutes
            }

            all_new_rows.append(row)

            # ---------------------------
            # ADD TO SET IMMEDIATELY
            # ---------------------------

            cached_routes.add(route_key)

    # ===================================
    # SAVE BATCH CACHE
    # ===================================

    if len(all_new_rows) > 0:

        new_cache_df = pd.DataFrame(
            all_new_rows
        )

        cache_df = pd.concat(

            [cache_df, new_cache_df],

            ignore_index=True
        )

        cache_df.to_csv(
            CACHE_FILE,
            index=False
        )

        print(
            f"\nSaved "
            f"{len(all_new_rows)} new routes"
        )

    else:

        print("\nNo new routes found")