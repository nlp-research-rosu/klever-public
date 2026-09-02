import Klean98CountUpper.Lemmas

def subtraction (x y : SortInt) : SortInt := x - y

example : Klean98CountUpper.Lemmas.targetStatement subtraction := by
  intro C B A
  rfl
