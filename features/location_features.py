from sklearn.cluster import KMeans

def generate_location_clusters(
    trips_df
):

    coords = trips_df[[
        "latitude",
        "longitude"
    ]]

    kmeans = KMeans(
        n_clusters=5,
        random_state=42
    )

    trips_df["area_cluster"] = (
        kmeans.fit_predict(coords)
    )

    return trips_df

def generate_location_features(
    trip_data
):

    area_cluster = int(

        trip_data["area_cluster"].mode()[0]
    )

    avg_latitude = round(

        trip_data["latitude"].mean(),

        6
    )

    avg_longitude = round(

        trip_data["longitude"].mean(),

        6
    )

    return {

        "area_cluster":
            area_cluster,

        "avg_latitude":
            avg_latitude,

        "avg_longitude":
            avg_longitude
    }