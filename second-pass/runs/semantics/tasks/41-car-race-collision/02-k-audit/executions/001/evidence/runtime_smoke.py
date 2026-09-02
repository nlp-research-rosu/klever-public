def car_race_collision(n: int):
    return n * n


# Natural-domain empty/boundary/representative cases plus one probe from the
# stronger all-mathematical-Int formal claim.
assert car_race_collision(0) == 0
assert car_race_collision(1) == 1
assert car_race_collision(2) == 4
assert car_race_collision(10) == 100
assert car_race_collision(-3) == 9
