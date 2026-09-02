def Strongest_Extension(class_name, extensions):
    strongest = extensions[0]
    strongest_strength = 0
    for character in strongest:
        if character.isupper():
            strongest_strength += 1
        if character.islower():
            strongest_strength -= 1

    for extension in extensions[1:]:
        extension_strength = 0
        for character in extension:
            if character.isupper():
                extension_strength += 1
            if character.islower():
                extension_strength -= 1
        if extension_strength > strongest_strength:
            strongest = extension
            strongest_strength = extension_strength

    return class_name + "." + strongest
