def by_length(arr):
    return (
        ["Nine"] * arr.count(9)
        + ["Eight"] * arr.count(8)
        + ["Seven"] * arr.count(7)
        + ["Six"] * arr.count(6)
        + ["Five"] * arr.count(5)
        + ["Four"] * arr.count(4)
        + ["Three"] * arr.count(3)
        + ["Two"] * arr.count(2)
        + ["One"] * arr.count(1)
    )
