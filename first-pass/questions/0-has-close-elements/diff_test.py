import random
from fractions import Fraction

# ===== DYADIC SCALE =====
# Domain: each value v and threshold t is a dyadic rational  m / 2^P  with |m| bounded,
# P (fractional bits) small and FIXED.  Then differences v_i - v_j are multiples of 2^-P
# bounded by 2^(B+1), exactly representable in IEEE-754 double when (B+1)+P <= 52, so the
# float subtraction does NOT round and the exact integer model is BIT-IDENTICAL.
#
# We pick the proof scale K = 62 (so the SCALED integer X = v*2^62 is exact for any
# dyadic value with up to 62 fractional bits -- covers the whole domain with margin).
# The DOMAIN restriction (what we claim sound) is the dyadic-grid restriction below.

K = 62
TwoK = 2**K
def scale(v):
    fr = Fraction(v) * TwoK
    assert fr.denominator == 1, f"{v!r} not exact at K={K}"
    return int(fr)

def canonical(numbers, threshold):
    for idx, elem in enumerate(numbers):
        for idx2, elem2 in enumerate(numbers):
            if idx != idx2:
                if abs(elem - elem2) < threshold:
                    return True
    return False

def model(numbers, threshold):
    Xs = [scale(v) for v in numbers]; T = scale(threshold); n = len(numbers)
    for i in range(n):
        for j in range(n):
            if i != j and abs(Xs[i] - Xs[j]) < T:
                return True
    return False

def run(label, gen, thr_gen, n=80000):
    mism = 0; ex = []
    for _ in range(n):
        L = random.randint(0, 8)
        nums = [gen() for _ in range(L)]
        t = thr_gen()
        c = canonical(nums, t); m = model(nums, t)
        if c != m:
            mism += 1
            if len(ex) < 6: ex.append((nums, t, c, m))
    print(f"{label}: {mism}/{n}")
    for e in ex: print("   MISMATCH", e)
    return mism

random.seed(20260629)
tot = 0
# P=0: integers, |v|<2^20
tot += run("P=0 integers |v|<2^20",
           lambda: float(random.randint(-(2**20), 2**20)),
           lambda: float(random.randint(1, 2**18)))
# P=3: multiples of 1/8, |v|<2^16
tot += run("P=3 (n/8) |v|<2^16",
           lambda: random.randint(-(2**19), 2**19)/8.0,
           lambda: random.choice([1,2,3,5,7])/8.0 if random.random()<0.5 else random.randint(1,2**16)/8.0)
# P=8: multiples of 1/256, |v|<2^16  (covers 2-3 fractional decimal-ish values that ARE dyadic)
tot += run("P=8 (n/256) |v|<2^16",
           lambda: random.randint(-(2**24), 2**24)/256.0,
           lambda: random.randint(1, 2**20)/256.0)
# P=16: multiples of 1/65536, smaller magnitude |v|<2^16
tot += run("P=16 (n/65536) |v|<2^16",
           lambda: random.randint(-(2**32), 2**32)/65536.0,
           lambda: random.randint(1, 2**28)/65536.0)
# near-threshold / equal-distance hammer on dyadic grid (P=4), tight thresholds
tot += run("P=4 near-threshold hammer",
           lambda: random.randint(-64, 64)/16.0,
           lambda: random.choice([1,2,4,8,16,17,31,32])/16.0,
           n=120000)
# duplicates / equal values (distance 0)
tot += run("P=2 with duplicates",
           lambda: random.choice([0.0,0.25,0.5,1.0,1.0,2.0,2.0,-1.0,-1.0,3.0])/1.0,
           lambda: random.choice([0.25,0.5,1.0]),
           n=80000)

print("TOTAL MISMATCHES:", tot)

# docstring examples
print("doc1 [1,2,3]/0.5:", canonical([1.0,2.0,3.0],0.5), model([1.0,2.0,3.0],0.5))
print("doc2 [1,2.8,3,4,5,2]/0.3:", canonical([1.0,2.8,3.0,4.0,5.0,2.0],0.3), model([1.0,2.8,3.0,4.0,5.0,2.0],0.3))
