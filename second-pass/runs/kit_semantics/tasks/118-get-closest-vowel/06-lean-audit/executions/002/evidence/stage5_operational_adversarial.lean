import Proof

namespace AuditOperational

def nil : SortIntSeq := .«.IntSeq_MPY-CORE_IntSeq»
def cons (head : SortInt) (tail : SortIntSeq) : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail

def b_a_c : SortIntSeq := cons 98 (cons 97 (cons 99 nil))
def a_e_c : SortIntSeq := cons 97 (cons 101 (cons 99 nil))
def b_a_e : SortIntSeq := cons 98 (cons 97 (cons 101 nil))
def b_a_c_e_d : SortIntSeq :=
  cons 98 (cons 97 (cons 99 (cons 101 (cons 100 nil))))

example : Proof._andBool_ true false = false := rfl
example : Proof.«_>=Int_» (-1) 0 = false := rfl
example : Proof.«_>=Int_» 0 0 = true := rfl
example : Proof.«_<Int_» (-1) 0 = true := rfl
example : Proof.«_<=Int_» 1 0 = false := rfl
example : Proof.«_+Int_» (-2) 3 = 1 := rfl

example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» nil = 0 := rfl
example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» b_a_c = 3 := rfl
example : Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c (-1) = none := rfl
example : Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c 0 = some 98 := rfl
example : Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c 1 = some 97 := rfl
example : Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c 2 = some 99 := rfl
example : Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c 3 = none := rfl

example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c 0 nil false = some nil := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c (-1) nil false = some nil := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c 1 nil false = some (cons 97 nil) := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      a_e_c 1 nil false = some nil := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_e 1 nil false = some nil := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c 1 (cons 42 nil) true = some (cons 42 nil) := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c_e_d 3 nil false = some (cons 101 nil) := rfl
example :
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c 4 nil false = none := rfl

def convenientAt (_ : SortIntSeq) (_ : SortInt) : Option SortInt := some 0
def convenientScan
    (_ : SortIntSeq) (_ : SortInt) (_ : SortIntSeq) (_ : SortBool) :
    Option SortIntSeq := some nil

theorem convenient_model_still_proves_generated_target :
    Klean118GetClosestVowel.Lemmas.targetStatement
      Proof._andBool_
      Proof.«_>=Int_»
      Proof.«_<Int_»
      Proof.«_<=Int_»
      Proof.«_+Int_»
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      convenientScan
      convenientAt := by
  unfold Klean118GetClosestVowel.Lemmas.targetStatement
  simp [convenientAt, convenientScan]

example : convenientAt b_a_c 0 ≠
    Proof.«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» b_a_c 0 := by
  decide
example : convenientScan b_a_c 1 nil false ≠
    Proof.«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
      b_a_c 1 nil false := by
  intro equality
  cases equality

end AuditOperational
