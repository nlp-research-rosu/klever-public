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
    index1 = planets.index(planet1)
    index2 = planets.index(planet2)
    if index1 < index2:
        return planets[index1 + 1:index2]
    return planets[index2 + 1:index1]


assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")
assert bf("Earth", "Mercury") == ("Venus",)
assert bf("Mercury", "Uranus") == (
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
)
assert bf("Mercury", "Venus") == ()
assert bf("Venus", "Mercury") == ()
assert bf("Earth", "Earth") == ()
assert bf("Mercury", "Neptune") == (
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
)
assert bf("Neptune", "Mercury") == (
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
)
assert bf("", "Earth") == ()
assert bf("Earth", "") == ()
assert bf("Pluto", "Pluto") == ()
assert bf("Neptune ", "Neptune") == ()
