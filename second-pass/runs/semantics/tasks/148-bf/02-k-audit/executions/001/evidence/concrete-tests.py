def bf(planet1, planet2):
    planets = (
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
    )
    if planet1 not in planets or planet2 not in planets:
        return ()
    first = planets.index(planet1)
    second = planets.index(planet2)
    if first < second:
        return planets[first + 1:second]
    return planets[second + 1:first]


assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")
assert bf("Earth", "Mercury") == ("Venus",)
assert bf("Mercury", "Uranus") == (
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
)
assert bf("Mercury", "Mercury") == ()
assert bf("Neptune", "Neptune") == ()
assert bf("Mercury", "Venus") == ()
assert bf("Venus", "Mercury") == ()
assert bf("", "Earth") == ()
assert bf("Earth", "") == ()
assert bf("mercury", "Mercury") == ()
