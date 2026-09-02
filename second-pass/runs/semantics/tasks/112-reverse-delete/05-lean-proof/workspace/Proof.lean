import Klean112ReverseDelete.Lemmas
import Lean

namespace Proof

open Lean Meta Elab Tactic

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def _Map_ (left right : SortMap) : SortMap :=
  match _root_._Map_ left right with
  | some result => result
  | none => left

private def normalizeKItem : SortKItem → SortKItem
  | SortKItem.inj_SortVal value => (@inj SortVal SortKItem) value
  | item => item

/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(normalizeKItem key, normalizeKItem value)]⟩

private def intSeqConcat (left right : SortIntSeq) : SortIntSeq :=
  match left with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (intSeqConcat tail right)

private def intSeqContainsChar (needle : SortInt) (haystack : SortIntSeq) : Bool :=
  match haystack with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      needle == head || intSeqContainsChar needle tail
/- KORE symbol: LblkeptAcc'LParUndsCommUndsCommUndsRParUnds'MPY-VERIFICATION-BASE'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
    (remaining deleted accumulator : SortIntSeq) : SortIntSeq :=
  match remaining with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      if intSeqContainsChar head deleted
      then
        «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
          tail deleted accumulator
      else
        «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
          tail deleted
          (intSeqConcat accumulator
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              head SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
/- KORE symbol: LbllastCharacter'LParUndsCommUndsRParUnds'MPY-VERIFICATION-BASE'Unds'Val'Unds'IntSeq'Unds'Val; frozen source obligations: rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val»
    (remaining : SortIntSeq) (previous : SortVal) : SortVal :=
  match remaining with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => previous
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val»
        tail
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              head SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
/- KORE symbol: LblreversedKeptAcc'LParUndsCommUndsCommUndsRParUnds'MPY-VERIFICATION-BASE'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
    (remaining deleted accumulator : SortIntSeq) : SortIntSeq :=
  match remaining with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      if intSeqContainsChar head deleted
      then
        «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
          tail deleted accumulator
      else
        «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
          tail deleted
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head accumulator)

private theorem mapDecompose (left right : SortMap) :
    ∃ remainder, _root_._Map_ left remainder = some (_Map_ left right) := by
  unfold _Map_
  cases h : _root_._Map_ left right with
  | some result =>
      exact ⟨right, h⟩
  | none =>
      cases left
      refine ⟨⟨[]⟩, ?_⟩
      change some (⟨_ ++ []⟩ : SortMap) = some (⟨_⟩ : SortMap)
      simp

private theorem optionIsSomeIf {α : Type} (p : Prop) [Decidable p] (value : α) :
    (if p then some value else none).isSome = decide p := by
  by_cases h : p <;> simp [h]

private theorem singletonConcatIsSome
    (key value₁ value₂ : SortKItem) (right : SortMap) :
    (_root_._Map_ ⟨[(key, value₁)]⟩ right).isSome =
      (_root_._Map_ ⟨[(key, value₂)]⟩ right).isSome := by
  cases right with
  | mk entries =>
      induction entries with
      | nil =>
          run_tac
            let goal ← getMainGoal
            let ctx ← Simp.Context.mkDefault
            let privatePrefix :=
              Name.num
                (Name.str
                  (Name.str (Name.mkSimple "_private") "Klean112ReverseDelete")
                  "Func")
                0
            let simpTheorems ← getSimpTheorems
            let simpTheorems ←
              simpTheorems.addDeclToUnfold (Name.mkSimple "_Map_")
            let simpTheorems ←
              simpTheorems.addDeclToUnfold
                (Name.str privatePrefix "kleanMapDisjointModel")
            let simpTheorems ←
              simpTheorems.addDeclToUnfold
                (Name.str privatePrefix "kleanMapContainsModel")
            let ctx := ctx.setSimpTheorems #[simpTheorems]
            let hyps ← goal.getNondepPropHyps
            let (result, _) ← simpGoal goal ctx (fvarIdsToSimp := hyps)
            match result with
            | none => replaceMainGoal []
            | some (_, newGoal) => replaceMainGoal [newGoal]
      | cons pair entries ih =>
          rcases pair with ⟨otherKey, otherValue⟩
          by_cases h : key = otherKey
          · run_tac
              let goal ← getMainGoal
              let ctx ← Simp.Context.mkDefault
              let privatePrefix :=
                Name.num
                  (Name.str
                    (Name.str (Name.mkSimple "_private") "Klean112ReverseDelete")
                    "Func")
                  0
              let simpTheorems ← getSimpTheorems
              let simpTheorems ←
                simpTheorems.addDeclToUnfold (Name.mkSimple "_Map_")
              let simpTheorems ←
                simpTheorems.addDeclToUnfold
                  (Name.str privatePrefix "kleanMapDisjointModel")
              let simpTheorems ←
                simpTheorems.addDeclToUnfold
                  (Name.str privatePrefix "kleanMapContainsModel")
              let ctx := ctx.setSimpTheorems #[simpTheorems]
              let hyps ← goal.getNondepPropHyps
              let (result, _) ← simpGoal goal ctx (fvarIdsToSimp := hyps)
              match result with
              | none => replaceMainGoal []
              | some (_, newGoal) => replaceMainGoal [newGoal]
            simp [h]
          · run_tac
              let goal ← getMainGoal
              let ctx ← Simp.Context.mkDefault
              let privatePrefix :=
                Name.num
                  (Name.str
                    (Name.str (Name.mkSimple "_private") "Klean112ReverseDelete")
                    "Func")
                  0
              let simpTheorems ← getSimpTheorems
              let simpTheorems ←
                simpTheorems.addDeclToUnfold (Name.mkSimple "_Map_")
              let simpTheorems ←
                simpTheorems.addDeclToUnfold
                  (Name.str privatePrefix "kleanMapDisjointModel")
              let simpTheorems ←
                simpTheorems.addDeclToUnfold
                  (Name.str privatePrefix "kleanMapContainsModel")
              let ctx := ctx.setSimpTheorems #[simpTheorems]
              let hyps ← goal.getNondepPropHyps
              let (result, _) ← simpGoal goal ctx (fvarIdsToSimp := hyps)
              match result with
              | none => replaceMainGoal []
              | some (_, newGoal) => replaceMainGoal [newGoal]
            simp only [h, if_false] at *
            simp only [optionIsSomeIf] at ih ⊢
            exact ih

