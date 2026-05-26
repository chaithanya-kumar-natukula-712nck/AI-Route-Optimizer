def generate_efficiency_features(
    route_features
):

    stop_count = route_features[
        "stop_count"
    ]

    total_distance = route_features[
        "total_distance_km"
    ]

    total_duration = route_features[
        "historical_travel_time"
    ]

    if stop_count > 0:

        distance_per_stop = round(

            total_distance /

            stop_count,

            2
        )

        duration_per_stop = round(

            total_duration /

            stop_count,

            2
        )

    else:

        distance_per_stop = 0

        duration_per_stop = 0

    return {

        "distance_per_stop":
            distance_per_stop,

        "duration_per_stop":
            duration_per_stop
    }