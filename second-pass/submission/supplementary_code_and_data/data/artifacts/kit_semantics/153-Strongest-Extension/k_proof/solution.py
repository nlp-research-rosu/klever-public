def Strongest_Extension(class_name, extensions):
    strongest = ""
    best_strength = None
    extension = ""
    character = ""

    for extension in extensions:
        strength = 0

        for character in extension:
            if character.isupper():
                strength += 1
            elif character.islower():
                strength -= 1

        if best_strength is None or strength > best_strength:
            strongest = extension
            best_strength = strength

    return class_name + "." + strongest