private theorem singletonPairDecompose
    (key value₁ value₂ : SortKItem) (right : SortMap) :
    ∃ remainder,
      _root_._Map_ ⟨[(key, value₁)]⟩ remainder =
          some (_Map_ ⟨[(key, value₁)]⟩ right) ∧
        _root_._Map_ ⟨[(key, value₂)]⟩ remainder =
          some (_Map_ ⟨[(key, value₂)]⟩ right) := by
  have stable := singletonConcatIsSome key value₁ value₂ right
  cases h₁ : _root_._Map_ ⟨[(key, value₁)]⟩ right with
  | none =>
      cases h₂ : _root_._Map_ ⟨[(key, value₂)]⟩ right with
      | none =>
          refine ⟨⟨[]⟩, ?_, ?_⟩
          · simp only [_Map_, h₁]
            change some (⟨_ ++ []⟩ : SortMap) = some (⟨_⟩ : SortMap)
            simp
          · simp only [_Map_, h₂]
            change some (⟨_ ++ []⟩ : SortMap) = some (⟨_⟩ : SortMap)
            simp
      | some result =>
          simp [h₁, h₂] at stable
  | some result₁ =>
      cases h₂ : _root_._Map_ ⟨[(key, value₂)]⟩ right with
      | none =>
          simp [h₁, h₂] at stable
      | some result₂ =>
          refine ⟨right, ?_, ?_⟩
          · simpa [_Map_, h₁] using h₁
          · simpa [_Map_, h₂] using h₂

private theorem seqConcatModel (left right : SortIntSeq) :
    «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» left right =
      some (intSeqConcat left right) := by
  induction left with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [
        «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»,
        _6d95c8d,
        _982236f,
        intSeqConcat,
        Option.orElse
      ]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail ih =>
      simp [
        «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»,
        _6d95c8d,
        _982236f,
        intSeqConcat,
        ih
      ]

private theorem strContainsCharModel (needle : SortInt) (haystack : SortIntSeq) :
    «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
          needle SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
        haystack =
      some (intSeqContainsChar needle haystack) := by
  induction haystack with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [
        «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
        _38142ad,
        _56a27c9,
        _e133ba2,
        «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
        _3a4bf2f,
        _5a819d8,
        _f69553d,
        notBool_,
        _17ebc68,
        _53fc758,
        intSeqContainsChar,
        guard,
        Option.orElse
      ]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail ih =>
      by_cases h : needle = head
      · subst head
        simp [
          «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
          _38142ad,
          _56a27c9,
          _e133ba2,
          «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
          _3a4bf2f,
          _5a819d8,
          _f69553d,
          notBool_,
          _17ebc68,
          _53fc758,
          _andBool_,
          _5b9db8d,
          _61fbef3,
          «_==Int_»,
          intSeqContainsChar
          , guard
          , Option.orElse
        ]
      · simp [
          beq_eq_false_iff_ne.mpr h,
          «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
          _38142ad,
          _56a27c9,
          _e133ba2,
          «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
          _3a4bf2f,
          _5a819d8,
          _f69553d,
          notBool_,
          _17ebc68,
          _53fc758,
          _andBool_,
          _5b9db8d,
          _61fbef3,
          «_==Int_»,
          intSeqContainsChar,
          h,
          ih,
          guard,
          Option.orElse
        ]
        rfl

