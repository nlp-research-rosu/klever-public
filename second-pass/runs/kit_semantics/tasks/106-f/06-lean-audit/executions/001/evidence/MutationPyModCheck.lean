import Proof

-- The frozen program uses modulus 2, where Python/K gives (-3) % 2 = 1.
-- This is expected to fail against the deliberately constant-zero bridge.
example : Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» (-3) 2 = 1 := by
  native_decide
