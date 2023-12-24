import math
# Fully chatGPT - https://chat.openai.com/share/d16a6c52-03b8-4f6e-b4b6-16e3c6eca6d0
def calculate_ways_to_win_optimized(time, distance):
    # Solving the quadratic equation: (time - x) * x > distance
    # which simplifies to: x^2 - time * x + distance < 0
    a = 1
    b = -time
    c = distance

    # Calculate the discriminant
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        # No real roots, means no solution
        return 0
    else:
        # Calculating the two roots of the quadratic equation
        root1 = (-b - math.sqrt(discriminant)) / (2 * a)
        root2 = (-b + math.sqrt(discriminant)) / (2 * a)

        # The range of button hold times that beat the record
        min_hold_time = max(0, math.ceil(root1))
        max_hold_time = min(time, math.floor(root2))

        if min_hold_time > max_hold_time:
            return 0
        else:
            return max_hold_time - min_hold_time + 1

# Single long race input
long_race_time = 49877895
long_race_distance = 356137815021882

# Calculating the number of ways to beat the record for the long race
long_race_result = calculate_ways_to_win_optimized(long_race_time, long_race_distance)
long_race_result
