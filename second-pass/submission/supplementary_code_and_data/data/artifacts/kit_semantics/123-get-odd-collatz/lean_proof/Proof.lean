import Klean123GetOddCollatz.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (a b : SortBool) : SortBool := a && b
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := a == b
/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-bf51f8af576c3c723ddfe912c4608940069bce29b6be31b545366c25e65e8e30, rule-57fc2eb6b8603c24117bc3c8656ecab475bdba5d09587b0d5fd0085351fcdb37, rule-89c097c36f3bdd496566e3c2f532dd496a1097a579d8ee9ce25c05754246d84e, rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_==K_» (a b : SortK) : SortBool :=
  letI : DecidableEq SortK := Classical.typeDecidableEq SortK
  decide (a = b)
/- KORE symbol: LblcollatzNext'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'Int; frozen source obligations: rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» (n : SortInt) : SortInt :=
  let r := ((n % 2) + 2) % 2
  if r == 0 then Int.tdiv (n - r) 2 else 3 * n + 1
/- KORE symbol: LblmaybeOdd'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'ValSeq'Unds'Int; frozen source obligations: rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» (n : SortInt) : SortValSeq :=
  let r := ((n % 2) + 2) % 2
  if r == 0 then
    SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  else
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt n)
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-89c097c36f3bdd496566e3c2f532dd496a1097a579d8ee9ce25c05754246d84e, rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (b : SortBool) : SortBool := !b
/- KORE symbol: LbloddWithoutLast'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» :
    SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest) =>
      let tail :=
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest
      match v with
      | SortVal.inj_SortInt i =>
          let r := ((i % 2) + 2) % 2
          if r == 0 then
            «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» tail
          else
            SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
              (SortVal.inj_SortInt i)
              («oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» tail)
      | _ => «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» tail
/- KORE symbol: LbltraceFirstInt'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'ValSeq; frozen source obligations: rule-89c097c36f3bdd496566e3c2f532dd496a1097a579d8ee9ce25c05754246d84e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» :
    SortValSeq → SortInt
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt i) _ => i
  | _ => 0
/- KORE symbol: LbltraceLastInt'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'ValSeq; frozen source obligations: rule-f6103b1ac225a169c76b912d0d9466de492ff6054396a5013d6ad69ec17b572b, rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632, rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» :
    SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest =>
      match rest with
      | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
          match v with
          | SortVal.inj_SortInt i => i
          | _ => 0
      | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ =>
          «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» rest
/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa, rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97, rule-bf51f8af576c3c723ddfe912c4608940069bce29b6be31b545366c25e65e8e30, rule-57fc2eb6b8603c24117bc3c8656ecab475bdba5d09587b0d5fd0085351fcdb37, rule-89c097c36f3bdd496566e3c2f532dd496a1097a579d8ee9ce25c05754246d84e, rule-f6103b1ac225a169c76b912d0d9466de492ff6054396a5013d6ad69ec17b572b, rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632, rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest, tail =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail)
/- KORE symbol: LblvalidCollatzTrace'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632, rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» :
    SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest =>
      match v, rest with
      | SortVal.inj_SortInt _, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
          true
      | SortVal.inj_SortInt i,
          SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt j) tail =>
          (j == «collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» i) &&
            «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
              (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
                (SortVal.inj_SortInt j) tail)
      | _, _ => false

private theorem eqK_true_of_eq {a b : SortK} (h : a = b) :
    «_==K_» a b = true := by
  simp [«_==K_», h]

private theorem eqK_false_of_ne {a b : SortK} (h : a ≠ b) :
    «_==K_» a b = false := by
  simp [«_==K_», h]

private theorem concat_empty_right : ∀ A : SortValSeq,
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
      A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = A
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest => by
      simp only [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]
      rw [concat_empty_right rest]

private theorem concat_assoc : ∀ A B C : SortValSeq,
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C =
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C)
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest, B, C => by
      simp only [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]
      rw [concat_assoc rest B C]

private theorem concat_cons_ne_empty : ∀
    (A : SortValSeq) (v : SortVal) (rest : SortValSeq),
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest) ≠
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => by
      simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _, _, _ => by
      simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]

private def valSeqObservedInK : SortK → SortValSeq
  | SortK.kseq (SortKItem.inj_SortValSeq values) _ => values
  | _ => SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

