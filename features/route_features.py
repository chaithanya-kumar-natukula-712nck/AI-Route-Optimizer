def generate_route_features(
    trip_data,
    cache_df,
    optimized_df,
    trip_id
):

    location_ids = list(
        trip_data["location_id"]
    )

    total_distance_meters = 0

    historical_travel_time = 0

    for i in range(
        len(location_ids) - 1
    ):

        origin = location_ids[i]

        destination = location_ids[i + 1]

        match = cache_df[

            (cache_df["origin_id"] == origin) &

            (cache_df["destination_id"] == destination)
        ]

        if len(match) > 0:

            total_distance_meters += (
                match.iloc[0]["distance_meters"]
            )

            historical_travel_time += (
                match.iloc[0]["duration_minutes"]
            )

    total_distance_km = round(
        total_distance_meters / 1000,
        2
    )

    stop_count = len(location_ids)

    optimized_match = optimized_df[
        optimized_df["trip_id"] == trip_id
    ]

    if len(optimized_match) > 0:

        optimized_duration = (
            optimized_match.iloc[0][
                "optimized_duration_min"
            ]
        )

        optimized_distance = (
            optimized_match.iloc[0][
                "optimized_distance_km"
            ]
        )

    else:

        optimized_duration = 0
        optimized_distance = 0

    return {

        "total_distance_km":
            total_distance_km,

        "historical_travel_time":
            historical_travel_time,

        "stop_count":
            stop_count,

        "optimized_duration_min":
            optimized_duration,

        "optimized_distance_km":
            optimized_distance
    }