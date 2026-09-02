import Proof

#eval Proof.«_+Int_» (-7) 5
#eval Proof.«_+Int_» 0 0
#eval Proof.«_+Int_» 12345678901234567890 (-9876543210987654321)

example : Proof.«_+Int_» (-7) 5 = -2 := rfl
example : Proof.«_+Int_» 0 0 = 0 := rfl
example :
    Proof.«_+Int_» 12345678901234567890 (-9876543210987654321) =
      2469135690246913569 := rfl

def constantAdd (_x _y : SortInt) : SortInt := 0
def leftProjection (x _y : SortInt) : SortInt := x
def rightProjection (_x y : SortInt) : SortInt := y

example : Klean98CountUpper.Lemmas.targetStatement constantAdd := by
  intro C B A
  rfl

example : Klean98CountUpper.Lemmas.targetStatement leftProjection := by
  intro C B A
  rfl

example : Klean98CountUpper.Lemmas.targetStatement rightProjection := by
  intro C B A
  rfl
