import pandas as pd

def generate_time_features(trip_data):

    trip_date = pd.to_datetime(
        trip_data.iloc[0]["date"]
    )

    arrival_time = pd.to_datetime(
        trip_data.iloc[0]["arrival_time"],
        format="%H:%M"
    )

    features = {

        "day_of_week":
            trip_date.day_name(),

        "month":
            trip_date.month,

        "quarter":
            trip_date.quarter,

        "hour":
            arrival_time.hour,

        "weekend_flag":
            int(trip_date.weekday() >= 5),

        "weekly_pattern":
            trip_date.isocalendar().week
    }

    return features