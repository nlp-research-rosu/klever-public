import Klean84Solve.Lemmas
import Lean

open Lean Elab Term

namespace Proof.BuildIS

private def findUniquePrivateConstant (suffix : String) : TermElabM Name := do
  let environment ← getEnv
  let candidates := environment.constants.toList.filter fun entry =>
    entry.1.toString.endsWith suffix
  match candidates with
  | [entry] => pure entry.1
  | [] => throwError "missing private constant ending in {suffix}"
  | _ => throwError "ambiguous private constant ending in {suffix}"

elab "kleanIntSeqLengthModel" : term => do
  return .const (← findUniquePrivateConstant "kleanIntSeqLengthModel") []

elab "kleanIntSeqAtNatModel" : term => do
  return .const (← findUniquePrivateConstant "kleanIntSeqAtNatModel") []

elab "kleanIntSeqAtModel" : term => do
  return .const (← findUniquePrivateConstant "kleanIntSeqAtModel") []

elab "kleanBuildISContinueModel" : term => do
  return .const (← findUniquePrivateConstant "kleanBuildISContinueModel") []

elab "kleanBuildISFuelModel" : term => do
  return .const (← findUniquePrivateConstant "kleanBuildISFuelModel") []

elab "kleanBuildISModel" : term => do
  return .const (← findUniquePrivateConstant "kleanBuildISModel") []

abbrev lengthModel : SortIntSeq → Nat :=
  kleanIntSeqLengthModel

abbrev atNatModel : SortIntSeq → Nat → Option SortInt :=
  kleanIntSeqAtNatModel

abbrev atModel : SortIntSeq → SortInt → Option SortInt :=
  kleanIntSeqAtModel

abbrev continueModel : SortInt → SortInt → SortInt → Bool :=
  kleanBuildISContinueModel

abbrev fuelModel :
    Nat → SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq :=
  kleanBuildISFuelModel

abbrev buildModel :
    SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq :=
  kleanBuildISModel

def append : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ys => ys
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs, ys =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (append xs ys)

@[simp] theorem lengthModel_empty :
    lengthModel SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» = 0 := by
  rfl

@[simp] theorem lengthModel_cons (x : SortInt) (xs : SortIntSeq) :
    lengthModel
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs) =
      lengthModel xs + 1 := by
  rfl

@[simp] theorem lengthModel_append (xs ys : SortIntSeq) :
    lengthModel (append xs ys) = lengthModel xs + lengthModel ys := by
  induction xs with
  | «.IntSeq_MPY-CORE_IntSeq» => simp [append]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs ih =>
      simp [append, ih, Nat.add_assoc, Nat.add_comm]

@[simp] theorem atNatModel_append_length_cons
    (pre rest : SortIntSeq) (x : SortInt) :
    atNatModel
        (append pre
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x rest))
        (lengthModel pre) =
      some x := by
  induction pre with
  | «.IntSeq_MPY-CORE_IntSeq» => rfl
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y pre ih =>
      simpa [append, Nat.add_comm] using ih

theorem append_cons_assoc
    (pre rest : SortIntSeq) (x : SortInt) :
    append pre
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x rest) =
      append
        (append pre
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
        rest := by
  induction pre with
  | «.IntSeq_MPY-CORE_IntSeq» => rfl
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y pre ih =>
      simp [append, ih]

@[simp] theorem atModel_ofNat (input : SortIntSeq) (index : Nat) :
    atModel input (Int.ofNat index) = atNatModel input index := by
  rfl

theorem continueModel_eq
    (index stop step : SortInt) :
    continueModel index stop step =
      ((step > 0 && index < stop) || (step < 0 && index > stop)) := by
  rfl

@[simp] theorem fuelModel_zero
    (input : SortIntSeq) (index stop step : SortInt) :
    fuelModel 0 input index stop step =
      if continueModel index stop step then none
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» := by
  rfl

@[simp] theorem fuelModel_succ
    (fuel : Nat) (input : SortIntSeq) (index stop step : SortInt) :
    fuelModel (fuel + 1) input index stop step =
      if continueModel index stop step then
        match atModel input index with
        | none => none
        | some value =>
            match fuelModel fuel input (index + step) stop step with
            | none => none
            | some rest =>
                some
                  (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                    value rest)
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» := by
  rfl

theorem buildModel_eq_fuelModel
    (input : SortIntSeq) (index stop step : SortInt) :
    buildModel input index stop step =
      fuelModel (lengthModel input + 1) input index stop step := by
  rfl

theorem fuelModel_append_suffix
    (pre rest : SortIntSeq) (extra : Nat) (extra_pos : 0 < extra) :
    fuelModel (lengthModel rest + extra) (append pre rest)
        (Int.ofNat (lengthModel pre))
        (Int.ofNat (lengthModel pre + lengthModel rest))
        1 =
      some rest := by
  induction rest generalizing pre with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      cases extra with
      | zero => omega
      | succ extra =>
          simp [fuelModel_succ, continueModel_eq]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x rest ih =>
      have fuel_eq :
          lengthModel
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  x rest) +
              extra =
            (lengthModel rest + extra) + 1 := by
        simp
        omega
      rw [fuel_eq, fuelModel_succ]
      have continue_eq :
          continueModel
              (Int.ofNat (lengthModel pre))
              (Int.ofNat
                (lengthModel pre +
                  lengthModel
                    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                      x rest)))
              1 =
            true := by
        simp [continueModel_eq]
        have positive_increment :
            (0 : Int) < Int.ofNat (lengthModel rest) + 1 :=
          Int.add_pos_of_nonneg_of_pos
            (Int.natCast_nonneg (lengthModel rest))
            (by decide)
        have shifted :=
          Int.add_lt_add_left positive_increment
            (Int.ofNat (lengthModel pre))
        simpa using shifted
      rw [if_pos continue_eq]
      have at_eq :
          atModel
              (append pre
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  x rest))
              (Int.ofNat (lengthModel pre)) =
            some x := by
        rw [atModel_ofNat]
        exact atNatModel_append_length_cons pre rest x
      rw [at_eq]
      let nextPre :=
        append pre
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      have recursive_eq :
          fuelModel (lengthModel rest + extra)
              (append pre
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  x rest))
              (Int.ofNat (lengthModel pre) + 1)
              (Int.ofNat
                (lengthModel pre +
                  lengthModel
                    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                      x rest)))
              1 =
            some rest := by
        have next_ih := ih (pre := nextPre)
        rw [← append_cons_assoc pre rest x] at next_ih
        simpa [
          nextPre,
          Nat.add_assoc,
          Nat.add_comm,
          Nat.add_left_comm
        ] using next_ih
      rw [recursive_eq]

