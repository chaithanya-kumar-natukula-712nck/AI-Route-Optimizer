def build_duration_matrix(
    location_ids,
    cache_df
):

    n = len(location_ids)

    matrix = [

        [0 for _ in range(n)]

        for _ in range(n)
    ]

    for i in range(n):

        for j in range(n):

            if i == j:
                continue

            origin = location_ids[i]

            destination = location_ids[j]

            match = cache_df[

                (cache_df["origin_id"] == origin) &

                (cache_df["destination_id"] == destination)
            ]

            if len(match) > 0:

                duration = match.iloc[0][
                    "duration_minutes"
                ]

                matrix[i][j] = duration

            else:

                matrix[i][j] = 9999

    return matrix