private theorem valSeq_ne_empty_of_not_eqK {T : SortValSeq}
    (h : notBool_
      («_==K_»
        (SortK.kseq (SortKItem.inj_SortValSeq T) SortK.dotk)
        (SortK.kseq
          (SortKItem.inj_SortValSeq
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)) = true) :
    T ≠ SortValSeq.«.ValSeq_MPY-CORE_ValSeq» := by
  intro e
  subst T
  have ek := eqK_true_of_eq (a :=
    SortK.kseq
      (SortKItem.inj_SortValSeq
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk) rfl
  simp [notBool_, ek] at h

private theorem traceLast_concat_singleton : ∀
    (T : SortValSeq) (J : SortInt),
    «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt J)
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) = J
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest), J => by
      simpa [
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»
      ] using traceLast_concat_singleton
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest) J

private theorem valid_concat_singleton : ∀
    (T : SortValSeq) (J : SortInt),
    T ≠ SortValSeq.«.ValSeq_MPY-CORE_ValSeq» →
    «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt J)
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) =
      _andBool_
        («validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» T)
        («_==Int_» J
          («collatzNext(_)_VERIFICATION-SYNTAX_Int_Int»
            («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» T)))
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, h => False.elim (h rfl)
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», J, _ => by
      cases v <;> simp [
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»,
        «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»,
        «_==Int_», _andBool_]
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest), J, _ => by
      have ih := valid_concat_singleton
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest) J
        (by simp)
      cases v <;> try simp [
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»,
        «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»,
        «_==Int_», _andBool_]
      case inj_SortInt i =>
        cases w <;> simp_all [
          «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
          «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»,
          «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»,
          «_==Int_», _andBool_, Bool.and_assoc]

private theorem oddWithoutLast_concat_singleton : ∀
    (T : SortValSeq) (ignored : SortInt),
    «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» T = true →
    «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt ignored)
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) =
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        («oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» T)
        («maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int»
          («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» T))
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, h => by
      simp [«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»] at h
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», ignored, h => by
      cases v <;> simp_all [
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»,
        «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»,
        «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»,
        «maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int»]
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest),
      ignored, h => by
      have ih := oddWithoutLast_concat_singleton
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» w rest)
        ignored
      cases v <;> try simp [
        «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»] at h
      case inj_SortInt i =>
        cases w <;> try simp [
          «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»] at h
        case inj_SortInt j =>
          have hj : j = «collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» i := by
            exact h.1
          have tailValid := h.2
          subst j
          have ihApplied := ih tailValid
          simp only [
            «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
            «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»,
            «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»]
          split
          · exact ihApplied
          · exact congrArg
              (fun values =>
                SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
                  (SortVal.inj_SortInt i) values)
              ihApplied

theorem final :
    Klean123GetOddCollatz.Lemmas.targetStatement _andBool_ «_==Int_» «_==K_» «collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» «maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» notBool_ «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» «traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» := by
  unfold Klean123GetOddCollatz.Lemmas.targetStatement
  refine ⟨concat_empty_right, (fun C B A => concat_assoc A B C),
    ?_, ?_, ?_, (fun J T => traceLast_concat_singleton T J),
    ?_, (fun ignored T h =>
      oddWithoutLast_concat_singleton T ignored h)⟩
  · intro gen2 gen1 gen0
    apply eqK_false_of_ne
    intro h
    have observed := congrArg valSeqObservedInK h
    have : «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» gen0
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» gen1 gen2) =
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» := by
      simpa [valSeqObservedInK] using observed
    exact concat_cons_ne_empty gen0 gen1 gen2 this
  · intro gen2 gen1 gen0
    apply eqK_false_of_ne
    intro h
    have observed := congrArg valSeqObservedInK h
    have : SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» gen0
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» gen1 gen2) := by
      simpa [valSeqObservedInK] using observed
    exact concat_cons_ne_empty gen0 gen1 gen2 this.symm
  · intro J T h
    cases T with
    | «.ValSeq_MPY-CORE_ValSeq» =>
        have e := eqK_true_of_eq (a :=
          SortK.kseq
            (SortKItem.inj_SortValSeq
              SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk) rfl
        simp [notBool_, e] at h
    | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest =>
        cases v <;> rfl
  · intro J T h
    exact valid_concat_singleton T J (valSeq_ne_empty_of_not_eqK h)

end Proof
