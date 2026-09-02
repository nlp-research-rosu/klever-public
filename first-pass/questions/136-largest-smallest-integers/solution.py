def largest_smallest_integers(lst):
    a = 0
    b = 0
    hn = False
    hp = False
    x = 0
    for x in lst:
        if x < 0:
            if hn == False:
                a = x
                hn = True
            elif x > a:
                a = x
        elif x > 0:
            if hp == False:
                b = x
                hp = True
            elif x < b:
                b = x
    ra = None
    if hn:
        ra = a
    rb = None
    if hp:
        rb = b
    return (ra, rb)
