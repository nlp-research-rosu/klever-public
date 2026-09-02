import Klean106F.Lemmas

namespace Proof

/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97, rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa, rule-4bb6de9678be64ad9a5dbb1d96a9acd747002bd379e02e9adb311bd159bf6396, rule-6b49fce56fe800f0a53b8ec7f41fec54b9db95c08b9bd8d56dde0b6720d71d84. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», suffix => suffix
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, suffix =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        value
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest suffix)

theorem final :
    Klean106F.Lemmas.targetStatement «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  unfold Klean106F.Lemmas.targetStatement
  let rec assoc (A B C : SortValSeq) :
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
          («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C =
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A
          («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) :=
    match A with
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
        rfl
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
        congrArg
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value)
          (assoc rest B C)
  let rec rightIdentity (A : SortValSeq) :
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
          A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = A :=
    match A with
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
        rfl
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
        congrArg
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value)
          (rightIdentity rest)
  let rec leftCancel (P A B : SortValSeq) :
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P A =
          «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P B →
        A = B :=
    match P with
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
        fun h => h
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest => by
        intro h
        injection h with _ htail
        exact leftCancel rest A B htail
  constructor
  · intro C B A
    exact assoc A B C
  constructor
  · intro A
    exact rightIdentity A
  constructor
  · intro B P A
    constructor
    · exact leftCancel P A B
    · intro h
      exact congrArg
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P)
        h
  · intro A P
    constructor
    · intro h
      apply leftCancel P SortValSeq.«.ValSeq_MPY-CORE_ValSeq» A
      calc
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            P SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = P :=
          rightIdentity P
        _ = «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P A := h
    · intro h
      cases h
      exact (rightIdentity P).symm

end Proof
