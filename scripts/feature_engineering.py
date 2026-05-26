import os
import sys
import pandas as pd

# =====================================================
# PROJECT ROOT
# =====================================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(project_root)

# =====================================================
# IMPORT FEATURE MODULES
# =====================================================

from features.time_features import (
    generate_time_features
)

from features.route_features import (
    generate_route_features
)

from features.driver_features import (
    generate_driver_features
)

from features.location_features import (
    generate_location_clusters,
    generate_location_features
)

from features.efficiency_features import (
    generate_efficiency_features
)

# =====================================================
# FILE PATHS
# =====================================================

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

optimized_path = os.path.join(
    project_root,
    "data",
    "optimized_routes.csv"
)

output_path = os.path.join(
    project_root,
    "data",
    "feature_dataset.csv"
)

# =====================================================
# LOAD DATA
# =====================================================

trips_df = pd.read_csv(
    trips_path
)

cache_df = pd.read_csv(
    cache_path
)

optimized_df = pd.read_csv(
    optimized_path
)

# =====================================================
# LOCATION CLUSTERING
# =====================================================

trips_df = generate_location_clusters(
    trips_df
)

# =====================================================
# GROUP TRIPS
# =====================================================

grouped_trips = trips_df.groupby(
    "trip_id"
)

# =====================================================
# FEATURE STORAGE
# =====================================================

feature_rows = []

# =====================================================
# MAIN LOOP
# =====================================================

for trip_id, trip_data in grouped_trips:

    print(f"Processing: {trip_id}")

    trip_data = trip_data.sort_values(
        by="stop_number"
    )

    # -------------------------------------------------
    # FEATURE MODULES
    # -------------------------------------------------

    time_features = (
        generate_time_features(
            trip_data
        )
    )

    route_features = (
        generate_route_features(
            trip_data,
            cache_df,
            optimized_df,
            trip_id
        )
    )

    driver_features = (
        generate_driver_features(
            trip_data,
            route_features,
            trips_df
        )
    )

    location_features = (
        generate_location_features(
            trip_data
        )
    )

    efficiency_features = (
        generate_efficiency_features(
            route_features
        )
    )

    # -------------------------------------------------
    # MERGE FEATURES
    # -------------------------------------------------

    feature_row = {

        "trip_id":
            trip_id,

        "driver_id":
            trip_data.iloc[0][
                "driver_id"
            ]
    }

    feature_row.update(
        time_features
    )

    feature_row.update(
        route_features
    )

    feature_row.update(
        driver_features
    )

    feature_row.update(
        location_features
    )

    feature_row.update(
        efficiency_features
    )

    feature_rows.append(
        feature_row
    )

# =====================================================
# FINAL DATAFRAME
# =====================================================

feature_df = pd.DataFrame(
    feature_rows
)

# =====================================================
# SAVE DATASET
# =====================================================

feature_df.to_csv(
    output_path,
    index=False
)

print("\nFeature Dataset Created!")

print(feature_df.head())