theorem buildIS_eq_buildModel
    (input : SortIntSeq) (index stop step : SortInt) :
    «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
        input index stop step =
      buildModel input index stop step := by
  rfl

theorem buildModel_append_suffix (pre rest : SortIntSeq) :
    buildModel (append pre rest)
        (Int.ofNat (lengthModel pre))
        (Int.ofNat (lengthModel pre + lengthModel rest))
        1 =
      some rest := by
  rw [buildModel_eq_fuelModel]
  have extra_pos : 0 < lengthModel pre + 1 := by
    omega
  simpa [
    Nat.add_assoc,
    Nat.add_comm,
    Nat.add_left_comm
  ] using
    fuelModel_append_suffix pre rest (lengthModel pre + 1) extra_pos

theorem buildIS_append_suffix (pre rest : SortIntSeq) :
    «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
        (append pre rest)
        (Int.ofNat (lengthModel pre))
        (Int.ofNat (lengthModel pre + lengthModel rest))
        1 =
      some rest := by
  rw [buildIS_eq_buildModel]
  exact buildModel_append_suffix pre rest

@[simp] theorem isLen_eq_lengthModel (input : SortIntSeq) :
    «isLen(_)_MPY-CORE_Int_IntSeq» input =
      some (Int.ofNat (lengthModel input)) := by
  induction input with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [
        «isLen(_)_MPY-CORE_Int_IntSeq»,
        _11995f1,
        _9b4a103
      ]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x input ih =>
      simp [
        «isLen(_)_MPY-CORE_Int_IntSeq»,
        _11995f1,
        _9b4a103,
        ih,
        «_+Int_»
      ]
      exact Int.add_comm 1 (Int.ofNat (lengthModel input))

def twoPrefix : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

theorem buildIS_drop_two (rest : SortIntSeq) :
    «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 rest))
        2
        (Int.ofNat
          (lengthModel
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                rest))))
        1 =
      some rest := by
  simpa [
    twoPrefix,
    append,
    Nat.add_assoc,
    Nat.add_comm,
    Nat.add_left_comm
  ] using buildIS_append_suffix twoPrefix rest

@[simp] theorem slStep_noBound :
    «slStep(_)_MPY-SUBSCRIPT_Int_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
      some 1 := by
  rfl

@[simp] theorem slStop_noBounds (length : SortInt) :
    «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        length =
      some length := by
  rfl

@[simp] theorem kite_false {α : Type} (x y : α) :
    kite false x y = some y := by
  rfl

@[simp] theorem kite_true {α : Type} (x y : α) :
    kite true x y = some x := by
  rfl

@[simp] theorem option_bind_some {α : Type} (value : Option α) :
    value.bind some = value := by
  cases value <;> rfl

