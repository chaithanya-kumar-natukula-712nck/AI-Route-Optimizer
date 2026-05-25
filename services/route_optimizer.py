def nearest_neighbor_optimizer(
    duration_matrix
):

    num_locations = len(duration_matrix)

    visited = [False] * num_locations

    # Start from first location
    current = 0

    route = [current]

    visited[current] = True

    total_duration = 0

    for _ in range(num_locations - 1):

        nearest = None

        nearest_duration = float("inf")

        for next_location in range(num_locations):

            if not visited[next_location]:

                duration = duration_matrix[
                    current
                ][next_location]

                if duration < nearest_duration:

                    nearest_duration = duration

                    nearest = next_location

        route.append(nearest)

        visited[nearest] = True

        total_duration += nearest_duration

        current = nearest

    return {

        "optimized_route": route,

        "total_duration_min": round(
            total_duration,
            2
        )
    }