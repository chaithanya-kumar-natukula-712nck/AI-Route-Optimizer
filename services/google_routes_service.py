import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")



URL = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"


def get_route_matrix(locations):

    origins = []
    destinations = []

    for lat, lon in locations:

        point = {
            "waypoint": {
                "location": {
                    "latLng": {
                        "latitude": lat,
                        "longitude": lon
                    }
                }
            }
        }

        origins.append(point)
        destinations.append(point)

    headers = {
        "Content-Type": "application/json",

        "X-Goog-Api-Key": API_KEY,

        "X-Goog-FieldMask":
        "originIndex,destinationIndex,distanceMeters,duration,status"
    }

    body = {
        "origins": origins,

        "destinations": destinations,

        "travelMode": "DRIVE"
    }

    response = requests.post(
        URL,
        headers=headers,
        json=body
    )

    return response.json()



def extract_duration_matrix(
    response,
    num_locations
):

    matrix = [

        [0 for _ in range(num_locations)]

        for _ in range(num_locations)
    ]

    for item in response:

        origin = item["originIndex"]

        destination = item["destinationIndex"]

        duration_seconds = int(
            item["duration"].replace("s", "")
        )

        duration_minutes = round(
            duration_seconds / 60,
            2
        )

        matrix[origin][destination] = (
            duration_minutes
        )

    return matrix