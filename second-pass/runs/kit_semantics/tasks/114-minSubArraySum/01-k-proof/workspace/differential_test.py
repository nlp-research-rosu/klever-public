from itertools import product

from solution import minSubArraySum


def brute_force_min_subarray(nums):
    best = nums[0]
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            if total < best:
                best = total
    return best


checked = 0
mismatches = 0
for length in range(1, 7):
    for values in product(range(-3, 4), repeat=length):
        nums = list(values)
        checked += 1
        if minSubArraySum(nums) != brute_force_min_subarray(nums):
            mismatches += 1
            print(
                "mismatch",
                nums,
                minSubArraySum(nums),
                brute_force_min_subarray(nums),
            )

print(f"checked={checked} mismatches={mismatches}")
if mismatches:
    raise SystemExit(1)
