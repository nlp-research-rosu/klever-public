import Proof

def quietNaN : Float := Float.ofBits 0x7ff8000000000000

#eval (Proof.maxFOpaque quietNaN 1.0).isNaN
#eval (Proof.«maxFloat(_,_)_FLOAT_Float_Float_Float» quietNaN 1.0).isNaN
#eval (Proof.maxFOpaque 1.0 quietNaN).isNaN
#eval (Proof.«maxFloat(_,_)_FLOAT_Float_Float_Float» 1.0 quietNaN).isNaN
