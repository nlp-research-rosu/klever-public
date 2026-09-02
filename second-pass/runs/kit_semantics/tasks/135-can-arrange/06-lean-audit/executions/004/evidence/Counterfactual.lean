import Proof

namespace AuditCounterfactual

def intVal (value : SortInt) : SortVal := .inj_SortInt value

def constantApplyCmp (_ : SortString) (_ _ : SortVal) : SortBool := false
def constantOrderGe (_ _ : SortVal) : SortBool := false
def constantOrderablePair (_ _ : SortVal) : SortBool := true

theorem coordinatedConstantsStillProveGeneratedTarget :
    Klean135CanArrange.Lemmas.targetStatement
      constantApplyCmp constantOrderGe constantOrderablePair := by
  unfold Klean135CanArrange.Lemmas.targetStatement
  intros
  rfl

def negatedGeApplyCmp (operator : SortString) (left right : SortVal) : SortBool :=
  if operator = ">=" then !(Proof.operationalOrderGe left right)
  else Proof.operationalApplyCmp operator left right

example : constantApplyCmp ">=" (intVal 2) (intVal 1) ≠
    Proof.operationalApplyCmp ">=" (intVal 2) (intVal 1) := by decide

example : negatedGeApplyCmp ">=" (intVal 2) (intVal 1) ≠
    Proof.operationalOrderGe (intVal 2) (intVal 1) := by decide

#print axioms coordinatedConstantsStillProveGeneratedTarget
#eval ("coordinated constant mutation vs frozen 2>=1",
  constantApplyCmp ">=" (intVal 2) (intVal 1),
  Proof.operationalApplyCmp ">=" (intVal 2) (intVal 1))
#eval ("negated mutation vs frozen 2>=1",
  negatedGeApplyCmp ">=" (intVal 2) (intVal 1),
  Proof.operationalOrderGe (intVal 2) (intVal 1))

end AuditCounterfactual