private theorem applyNotInModel (needle : SortInt) (haystack : SortIntSeq) :
    «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        "not in"
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              needle SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» haystack)) =
      some (!intSeqContainsChar needle haystack) := by
  simp [
    «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
    _03e60c5,
    _0ae23e4,
    _0d7d6b1,
    _1c34a14,
    _1eb1e83,
    _21c3768,
    _220c8a2,
    _31a7ce9,
    _3762d3f,
    _41490e6,
    _42db81d,
    _57afa07,
    _57f520f,
    _641b30a,
    _6b454b2,
    _6b7e0d4,
    _7031c92,
    _758418c,
    _7a57b51,
    _87bf7c6,
    _882c519,
    _8a4564e,
    _9a8a33a,
    _9b4e435,
    _9d30e79,
    _9e5ad0c,
    _9ec2057,
    _9f9c54d,
    _b076352,
    _b37e75d,
    _b558675,
    _b69f73f,
    _beb7b49,
    _c0092c8,
    _c91e9fa,
    _c986c4d,
    _f10cf1b,
    _f53e67b,
    _f5cd646,
    _f64794f,
    strContainsCharModel,
    notBool_,
    _17ebc68,
    _53fc758,
    Option.orElse
  ]
  cases intSeqContainsChar needle haystack <;> rfl

private theorem applyStringAddModel (left right : SortIntSeq) :
    «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
        "+"
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left))
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right)) =
      some
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (intSeqConcat left right))) := by
  simp [
    «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
    _13d6ee6,
    _1909c2e,
    _2acce51,
    _30456db,
    _3598da3,
    _42bfa12,
    _4f03d42,
    _4f373ea,
    _50f1b5a,
    _614d946,
    _798d463,
    _7f23ecf,
    _7ff1b9f,
    _a4f5818,
    _a4f63fd,
    _a6670cb,
    _b009d60,
    _bb59890,
    _bc844c7,
    _c2eab84,
    _ca41a23,
    _d8961f0,
    _dece19f,
    _e0a3283,
    _ebcc6ed,
    _f394023,
    seqConcatModel,
    Option.orElse
  ]
  rfl

private theorem truthyBoolModel (value : Bool) :
    «truthy(_)_MPY-CORE_Bool_Val» (SortVal.inj_SortBool value) =
      some value := by
  cases value <;>
    simp [
      «truthy(_)_MPY-CORE_Bool_Val»,
      _296075e,
      _542a815,
      _a99224c,
      _e6ccd5c,
      _f05ec3f,
      _f37ebb3,
      retr,
      Option.orElse
    ]

private theorem isKResultExprValModel (value : SortVal) :
    isKResult
        (SortK.kseq
          ((@inj SortExpr SortKItem) ((@inj SortVal SortExpr) value))
          SortK.dotk) =
      some true := by
  cases value <;>
    rfl

private theorem isKResultExprBoolModel (value : Bool) :
    isKResult
        (SortK.kseq
          ((@inj SortExpr SortKItem) ((@inj SortBool SortExpr) value))
          SortK.dotk) =
      some true := by
  cases value <;>
    rfl

private def localVariables
    (original deleted forward reverse : SortIntSeq) (character : SortVal) :
    SortMap :=
  ⟨[
    (SortKItem.inj_SortString "s",
      SortKItem.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» original)),
    (SortKItem.inj_SortString "c",
      SortKItem.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» deleted)),
    (SortKItem.inj_SortString "result",
      SortKItem.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» forward)),
    (SortKItem.inj_SortString "reversed_result",
      SortKItem.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» reverse)),
    (SortKItem.inj_SortString "character",
      (@inj SortVal SortKItem) character)
  ]⟩

