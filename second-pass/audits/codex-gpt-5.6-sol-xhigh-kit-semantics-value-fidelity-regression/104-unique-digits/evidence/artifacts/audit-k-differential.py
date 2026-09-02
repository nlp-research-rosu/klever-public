def unique_digits(x):
    result = []
    n = 1
    odd = True
    y = 0
    for n in x:
        odd = True
        y = n
        while y > 0:
            if y % 2 == 0:
                odd = False
            y = y // 10
        if odd:
            result.append(n)
    result.sort()
    return result


assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([]) == []
assert unique_digits([1]) == [1]
assert unique_digits([2]) == []
assert unique_digits([9, 10, 11, 12, 19, 20]) == [9, 11, 19]
assert unique_digits([99, 15, 15, 1]) == [1, 15, 15, 99]
assert unique_digits([101, 111, 13579, 20]) == [111, 13579]
assert unique_digits([8242, 65851, 60525, 66727]) == []
assert unique_digits([15582, 95792, 26729, 47057, 49317]) == []
assert unique_digits([34701, 74072, 8713, 43320, 89612, 59287]) == []
assert unique_digits([61704, 37171, 14832]) == [37171]
assert unique_digits([91387, 4905, 75398, 68041, 63465, 14825]) == []
assert unique_digits([89651, 60763, 35607, 82528, 42468]) == []
assert unique_digits([70416, 84240, 11221, 56189]) == []
assert unique_digits([83633, 18973, 31791, 37588, 9871]) == [31791]
assert unique_digits([66660, 88342]) == []
assert unique_digits([16599, 57716]) == []
assert unique_digits([53178]) == []
assert unique_digits([67420, 61382, 35465, 52857, 26542]) == []
assert unique_digits([53008, 73227, 20049]) == []
assert unique_digits([27802, 825, 68231, 30502, 27444]) == []
assert unique_digits([20594, 8918]) == []
assert unique_digits([3569, 72335, 6301]) == []
assert unique_digits([27329]) == []
assert unique_digits([73194, 14526, 79326, 15849, 1948]) == []
assert unique_digits([10959, 54065, 80366, 81265, 85747, 14748]) == []
assert unique_digits([20517, 47053, 3025, 67153, 10744, 15152]) == []
assert unique_digits([74341]) == []
assert unique_digits([]) == []
assert unique_digits([12675, 41555, 18218, 51336]) == []
assert unique_digits([]) == []
assert unique_digits([95796, 42490, 74021]) == []
assert unique_digits([]) == []
assert unique_digits([27679, 5227, 30173, 74430, 98583, 55412]) == []
assert unique_digits([62409, 68455, 73406, 76632, 46720]) == []
assert unique_digits([67120, 86882, 41224, 68443, 77279, 72636]) == []
assert unique_digits([15315]) == [15315]
assert unique_digits([]) == []
assert unique_digits([18352, 52024, 78459, 49134, 30972]) == []
assert unique_digits([63875, 93781, 78214, 75754, 33216]) == []
assert unique_digits([38098, 6371, 19865, 81318]) == []
assert unique_digits([41833, 10966, 28450, 83436]) == []
assert unique_digits([69933, 69195, 81068]) == []
assert unique_digits([41307, 22751]) == []
assert unique_digits([91345, 43123, 85995]) == []
assert unique_digits([57335, 78476, 85524, 74898, 70346, 34054]) == [57335]
assert unique_digits([46463, 33496, 91443, 70331, 67189, 30726]) == []
assert unique_digits([56660, 81475, 28620, 86952, 57753, 17343]) == [57753]
assert unique_digits([44807, 16551, 36223, 48071]) == []
assert unique_digits([78213, 91381, 52992, 95685]) == []
assert unique_digits([23842, 77939, 49090, 94916, 48085, 30786]) == [77939]
assert unique_digits([38022, 90402, 27381, 2699, 35567]) == []
assert unique_digits([54262, 19807]) == []
assert unique_digits([46053]) == []
assert unique_digits([95424, 89734, 66666]) == []
assert unique_digits([64562, 5746, 81676, 32859, 46776]) == []
assert unique_digits([57828, 94802, 48099, 99192, 3877, 73587]) == []
assert unique_digits([12210]) == []
assert unique_digits([31980, 27707, 89931, 52893]) == []
assert unique_digits([37319, 30880, 27301]) == [37319]
assert unique_digits([]) == []
assert unique_digits([23005, 73720, 57742]) == []
assert unique_digits([58619, 22461, 29258]) == []
