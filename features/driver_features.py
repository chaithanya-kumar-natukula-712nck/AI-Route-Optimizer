def generate_driver_features(
    trip_data,
    route_features,
    trips_df
):

    driver_id = trip_data.iloc[0][
        "driver_id"
    ]

    trip_date = trip_data.iloc[0][
        "date"
    ]

    total_distance = route_features[
        "total_distance_km"
    ]

    total_duration = route_features[
        "historical_travel_time"
    ]

    if total_duration > 0:

        average_speed = round(

            total_distance /

            (total_duration / 60),

            2
        )

    else:

        average_speed = 0

    daily_visits = len(

        trips_df[

            (trips_df["driver_id"] == driver_id) &

            (trips_df["date"] == trip_date)
        ]
    )

    optimized_duration = route_features[
        "optimized_duration_min"
    ]

    if total_duration > 0:

        past_route_efficiency = round(

            optimized_duration /

            total_duration,

            2
        )

    else:

        past_route_efficiency = 1

    return {

        "average_speed":
            average_speed,

        "daily_visits":
            daily_visits,

        "past_route_efficiency":
            past_route_efficiency
    }