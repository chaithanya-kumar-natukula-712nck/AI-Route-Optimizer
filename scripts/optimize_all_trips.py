import pandas as pd
import os
import sys



project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(project_root)

from services.route_optimizer import (
    nearest_neighbor_optimizer
)

from services.matrix_builder import (
    build_duration_matrix,build_distance_matrix
)


trips_path = os.path.join(
    project_root,
    "data",
    "historical_trips.csv"
)

cache_path = os.path.join(
    project_root,
    "data",
    "route_cache.csv"
)

trips_df = pd.read_csv(trips_path)

cache_df = pd.read_csv(cache_path)

grouped_trips = trips_df.groupby(
    "trip_id"
)

optimized_rows = []



for trip_id, trip_data in grouped_trips:

    print(f"\nOptimizing Trip: {trip_id}")

    # -----------------------------------
    # SORT ORIGINAL ROUTE
    # -----------------------------------

    trip_data = trip_data.sort_values(
        by="stop_number"
    )

    # -----------------------------------
    # EXTRACT IDS/NAMES
    # -----------------------------------

    location_ids = list(
        trip_data["location_id"]
    )

    store_names = list(
        trip_data["store_name"]
    )

    # -----------------------------------
    # BUILD MATRIX
    # -----------------------------------

    duration_matrix = build_duration_matrix(
        location_ids,
        cache_df
    )

    distance_matrix = build_distance_matrix(
    location_ids,
    cache_df
    )
    # -----------------------------------
    # OPTIMIZE
    # -----------------------------------

    result = nearest_neighbor_optimizer(
        duration_matrix
    )

    optimized_indexes = result[
        "optimized_route"
    ]

    optimized_distance = 0

    for i in range(
        len(optimized_indexes) - 1
    ):

        current_stop = optimized_indexes[i]

        next_stop = optimized_indexes[i + 1]

        optimized_distance += (

            distance_matrix[
                current_stop
            ][
                next_stop
            ]
        )

    optimized_distance = round(
        optimized_distance,
        2
    )


    optimized_route = [

        store_names[i]

        for i in optimized_indexes
    ]

    optimized_route_string = (
        " → ".join(optimized_route)
    )

    optimized_rows.append({

        "trip_id": trip_id,

        "optimized_route":
            optimized_route_string,
        
        "optimized_distance_km":
            optimized_distance,

        "optimized_duration_min":
            result[
                "total_duration_min"
            ]
    })

    optimized_df = pd.DataFrame(
    optimized_rows
)

output_path = os.path.join(
    project_root,
    "data",
    "optimized_routes.csv"
)

optimized_df.to_csv(
    output_path,
    index=False
)

print("\nOptimization Complete!")

print(optimized_df.head())