private theorem assembledLocalsModel
    (original deleted forward reverse : SortIntSeq) (character : SortVal) :
    _Map_
        (_Map_
          (_Map_
            (_Map_
              («_|->_»
                (SortKItem.inj_SortString "s")
                (SortKItem.inj_SortStr
                  (SortStr.«str(_)_MPY-CORE_Str_IntSeq» original)))
              («_|->_»
                (SortKItem.inj_SortString "c")
                (SortKItem.inj_SortStr
                  (SortStr.«str(_)_MPY-CORE_Str_IntSeq» deleted))))
            («_|->_»
              (SortKItem.inj_SortString "result")
              (SortKItem.inj_SortStr
                (SortStr.«str(_)_MPY-CORE_Str_IntSeq» forward))))
          («_|->_»
            (SortKItem.inj_SortString "reversed_result")
            (SortKItem.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq» reverse))))
        («_|->_»
          (SortKItem.inj_SortString "character")
          (SortKItem.inj_SortVal character)) =
      localVariables original deleted forward reverse character := by
  simp only [_Map_, «_|->_», localVariables]
  simp only [normalizeKItem]
  run_tac
    let goal ← getMainGoal
    let ctx ← Simp.Context.mkDefault
    let privatePrefix :=
      Name.num
        (Name.str
          (Name.str (Name.mkSimple "_private") "Klean112ReverseDelete")
          "Func")
        0
    let simpTheorems ← getSimpTheorems
    let simpTheorems ←
      simpTheorems.addDeclToUnfold (Name.mkSimple "_Map_")
    let simpTheorems ←
      simpTheorems.addDeclToUnfold
        (Name.str privatePrefix "kleanMapDisjointModel")
    let simpTheorems ←
      simpTheorems.addDeclToUnfold
        (Name.str privatePrefix "kleanMapContainsModel")
    let ctx := ctx.setSimpTheorems #[simpTheorems]
    let ctx ← ctx.setConfig { ctx.config with failIfUnchanged := false }
    replaceMainGoal [goal]
    for _ in [0:20] do
      match ← getGoals with
      | [] => pure ()
      | current :: _ =>
          let hyps ← current.getNondepPropHyps
          let (result, _) ←
            simpGoal current ctx (fvarIdsToSimp := hyps)
          match result with
          | none => replaceMainGoal []
          | some (_, newGoal) => replaceMainGoal [newGoal]
          evalTactic (← `(tactic| try simp))

private theorem localVariablesOps
    (original deleted forward reverse : SortIntSeq) (character newCharacter : SortVal)
    (newForward newReverse : SortIntSeq) :
    «Map:update»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "character")
        ((@inj SortVal SortKItem) newCharacter) =
          some (localVariables original deleted forward reverse newCharacter) ∧
    «Map:update»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "result")
        (SortKItem.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» newForward)) =
          some (localVariables original deleted newForward reverse character) ∧
    «Map:update»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "reversed_result")
        (SortKItem.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» newReverse)) =
          some (localVariables original deleted forward newReverse character) ∧
    «_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString "character")
        (localVariables original deleted forward reverse character) = some true ∧
    «_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString "c")
        (localVariables original deleted forward reverse character) = some true ∧
    «_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString "result")
        (localVariables original deleted forward reverse character) = some true ∧
    «_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString "reversed_result")
        (localVariables original deleted forward reverse character) = some true ∧
    «Map:lookup»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "character") =
          some ((@inj SortVal SortKItem) character) ∧
    «Map:lookup»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "c") =
          some
            (SortKItem.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq» deleted)) ∧
    «Map:lookup»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "result") =
          some
            (SortKItem.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq» forward)) ∧
    «Map:lookup»
        (localVariables original deleted forward reverse character)
        (SortKItem.inj_SortString "reversed_result") =
          some
            (SortKItem.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq» reverse)) := by
  simp only [
    localVariables,
    «Map:update»,
    «Map:lookup»,
    «_in_keys(_)_MAP_Bool_KItem_Map»
  ]
  run_tac
    let goal ← getMainGoal
    let ctx ← Simp.Context.mkDefault
    let privatePrefix :=
      Name.num
        (Name.str
          (Name.str (Name.mkSimple "_private") "Klean112ReverseDelete")
          "Func")
        0
    let simpTheorems ← getSimpTheorems
    let simpTheorems ←
      simpTheorems.addDeclToUnfold
        (Name.str privatePrefix "kleanMapContainsModel")
    let simpTheorems ←
      simpTheorems.addDeclToUnfold
        (Name.str privatePrefix "kleanMapUpdateModel")
    let simpTheorems ←
      simpTheorems.addDeclToUnfold
        (Name.str privatePrefix "kleanMapLookupModel")
    let ctx := ctx.setSimpTheorems #[simpTheorems]
    let ctx ← ctx.setConfig { ctx.config with failIfUnchanged := false }
    replaceMainGoal [goal]
    for _ in [0:20] do
      match ← getGoals with
      | [] => pure ()
      | current :: _ =>
          let hyps ← current.getNondepPropHyps
          let (result, _) ←
            simpGoal current ctx (fvarIdsToSimp := hyps)
          match result with
          | none => replaceMainGoal []
          | some (_, newGoal) => replaceMainGoal [newGoal]
          evalTactic (← `(tactic| try simp))

