def bf(planet1, planet2):
    if planet1 == "Mercury":
        if planet2 == "Earth":
            return ("Venus",)
        if planet2 == "Mars":
            return ("Venus", "Earth")
        if planet2 == "Jupiter":
            return ("Venus", "Earth", "Mars")
        if planet2 == "Saturn":
            return ("Venus", "Earth", "Mars", "Jupiter")
        if planet2 == "Uranus":
            return ("Venus", "Earth", "Mars", "Jupiter", "Saturn")
        if planet2 == "Neptune":
            return ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        return ()

    if planet1 == "Venus":
        if planet2 == "Mars":
            return ("Earth",)
        if planet2 == "Jupiter":
            return ("Earth", "Mars")
        if planet2 == "Saturn":
            return ("Earth", "Mars", "Jupiter")
        if planet2 == "Uranus":
            return ("Earth", "Mars", "Jupiter", "Saturn")
        if planet2 == "Neptune":
            return ("Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        return ()

    if planet1 == "Earth":
        if planet2 == "Mercury":
            return ("Venus",)
        if planet2 == "Jupiter":
            return ("Mars",)
        if planet2 == "Saturn":
            return ("Mars", "Jupiter")
        if planet2 == "Uranus":
            return ("Mars", "Jupiter", "Saturn")
        if planet2 == "Neptune":
            return ("Mars", "Jupiter", "Saturn", "Uranus")
        return ()

    if planet1 == "Mars":
        if planet2 == "Mercury":
            return ("Venus", "Earth")
        if planet2 == "Venus":
            return ("Earth",)
        if planet2 == "Saturn":
            return ("Jupiter",)
        if planet2 == "Uranus":
            return ("Jupiter", "Saturn")
        if planet2 == "Neptune":
            return ("Jupiter", "Saturn", "Uranus")
        return ()

    if planet1 == "Jupiter":
        if planet2 == "Mercury":
            return ("Venus", "Earth", "Mars")
        if planet2 == "Venus":
            return ("Earth", "Mars")
        if planet2 == "Earth":
            return ("Mars",)
        if planet2 == "Uranus":
            return ("Saturn",)
        if planet2 == "Neptune":
            return ("Saturn", "Uranus")
        return ()

    if planet1 == "Saturn":
        if planet2 == "Mercury":
            return ("Venus", "Earth", "Mars", "Jupiter")
        if planet2 == "Venus":
            return ("Earth", "Mars", "Jupiter")
        if planet2 == "Earth":
            return ("Mars", "Jupiter")
        if planet2 == "Mars":
            return ("Jupiter",)
        if planet2 == "Neptune":
            return ("Uranus",)
        return ()

    if planet1 == "Uranus":
        if planet2 == "Mercury":
            return ("Venus", "Earth", "Mars", "Jupiter", "Saturn")
        if planet2 == "Venus":
            return ("Earth", "Mars", "Jupiter", "Saturn")
        if planet2 == "Earth":
            return ("Mars", "Jupiter", "Saturn")
        if planet2 == "Mars":
            return ("Jupiter", "Saturn")
        if planet2 == "Jupiter":
            return ("Saturn",)
        return ()

    if planet1 == "Neptune":
        if planet2 == "Mercury":
            return ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        if planet2 == "Venus":
            return ("Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        if planet2 == "Earth":
            return ("Mars", "Jupiter", "Saturn", "Uranus")
        if planet2 == "Mars":
            return ("Jupiter", "Saturn", "Uranus")
        if planet2 == "Jupiter":
            return ("Saturn", "Uranus")
        if planet2 == "Saturn":
            return ("Uranus",)
        return ()

    return ()
