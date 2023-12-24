def calculate_ways_to_win(races):
    total_ways = 1

    for race in races:
        time_allowed, current_record = race
        ways_to_win = 0

        for hold_time in range(time_allowed):
            travel_time = time_allowed - hold_time
            speed = hold_time
            distance = travel_time * speed
            if distance > current_record:
                ways_to_win += 1

        total_ways *= ways_to_win

    return total_ways

# New races data input
new_races = [(49, 356), (87, 1378), (78, 1502), (95, 1882)]

# Calculating the number of ways to beat the record for the new races
new_result = calculate_ways_to_win(new_races)
new_result