private def verificationLoopBody : SortStmts :=
  SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
    (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
      ((SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
            "character").«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
        (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr»
          "not in"
          (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")))
      (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
        (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
          (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result")
          "+"
          (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "character"))
        (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
          (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
            (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "reversed_result")
            (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr»
              "+"
              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "character")
              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                "reversed_result")))
          SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))
      SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
    SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»

private def verificationLoopNext (remaining : SortIntSeq) : SortK :=
  SortK.kseq
    (SortKItem.«#loop(_,_,_)_MPY-CONTROLS_KItem_Val_Expr_Stmts»
      (SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» remaining))
      (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "character")
      verificationLoopBody)
    SortK.dotk

theorem final :
    Klean112ReverseDelete.Lemmas.targetStatement _Map_ «_|->_» «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq» «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val» «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq» := by
  unfold Klean112ReverseDelete.Lemmas.targetStatement
  intro generatedCounter exitCode exc ret stack heapLoc heap scopeLoc
    scopeTail P V RA A C ORIG L continuation S
  simp only [assembledLocalsModel]
  induction S generalizing V RA A with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp only [
        «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»,
        «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val»,
        «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
      ]
      exact Rewrites.tran
        (Rewrites._c65b0f2
          (IT := SortIterable.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
        (Rewrites.tran Rewrites._7fe18de Rewrites._8e90948)
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail ih =>
      apply Rewrites.tran
      · exact Rewrites.tran
          (Rewrites._c65b0f2
            (IT := SortIterable.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  head tail))))
          (Rewrites.tran Rewrites._e024194 Rewrites._3ff423b)
      · let one :=
          SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
            head SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
        let character :=
          SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq» one)
        have operations :=
          localVariablesOps ORIG C A RA V character A RA
        rcases operations with
          ⟨updateCharacter, _, _, _, _, _, _, _, _, _, _⟩
        obtain ⟨scopeRemainder, oldScope, newScope⟩ :=
          singletonPairDecompose
            (SortKItem.inj_SortInt L)
            (SortKItem.inj_SortScope
              (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                (localVariables ORIG C A RA V) P))
            (SortKItem.inj_SortScope
              (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                (localVariables ORIG C A RA character) P))
            scopeTail
        apply Rewrites.tran
        · exact Rewrites._d5bec6c
            (M := localVariables ORIG C A RA V)
            (_DotVar2 := scopeRemainder)
            (V := character)
            (X := "character")
            (_Val2 := localVariables ORIG C A RA character)
            (by rfl)
            (by simpa [«_|->_»] using oldScope)
            (by
              change
                «Map:update»
                    (localVariables ORIG C A RA V)
                    (SortKItem.inj_SortString "character")
                    ((@inj SortVal SortKItem) character) =
                  some (localVariables ORIG C A RA character)
              exact updateCharacter)
            (by rfl)
            (by simpa [«_|->_»] using newScope)
        ·
          have currentOperations :=
            localVariablesOps ORIG C A RA character character A RA
          rcases currentOperations with
            ⟨_,
              _,
              _,
              inCharacter,
              inC,
              inResult,
              inReversedResult,
              lookupCharacter,
              lookupC,
              lookupResult,
              lookupReversedResult⟩
          apply Rewrites.tran
          · exact Rewrites._94bd14e
          · apply Rewrites.tran
            · exact
                Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
                  (by rfl) (by rfl) (by rfl) (by rfl)
            · apply Rewrites.tran
              · exact Rewrites._1f0e78f
                  (by rfl) (by rfl) (by rfl) (by rfl)
              · apply Rewrites.tran
                · exact Rewrites._6d39855
                · apply Rewrites.tran
                  · exact Rewrites._db779c6
                      (M := localVariables ORIG C A RA character)
                      (_DotVar2 := scopeRemainder)
                      (_Val4 := character)
                      (by simpa using inCharacter)
                      (by rfl)
                      (by simpa using newScope)
                      (by simpa using lookupCharacter)
                      (by rfl)
                      (by rfl)
                      (by simpa using newScope)
                      (by rfl)
                  · apply Rewrites.tran
                    · exact Rewrites._dfb9e43
                        (HOLE := (@inj SortVal SortExpr) character)
                        (isKResultExprValModel character)
                        (by rfl)
                        (by rfl)
                    · apply Rewrites.tran
                      · exact Rewrites._e1122bd
                          (HOLE :=
                            SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")
                          (_Gen0 := character)
                          (_Gen1 := "not in")
                          (by rfl) (by rfl) (by rfl) (by rfl)
                      · apply Rewrites.tran
                        · exact Rewrites._6d39855
                        · apply Rewrites.tran
                          · exact Rewrites._db779c6
                              (M := localVariables ORIG C A RA character)
                              (_DotVar2 := scopeRemainder)
                              (_Val4 :=
                                SortVal.inj_SortStr
                                  (SortStr.«str(_)_MPY-CORE_Str_IntSeq» C))
                              (by simpa using inC)
                              (by rfl)
                              (by simpa using newScope)
                              (by simpa using lookupC)
                              (by rfl)
                              (by rfl)
                              (by simpa using newScope)
                              (by rfl)
                          · apply Rewrites.tran
                            · exact Rewrites._aae3b52
                                (HOLE :=
                                  (@inj SortVal SortExpr)
                                    (SortVal.inj_SortStr
                                      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» C)))
                                (_Gen0 := character)
                                (_Gen1 := "not in")
                                (isKResultExprValModel
                                  (SortVal.inj_SortStr
                                    (SortStr.«str(_)_MPY-CORE_Str_IntSeq» C)))
                                (by rfl)
                                (by rfl)
                            · apply Rewrites.tran
                              · exact Rewrites._a00964a
                                  (applyNotInModel head C)
                              · apply Rewrites.tran
                                · exact
                                    Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
                                      (HOLE :=
                                        (@inj SortBool SortExpr)
                                          (!intSeqContainsChar head C))
                                      (isKResultExprBoolModel
                                        (!intSeqContainsChar head C))
                                      (by rfl)
                                      (by rfl)
                                · apply Rewrites.tran
                                  · exact Rewrites._c82b7aa
                                      (truthyBoolModel
                                        (!intSeqContainsChar head C))
                                  · cases h :
                                      intSeqContainsChar head C with
                                    | true =>
                                      simp only [h, Bool.not_true]
                                      apply Rewrites.tran
                                      · exact Rewrites._052f78e
                                      · apply Rewrites.tran
                                        · exact Rewrites._2a0ddee
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · exact Rewrites._d499ad9
                                                (NEXT :=
                                                  SortK.kseq
                                                    (SortKItem.«#loop(_,_,_)_MPY-CONTROLS_KItem_Val_Expr_Stmts»
                                                      (SortVal.inj_SortStr
                                                        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                          tail))
                                                      (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                        "character")
                                                      (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
                                                        (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
                                                          ((SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                "character").«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
                                                            (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr»
                                                              "not in"
                                                              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                "c")))
                                                          (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
                                                            (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
                                                              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                "result")
                                                              "+"
                                                              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                "character"))
                                                            (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
                                                              (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
                                                                (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                  "reversed_result")
                                                                (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr»
                                                                  "+"
                                                                  (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                    "character")
                                                                  (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                    "reversed_result")))
                                                              SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))
                                                          SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
                                                        SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))
                                                    SortK.dotk)
                                                (_DotVar1 := continuation)
                                                (by rfl)
                                            ·
                                              simpa [
                                                h,
                                                «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»,
                                                «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val»,
                                                «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
                                              ] using
                                                (ih character RA A)
                                    | false =>
                                      simp only [h, Bool.not_false]
                                      apply Rewrites.tran
                                      · exact Rewrites._0fd4639
                                      · apply Rewrites.tran
                                        · exact Rewrites._94bd14e
                                        · apply Rewrites.tran
                                          · exact
                                              Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_heat»
                                                (HOLE :=
                                                  SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                    "character")
                                                (K0 :=
                                                  SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                    "result")
                                                (K1 := "+")
                                                (by rfl)
                                                (by rfl)
                                                (by rfl)
                                                (by rfl)
                                          · apply Rewrites.tran
                                            · exact Rewrites._6d39855
                                            · apply Rewrites.tran
                                              · exact Rewrites._db779c6
                                                  (M :=
                                                    localVariables
                                                      ORIG C A RA character)
                                                  (_DotVar2 :=
                                                    scopeRemainder)
                                                  (_Val4 := character)
                                                  (by simpa using
                                                    inCharacter)
                                                  (by rfl)
                                                  (by simpa using newScope)
                                                  (by simpa using
                                                    lookupCharacter)
                                                  (by rfl)
                                                  (by rfl)
                                                  (by simpa using newScope)
                                                  (by rfl)
                                              · apply Rewrites.tran
                                                · exact
                                                    Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_cool»
                                                      (HOLE :=
                                                        (@inj SortVal SortExpr)
                                                          character)
                                                      (K0 :=
                                                        SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                          "result")
                                                      (K1 := "+")
                                                      (isKResultExprValModel
                                                        character)
                                                      (by rfl)
                                                      (by rfl)
                                                ·
                                                  let newForward :=
                                                    intSeqConcat A one
                                                  have forwardOperations :=
                                                    localVariablesOps
                                                      ORIG
                                                      C
                                                      A
                                                      RA
                                                      character
                                                      character
                                                      newForward
                                                      RA
                                                  rcases forwardOperations with
                                                    ⟨_,
                                                      updateResult,
                                                      _,
                                                      _,
                                                      _,
                                                      _,
                                                      _,
                                                      _,
                                                      _,
                                                      _,
                                                      _⟩
                                                  obtain
                                                      ⟨forwardRemainder,
                                                        currentScope,
                                                        forwardScope⟩ :=
                                                    singletonPairDecompose
                                                      (SortKItem.inj_SortInt
                                                        L)
                                                      (SortKItem.inj_SortScope
                                                        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                                                          (localVariables
                                                            ORIG
                                                            C
                                                            A
                                                            RA
                                                            character)
                                                          P))
                                                      (SortKItem.inj_SortScope
                                                        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                                                          (localVariables
                                                            ORIG
                                                            C
                                                            newForward
                                                            RA
                                                            character)
                                                          P))
                                                      scopeTail
                                                  apply Rewrites.tran
                                                  · exact Rewrites._460aaab
                                                      (M :=
                                                        localVariables
                                                          ORIG
                                                          C
                                                          A
                                                          RA
                                                          character)
                                                      (_DotVar2 :=
                                                        forwardRemainder)
                                                      (OP := "+")
                                                      (X := "result")
                                                      (V := character)
                                                      (_Val4 :=
                                                        SortVal.inj_SortStr
                                                          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                            A))
                                                      (_Val5 :=
                                                        SortVal.inj_SortStr
                                                          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                            newForward))
                                                      (by simpa using
                                                        inResult)
                                                      (by rfl)
                                                      (by simpa using
                                                        currentScope)
                                                      (by simpa using
                                                        lookupResult)
                                                      (by rfl)
                                                      (applyStringAddModel
                                                        A one)
                                                      (by
                                                        change
                                                          «Map:update»
                                                              (localVariables
                                                                ORIG
                                                                C
                                                                A
                                                                RA
                                                                character)
                                                              (SortKItem.inj_SortString
                                                                "result")
                                                              (SortKItem.inj_SortStr
                                                                (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                  newForward)) =
                                                            some
                                                              (localVariables
                                                                ORIG
                                                                C
                                                                newForward
                                                                RA
                                                                character)
                                                        exact updateResult)
                                                      (by rfl)
                                                      (by simpa using
                                                        forwardScope)
                                                      (by rfl)
                                                  ·
                                                    have updatedOperations :=
                                                      localVariablesOps
                                                        ORIG
                                                        C
                                                        newForward
                                                        RA
                                                        character
                                                        character
                                                        newForward
                                                        (intSeqConcat one RA)
                                                    rcases updatedOperations with
                                                      ⟨_,
                                                        _,
                                                        updateReversedResult,
                                                        inUpdatedCharacter,
                                                        _,
                                                        _,
                                                        inUpdatedReversedResult,
                                                        lookupUpdatedCharacter,
                                                        _,
                                                        _,
                                                        lookupUpdatedReversedResult⟩
                                                    let newReverse :=
                                                      intSeqConcat one RA
                                                    obtain
                                                        ⟨reverseRemainder,
                                                          updatedForwardScope,
                                                          updatedReverseScope⟩ :=
                                                      singletonPairDecompose
                                                        (SortKItem.inj_SortInt
                                                          L)
                                                        (SortKItem.inj_SortScope
                                                          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                                                            (localVariables
                                                              ORIG
                                                              C
                                                              newForward
                                                              RA
                                                              character)
                                                            P))
                                                        (SortKItem.inj_SortScope
                                                          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                                                            (localVariables
                                                              ORIG
                                                              C
                                                              newForward
                                                              newReverse
                                                              character)
                                                            P))
                                                        scopeTail
                                                    apply Rewrites.tran
                                                    · exact
                                                        Rewrites._94bd14e
                                                    · apply Rewrites.tran
                                                      · exact
                                                          Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat»
                                                            (HOLE :=
                                                              SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr»
                                                                "+"
                                                                (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                  "character")
                                                                (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                  "reversed_result"))
                                                            (K0 :=
                                                              SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                "reversed_result")
                                                            (by rfl)
                                                            (by rfl)
                                                            (by rfl)
                                                            (by rfl)
                                                      · apply Rewrites.tran
                                                        · exact
                                                            Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
                                                              (HOLE :=
                                                                SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                  "character")
                                                              (K0 := "+")
                                                              (K2 :=
                                                                SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                  "reversed_result")
                                                              (by rfl)
                                                              (by rfl)
                                                              (by rfl)
                                                              (by rfl)
                                                        · apply Rewrites.tran
                                                          · exact
                                                              Rewrites._6d39855
                                                          · apply Rewrites.tran
                                                            · exact
                                                                Rewrites._db779c6
                                                                  (M :=
                                                                    localVariables
                                                                      ORIG
                                                                      C
                                                                      newForward
                                                                      RA
                                                                      character)
                                                                  (_DotVar2 :=
                                                                    reverseRemainder)
                                                                  (_Val4 :=
                                                                    character)
                                                                  (by simpa using
                                                                    inUpdatedCharacter)
                                                                  (by rfl)
                                                                  (by simpa using
                                                                    updatedForwardScope)
                                                                  (by simpa using
                                                                    lookupUpdatedCharacter)
                                                                  (by rfl)
                                                                  (by rfl)
                                                                  (by simpa using
                                                                    updatedForwardScope)
                                                                  (by rfl)
                                                            · apply Rewrites.tran
                                                              · exact
                                                                  Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                                    (HOLE :=
                                                                      (@inj SortVal SortExpr)
                                                                        character)
                                                                    (K0 := "+")
                                                                    (K2 :=
                                                                      SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                        "reversed_result")
                                                                    (isKResultExprValModel
                                                                      character)
                                                                    (by rfl)
                                                                    (by rfl)
                                                              · apply Rewrites.tran
                                                                · exact
                                                                    Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                                      (HOLE :=
                                                                        SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                          "reversed_result")
                                                                      (K0 := "+")
                                                                      (K1 :=
                                                                        (@inj SortVal SortExpr)
                                                                          character)
                                                                      (isKResultExprValModel
                                                                        character)
                                                                      (by rfl)
                                                                      (by rfl)
                                                                      (by rfl)
                                                                      (by rfl)
                                                                      (by rfl)
                                                                · apply Rewrites.tran
                                                                  · exact
                                                                      Rewrites._6d39855
                                                                  · apply Rewrites.tran
                                                                    · exact
                                                                        Rewrites._db779c6
                                                                          (M :=
                                                                            localVariables
                                                                              ORIG
                                                                              C
                                                                              newForward
                                                                              RA
                                                                              character)
                                                                          (_DotVar2 :=
                                                                            reverseRemainder)
                                                                          (_Val4 :=
                                                                            SortVal.inj_SortStr
                                                                              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                RA))
                                                                          (by simpa using
                                                                            inUpdatedReversedResult)
                                                                          (by rfl)
                                                                          (by simpa using
                                                                            updatedForwardScope)
                                                                          (by simpa using
                                                                            lookupUpdatedReversedResult)
                                                                          (by rfl)
                                                                          (by rfl)
                                                                          (by simpa using
                                                                            updatedForwardScope)
                                                                          (by rfl)
                                                                    · apply Rewrites.tran
                                                                      · exact
                                                                          Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                                            (HOLE :=
                                                                              (@inj SortVal SortExpr)
                                                                                (SortVal.inj_SortStr
                                                                                  (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                    RA)))
                                                                            (K0 := "+")
                                                                            (K1 :=
                                                                              (@inj SortVal SortExpr)
                                                                                character)
                                                                            (isKResultExprValModel
                                                                              (SortVal.inj_SortStr
                                                                                (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                  RA)))
                                                                            (by rfl)
                                                                            (by rfl)
                                                                      · apply Rewrites.tran
                                                                        · exact
                                                                            Rewrites._d9b5bba
                                                                              (applyStringAddModel
                                                                                one
                                                                                RA)
                                                                        · apply Rewrites.tran
                                                                          · exact
                                                                              Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
                                                                                (HOLE :=
                                                                                  (@inj SortVal SortExpr)
                                                                                    (SortVal.inj_SortStr
                                                                                      (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                        newReverse)))
                                                                                (K0 :=
                                                                                  SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                                                                                    "reversed_result")
                                                                                (isKResultExprValModel
                                                                                  (SortVal.inj_SortStr
                                                                                    (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                      newReverse)))
                                                                                (by rfl)
                                                                                (by rfl)
                                                                          · apply Rewrites.tran
                                                                            · exact
                                                                                Rewrites._e6f504a
                                                                                  (M :=
                                                                                    localVariables
                                                                                      ORIG
                                                                                      C
                                                                                      newForward
                                                                                      RA
                                                                                      character)
                                                                                  (_DotVar2 :=
                                                                                    reverseRemainder)
                                                                                  (V :=
                                                                                    SortVal.inj_SortStr
                                                                                      (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                        newReverse))
                                                                                  (X :=
                                                                                    "reversed_result")
                                                                                  (by rfl)
                                                                                  (by simpa using
                                                                                    updatedForwardScope)
                                                                                  (by
                                                                                    change
                                                                                      «Map:update»
                                                                                          (localVariables
                                                                                            ORIG
                                                                                            C
                                                                                            newForward
                                                                                            RA
                                                                                            character)
                                                                                          (SortKItem.inj_SortString
                                                                                            "reversed_result")
                                                                                          (SortKItem.inj_SortStr
                                                                                            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                                                                                              newReverse)) =
                                                                                        some
                                                                                          (localVariables
                                                                                            ORIG
                                                                                            C
                                                                                            newForward
                                                                                            newReverse
                                                                                            character)
                                                                                    exact
                                                                                      updateReversedResult)
                                                                                  (by rfl)
                                                                                  (by simpa using
                                                                                    updatedReverseScope)
                                                                            · apply Rewrites.tran
                                                                              · exact
                                                                                  Rewrites._2a0ddee
                                                                              · apply Rewrites.tran
                                                                                · exact
                                                                                    Rewrites._2a0ddee
                                                                                · apply Rewrites.tran
                                                                                  · exact
                                                                                      Rewrites._d499ad9
                                                                                        (NEXT :=
                                                                                          verificationLoopNext
                                                                                            tail)
                                                                                        (_DotVar1 :=
                                                                                          continuation)
                                                                                        (by rfl)
                                                                                  ·
                                                                                    simpa [
                                                                                      h,
                                                                                      one,
                                                                                      character,
                                                                                      newForward,
                                                                                      newReverse,
                                                                                      verificationLoopNext,
                                                                                      verificationLoopBody,
                                                                                      intSeqConcat,
                                                                                      «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»,
                                                                                      «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val»,
                                                                                      «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq»
                                                                                    ] using
                                                                                      (ih
                                                                                        character
                                                                                        newReverse
                                                                                        newForward)

end Proof