theorem clampHi_two (tailLength : Nat) :
    «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
        2 (Int.ofNat (tailLength + 2)) 1 =
      some 2 := by
  cases tailLength with
  | zero =>
      rfl
  | succ tailLength =>
      have positive_increment :
          (0 : Int) < Int.ofNat tailLength + 1 :=
        Int.add_pos_of_nonneg_of_pos
          (Int.natCast_nonneg tailLength)
          (by decide)
      have index_lt :
          (2 : Int) < (Int.ofNat tailLength + 1) + 2 := by
        have shifted := Int.add_lt_add_right positive_increment 2
        simpa using shifted
      have index_not_ge :
          ¬(2 : Int) ≥ (Int.ofNat tailLength + 1) + 2 := by
        intro index_ge
        exact Int.not_lt_of_ge index_ge index_lt
      have index_lt_original :
          (2 : Int) < Int.ofNat (Nat.succ tailLength + 2) := by
        change (2 : Int) < (Int.ofNat tailLength + 1) + 2
        exact index_lt
      have index_not_ge_original :
          ¬(2 : Int) ≥ Int.ofNat (Nat.succ tailLength + 2) := by
        intro index_ge
        exact Int.not_lt_of_ge index_ge index_lt_original
      have ge_false :
          «_>=Int_» 2 (Int.ofNat (Nat.succ tailLength + 2)) =
            some false := by
        unfold «_>=Int_»
        rw [decide_eq_false index_not_ge_original]
      have lt_true :
          «_<Int_» 2 (Int.ofNat (Nat.succ tailLength + 2)) =
            some true := by
        unfold «_<Int_»
        rw [decide_eq_true index_lt_original]
      have first_none :
          _6f49a32 2 (Int.ofNat (Nat.succ tailLength + 2)) 1 =
            none := by
        simp only [
          _6f49a32,
          ge_false
        ]
        rfl
      have second_some :
          _ffe5f5d 2 (Int.ofNat (Nat.succ tailLength + 2)) 1 =
            some 2 := by
        simp only [
          _ffe5f5d,
          lt_true
        ]
        rfl
      rw [
        show
          «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
              2 (Int.ofNat (Nat.succ tailLength + 2)) 1 =
            (_6f49a32 2 (Int.ofNat (Nat.succ tailLength + 2)) 1 <|>
              _ffe5f5d 2 (Int.ofNat (Nat.succ tailLength + 2)) 1) by
          rfl,
        first_none,
        second_some
      ]
      rfl

theorem slStart_two (tailLength : Nat) :
    «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int»
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        (Int.ofNat (tailLength + 2)) =
      some 2 := by
  have positive_some :
      _4b524a8 2 (Int.ofNat (tailLength + 2)) 1 =
        some 2 := by
    have ge_true : «_>=Int_» 2 0 = some true := by
      rfl
    simp only [
      _4b524a8,
      ge_true,
      clampHi_two
    ]
    rfl
  have negative_none :
      _e75deb6 2 (Int.ofNat (tailLength + 2)) 1 =
        none := by
    rfl
  have adjust_eq :
      «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
          2 (Int.ofNat (tailLength + 2)) 1 =
        some 2 := by
    rw [
      show
        «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
            2 (Int.ofNat (tailLength + 2)) 1 =
          (_4b524a8 2 (Int.ofNat (tailLength + 2)) 1 <|>
            _e75deb6 2 (Int.ofNat (tailLength + 2)) 1) by
        rfl,
      positive_some
    ]
    rfl
  have final_some :
      _4ae8014
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          (Int.ofNat (tailLength + 2)) =
        some 2 := by
    unfold _4ae8014
    change
      (do
        let step ←
          «slStep(_)_MPY-SUBSCRIPT_Int_OptInt»
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        let adjusted ←
          «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
            2 (Int.ofNat (tailLength + 2)) step
        pure adjusted) =
        some 2
    rw [slStep_noBound]
    simp only [
      Option.bind_eq_bind,
      Option.bind_some,
      Option.pure_def,
      option_bind_some
    ]
    exact adjust_eq
  rw [
    show
      «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int»
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          (Int.ofNat (tailLength + 2)) =
        (_396b61d
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            (Int.ofNat (tailLength + 2)) <|>
          _3cb3e9b
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            (Int.ofNat (tailLength + 2)) <|>
          _4ae8014
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            (Int.ofNat (tailLength + 2))) by
        rfl,
    show
      _396b61d
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          (Int.ofNat (tailLength + 2)) =
        none by
      rfl,
    show
      _3cb3e9b
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          (Int.ofNat (tailLength + 2)) =
        none by
      rfl,
    final_some
  ]
  rfl

theorem doSlice_drop_binary_prefix (rest : SortIntSeq) :
    «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                rest))))
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
      some
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rest)) := by
  have start_eq :
      «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int»
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          (Int.ofNat
            (lengthModel
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                  rest)))) =
        some 2 := by
    simpa [Nat.add_assoc] using slStart_two (lengthModel rest)
  have primary_eq :
      _13a7bb3
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                  rest))))
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
        some
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rest)) := by
    simp only [
      _13a7bb3,
      isLen_eq_lengthModel,
      start_eq,
      slStop_noBounds,
      slStep_noBound,
      buildIS_drop_two,
      Option.bind_eq_bind,
      Option.bind_some,
      Option.pure_def
    ]
    rfl
  rw [
    show
      «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                  rest))))
          (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
          SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
        (_13a7bb3
            (SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                  (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                    rest))))
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» <|>
          _84f67ef
            (SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                  (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                    rest))))
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» <|>
          _8f16e60
            (SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
                  (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                    rest))))
            (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
            SortOptInt.«noB_MPY-SUBSCRIPT_OptInt») by
        rfl,
    primary_eq
  ]
  rfl

end Proof.BuildIS
