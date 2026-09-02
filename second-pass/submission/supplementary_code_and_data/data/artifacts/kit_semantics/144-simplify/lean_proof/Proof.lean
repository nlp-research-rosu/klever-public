import Klean144Simplify.Lemmas
import Lean.Elab.Tactic.Unfold

namespace Proof

open Lean Elab Tactic

set_option maxHeartbeats 5000000
set_option Elab.async false
set_option linter.unusedSimpArgs false

/- The generated map model is private to `Func.lean`.  This proof-only tactic
   unfolds those exact generated definitions by their environment names; it
   introduces no equations or trusted facts. -/
elab "candidateUnfoldMapModels" : tactic => withMainContext do
  let env ← getEnv
  let mut changed := false
  for (name, _) in env.constants.toList do
    match name with
    | .str _ suffix =>
      if suffix = "kleanMapLookupModel" ||
         suffix = "kleanMapContainsModel" ||
         suffix = "kleanMapDisjointModel" ||
         suffix = "kleanMapDeleteModel" ||
         suffix = "kleanKeyOrderModel" ||
         suffix = "kleanMapInsertModel" ||
         suffix = "kleanMapUpdateModel" then
        try
          unfoldTarget name
          changed := true
        catch _ => pure ()
    | _ => pure ()
  if !changed then
    throwError "no generated private map model could be unfolded"

elab "candidateUnfoldMapUpdate" : tactic => withMainContext do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    match name with
    | .str _ suffix =>
      if suffix = "kleanMapUpdateModel" then
        try unfoldTarget name catch _ => pure ()
    | _ => pure ()

elab "candidateUnfoldMapDelete" : tactic => withMainContext do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    match name with
    | .str _ suffix =>
      if suffix = "kleanMapDeleteModel" then
        try unfoldTarget name catch _ => pure ()
    | _ => pure ()

elab "candidateUnfoldMapInsert" : tactic => withMainContext do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    match name with
    | .str _ suffix =>
      if suffix = "kleanMapInsertModel" || suffix = "kleanKeyOrderModel" then
        try unfoldTarget name catch _ => pure ()
    | _ => pure ()

/- KORE symbol: Lbl'Stop'List; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «.List» : SortList := ⟨[]⟩
/- KORE symbol: Lbl'Stop'Map; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «.Map» : SortMap := ⟨[]⟩
/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable local instance candidateKItemDecEq : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def candidateMapContains
    (entries : List (SortKItem × SortKItem)) (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true else candidateMapContains rest key

private noncomputable def candidateMapsDisjoint
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if candidateMapContains left key then false
      else candidateMapsDisjoint left rest

private noncomputable def candidateKeyBefore : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortInt left, SortKItem.inj_SortInt right => decide (left < right)
  | SortKItem.inj_SortInt _, _ => true
  | _, SortKItem.inj_SortInt _ => false
  | SortKItem.inj_SortString left, SortKItem.inj_SortString right =>
      decide (left < right)
  | SortKItem.inj_SortString _, _ => true
  | _, SortKItem.inj_SortString _ => false
  | _, _ => false

private noncomputable def candidateMapInsert
    (key value : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidateKeyBefore candidate key then
        (candidate, oldValue) :: candidateMapInsert key value rest
      else (key, value) :: (candidate, oldValue) :: rest

private noncomputable def candidateCanonicalMap
    (entries : List (SortKItem × SortKItem)) : SortMap :=
  ⟨entries.foldr (fun kv acc => candidateMapInsert kv.1 kv.2 acc) []⟩

noncomputable def _Map_ (left right : SortMap) : SortMap :=
  (_root_._Map_ left right).getD «.Map»
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool := decide (left < right)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool := decide (left ≤ right)
/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_==K_» (left right : SortK) : SortBool :=
  @decide (left = right) (Classical.propDecidable _)
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_|->_» (key value : SortKItem) : SortMap :=
  (_root_.«_|->_» key value).getD «.Map»
/- KORE symbol: LblListItem; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def ListItem (item : SortKItem) : SortList := ⟨[item]⟩
private noncomputable def candidateBuiltinBindings : SortMap :=
  ⟨[
      (SortKItem.inj_SortString "abs", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs")),
      (SortKItem.inj_SortString "all", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all")),
      (SortKItem.inj_SortString "any", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any")),
      (SortKItem.inj_SortString "bin", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin")),
      (SortKItem.inj_SortString "chr", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr")),
      (SortKItem.inj_SortString "enumerate", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate")),
      (SortKItem.inj_SortString "eval", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval")),
      (SortKItem.inj_SortString "float", SortKItem.inj_SortVal (SortVal.«typeV(_)_MPY-CORE_Val_String» "float")),
      (SortKItem.inj_SortString "int", SortKItem.inj_SortVal (SortVal.«typeV(_)_MPY-CORE_Val_String» "int")),
      (SortKItem.inj_SortString "isinstance", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance")),
      (SortKItem.inj_SortString "len", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")),
      (SortKItem.inj_SortString "list", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list")),
      (SortKItem.inj_SortString "map", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map")),
      (SortKItem.inj_SortString "max", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max")),
      (SortKItem.inj_SortString "min", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min")),
      (SortKItem.inj_SortString "ord", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord")),
      (SortKItem.inj_SortString "range", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range")),
      (SortKItem.inj_SortString "round", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round")),
      (SortKItem.inj_SortString "set", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set")),
      (SortKItem.inj_SortString "sorted", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted")),
      (SortKItem.inj_SortString "str", SortKItem.inj_SortVal (SortVal.«typeV(_)_MPY-CORE_Val_String» "str")),
      (SortKItem.inj_SortString "sum", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")),
      (SortKItem.inj_SortString "zip", SortKItem.inj_SortVal (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip"))
  ]⟩

/- KORE symbol: LblbuiltinsScope'Unds'MPY-CORE'Unds'Scope; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «builtinsScope_MPY-CORE_Scope» : SortScope :=
  SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» candidateBuiltinBindings
    SortParent.«root_MPY-CORE_Parent»
/- KORE symbol: LblisDigitC'LParUndsRParUnds'MPY-METHODS'Unds'Bool'Unds'Int; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isDigitC(_)_MPY-METHODS_Bool_Int» (code : SortInt) : SortBool :=
  decide (48 ≤ code ∧ code ≤ 57)
/- KORE symbol: LblscanResult'LParUndsCommUndsCommUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'IntSeq'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
private def pythonModuloTotal (left right : SortInt) : SortInt :=
  if right = 0 then 0
  else Int.tmod (Int.tmod left right + right) right

def «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» :
    SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», phase, a, b, c, d =>
      if phase = 3 ∧ 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d then
        decide (pythonModuloTotal (a * c) (b * d) = 0)
      else false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      phase, a, b, c, d =>
      if code = 47 ∧ 0 ≤ phase ∧ phase < 3 then
        «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest (phase + 1) a b c d
      else if «isDigitC(_)_MPY-METHODS_Bool_Int» code then
        if phase = 0 then
          «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 0 (a * 10 + (code - 48)) b c d
        else if phase = 1 then
          «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 1 a (b * 10 + (code - 48)) c d
        else if phase = 2 then
          «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 2 a b (c * 10 + (code - 48)) d
        else if phase = 3 then
          «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 3 a b c (d * 10 + (code - 48))
        else false
      else false
/- KORE symbol: LblsimplifyLoopBody'Unds'VERIFICATION-SYNTAX'Unds'Stmts; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «simplifyLoopBody_VERIFICATION-SYNTAX_Stmts» : SortStmts :=
  _root_.«simplifyLoopBody_VERIFICATION-SYNTAX_Stmts».getD
    SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»
/- KORE symbol: LblsimplifyReturn'Unds'VERIFICATION-SYNTAX'Unds'Stmt; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «simplifyReturn_VERIFICATION-SYNTAX_Stmt» : SortStmt :=
  _root_.«simplifyReturn_VERIFICATION-SYNTAX_Stmt».getD
    (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» false))
/- KORE symbol: LblsimplifyScope'LParUndsCommUndsCommUndsCommUndsCommUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Scope'Unds'Val'Unds'Val'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Val; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
private noncomputable def candidateLocalBindings
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortMap :=
  ⟨[
    (SortKItem.inj_SortString "a", SortKItem.inj_SortInt a),
    (SortKItem.inj_SortString "b", SortKItem.inj_SortInt b),
    (SortKItem.inj_SortString "c", SortKItem.inj_SortInt c),
    (SortKItem.inj_SortString "ch", (@inj SortVal SortKItem) ch),
    (SortKItem.inj_SortString "d", SortKItem.inj_SortInt d),
    (SortKItem.inj_SortString "n", (@inj SortVal SortKItem) n),
    (SortKItem.inj_SortString "part", SortKItem.inj_SortInt phase),
    (SortKItem.inj_SortString "x", (@inj SortVal SortKItem) x)
  ]⟩

noncomputable def «simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortScope :=
  SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
    (candidateLocalBindings x n phase a b c d ch)
    (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
/- KORE symbol: LblvalidScan'LParUndsCommUndsCommUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'IntSeq'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543, rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» :
    SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», phase, a, b, c, d =>
      decide (phase = 3 ∧ 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d)
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      phase, a, b, c, d =>
      if phase = 0 then
        (decide (code = 47) && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 1 a b c d) ||
        («isDigitC(_)_MPY-METHODS_Bool_Int» code && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 0 (a * 10 + (code - 48)) b c d)
      else if phase = 1 then
        (decide (code = 47) && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 2 a b c d) ||
        («isDigitC(_)_MPY-METHODS_Bool_Int» code && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 1 a (b * 10 + (code - 48)) c d)
      else if phase = 2 then
        (decide (code = 47) && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 3 a b c d) ||
        («isDigitC(_)_MPY-METHODS_Bool_Int» code && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 2 a b (c * 10 + (code - 48)) d)
      else if phase = 3 then
        «isDigitC(_)_MPY-METHODS_Bool_Int» code && «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» rest 3 a b c (d * 10 + (code - 48))
      else false

private noncomputable def candidatePersistentScopes : SortMap :=
  ⟨[
    (SortKItem.inj_SortInt (-1),
      SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»),
    (SortKItem.inj_SortInt 0,
      SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
          (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1))))
  ]⟩

private noncomputable def candidateCalleeSingleton
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortMap :=
  ⟨[(SortKItem.inj_SortInt 1,
    SortKItem.inj_SortScope
      («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
        x n phase a b c d ch))]⟩

private noncomputable def candidateActiveScopes
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortMap :=
  ⟨[
    (SortKItem.inj_SortInt (-1),
      SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»),
    (SortKItem.inj_SortInt 0,
      SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
          (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))),
    (SortKItem.inj_SortInt 1,
      SortKItem.inj_SortScope
        («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
          x n phase a b c d ch))
  ]⟩

private noncomputable def candidateRootSingleton : SortMap :=
  ⟨[(SortKItem.inj_SortInt 0,
    SortKItem.inj_SortScope
      (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
        (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1))))]⟩

private noncomputable def candidateWithoutRoot
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortMap :=
  ⟨[
    (SortKItem.inj_SortInt (-1),
      SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»),
    (SortKItem.inj_SortInt 1,
      SortKItem.inj_SortScope
        («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
          x n phase a b c d ch))
  ]⟩

private noncomputable def candidateBuiltinSingleton : SortMap :=
  ⟨[(SortKItem.inj_SortInt (-1),
    SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»)]⟩

private noncomputable def candidateWithoutBuiltins
    (x n : SortVal) (phase a b c d : SortInt) (ch : SortVal) : SortMap :=
  ⟨[
    (SortKItem.inj_SortInt 0,
      SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
          (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))),
    (SortKItem.inj_SortInt 1,
      SortKItem.inj_SortScope
        («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
          x n phase a b c d ch))
  ]⟩

private def candidateCharValue (code : SortInt) : SortVal :=
  SortVal.inj_SortStr
    (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))

private noncomputable def candidateLoopStart
    (codes : SortIntSeq) (xarg narg : SortVal)
    (phase a b c d : SortInt) (oldch : SortVal)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    SortGeneratedTopCell :=
  {
    k := { val := (
      SortK.kseq
        (SortKItem.«#loop(_,_,_)_MPY-CONTROLS_KItem_Val_Expr_Stmts»
          (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
          (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "ch")
          «simplifyLoopBody_VERIFICATION-SYNTAX_Stmts»)
        (SortK.kseq
          (SortKItem.inj_SortStmts
            (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
              «simplifyReturn_VERIFICATION-SYNTAX_Stmt»
              SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))
          (SortK.kseq SortKItem.«#endcall_MPY-FUNCTIONS_KItem» SortK.dotk))) },
    env := { val := 1 },
    scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
    scopeLoc := { val := 2 },
    heap := { val := «.Map» },
    heapLoc := { val := 0 },
    stack := { val := (ListItem
      (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int» SortK.dotk 0 1)) },
    ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
    exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
    exitCode := exitCode,
    generatedCounter := counter
  }

private noncomputable def candidateLoopEnd
    (result : SortBool) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) : SortGeneratedTopCell :=
  {
    k := { val := SortK.kseq (SortKItem.inj_SortBool result) SortK.dotk },
    env := { val := 0 },
    scopes := { val := candidatePersistentScopes },
    scopeLoc := { val := 1 },
    heap := { val := «.Map» },
    heapLoc := { val := 0 },
    stack := { val := «.List» },
    ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
    exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
    exitCode := exitCode,
    generatedCounter := counter
  }

private noncomputable def candidateLiveState
    (kont : SortK) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    SortGeneratedTopCell :=
  {
    k := { val := kont }, env := { val := 1 },
    scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
    scopeLoc := { val := 2 }, heap := { val := «.Map» },
    heapLoc := { val := 0 },
    stack := { val :=
      (ListItem (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
        SortK.dotk 0 1)) },
    ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
    exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
    exitCode := exitCode, generatedCounter := counter
  }

set_option maxHeartbeats 10000000 in
private theorem candidateMergeActive
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _root_._Map_
        (candidateCalleeSingleton xarg narg phase a b c d ch)
        candidatePersistentScopes =
      some (candidateActiveScopes xarg narg phase a b c d ch) := by
  unfold _root_._Map_
  unfold candidateCalleeSingleton candidatePersistentScopes
    candidateActiveScopes
    «simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true, eq_self]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true, eq_self]

private theorem candidateMergeRoot
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _root_._Map_ candidateRootSingleton
        (candidateWithoutRoot xarg narg phase a b c d ch) =
      some (candidateActiveScopes xarg narg phase a b c d ch) := by
  unfold _root_._Map_ candidateRootSingleton candidateWithoutRoot
    candidateActiveScopes
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false]
  candidateUnfoldMapModels

  simp

private theorem candidateMergeBuiltins
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _root_._Map_ candidateBuiltinSingleton
        (candidateWithoutBuiltins xarg narg phase a b c d ch) =
      some (candidateActiveScopes xarg narg phase a b c d ch) := by
  unfold _root_._Map_ candidateBuiltinSingleton candidateWithoutBuiltins
    candidateActiveScopes
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false]
  candidateUnfoldMapModels
  simp

macro "candidateMapSolve" : tactic =>
  `(tactic|
    first
    | rfl
    | (
      try simp_all [_root_._Map_, _root_.«_|->_»,
        «Map:update», «Map:lookup», «_in_keys(_)_MAP_Bool_KItem_Map»,
        «_[_<-undef]», _root_.ListItem, _root_._List_,
        candidateLocalBindings, candidateCalleeSingleton,
        candidateRootSingleton, candidateWithoutRoot,
        candidateBuiltinSingleton, candidateWithoutBuiltins,
        candidateBuiltinBindings,
        candidatePersistentScopes, candidateActiveScopes, «.Map», «.List»,
        instInjSortIntSortKItem]
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [candidateLocalBindings, candidateCalleeSingleton,
        candidateRootSingleton, candidateWithoutRoot,
        candidateBuiltinSingleton, candidateWithoutBuiltins,
        candidateBuiltinBindings,
        candidatePersistentScopes, candidateActiveScopes, «.Map», «.List»,
        instInjSortIntSortKItem])
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [instInjSortIntSortKItem])
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [instInjSortIntSortKItem])
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [instInjSortIntSortKItem])
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [instInjSortIntSortKItem])
      all_goals (try candidateUnfoldMapModels)
      all_goals (try simp_all [instInjSortIntSortKItem])
      all_goals done))

set_option maxHeartbeats 10000000 in
private theorem candidateLookupA
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "a" 1) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq (SortKItem.inj_SortInt a) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._db779c6
    (L := 1) (X := "a")
    (M := candidateLocalBindings xarg narg phase a b c d oldch)
    (_DotVar2 := candidatePersistentScopes)
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := true)
    (_Val1 := candidateCalleeSingleton xarg narg phase a b c d oldch)
    (_Val2 := candidateActiveScopes xarg narg phase a b c d oldch)
    (_Val3 := SortKItem.inj_SortInt a)
    (_Val4 := SortVal.inj_SortInt a)
    (_Val5 := candidateCalleeSingleton xarg narg phase a b c d oldch)
    (_Val6 := candidateActiveScopes xarg narg phase a b c d oldch)
  case defn_Val0 =>
    unfold «_in_keys(_)_MAP_Bool_KItem_Map»
    candidateUnfoldMapModels
    simp [candidateLocalBindings, inj]
    left
    rfl
  case defn_Val1 =>
    rfl
  case defn_Val2 =>
    exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val3 =>
    unfold «Map:lookup»
    candidateUnfoldMapModels
    simp [candidateLocalBindings, inj]
    intro h
    exact (h rfl).elim
  case defn_Val4 => rfl
  case defn_Val5 =>
    rfl
  case defn_Val6 =>
    exact candidateMergeActive _ _ _ _ _ _ _ _
  case req => rfl

set_option maxHeartbeats 10000000 in
private theorem candidateLookupInt
    (field : SortString) (value : SortInt)
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell)
    (hContains :
      «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString field)
        (candidateLocalBindings xarg narg phase a b c d oldch) = some true)
    (hLookup :
      «Map:lookup» (candidateLocalBindings xarg narg phase a b c d oldch)
        (SortKItem.inj_SortString field) = some (SortKItem.inj_SortInt value)) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» field 1) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := SortK.kseq (SortKItem.inj_SortInt value) cont },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._db779c6
    (L := 1) (X := field)
    (M := candidateLocalBindings xarg narg phase a b c d oldch)
    (_DotVar2 := candidatePersistentScopes)
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := true)
    (_Val1 := candidateCalleeSingleton xarg narg phase a b c d oldch)
    (_Val2 := candidateActiveScopes xarg narg phase a b c d oldch)
    (_Val3 := SortKItem.inj_SortInt value)
    (_Val4 := SortVal.inj_SortInt value)
    (_Val5 := candidateCalleeSingleton xarg narg phase a b c d oldch)
    (_Val6 := candidateActiveScopes xarg narg phase a b c d oldch)
  case defn_Val0 => exact hContains
  case defn_Val1 => rfl
  case defn_Val2 =>
    exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val3 => exact hLookup
  case defn_Val4 => rfl
  case defn_Val5 => rfl
  case defn_Val6 =>
    exact candidateMergeActive _ _ _ _ _ _ _ _
  case req => rfl

private theorem candidateContainsC
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "c")
      (candidateLocalBindings xarg narg phase a b c d oldch) = some true := by
  unfold «_in_keys(_)_MAP_Bool_KItem_Map»
  candidateUnfoldMapModels
  simp [candidateLocalBindings, inj]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateMapLookupC
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «Map:lookup» (candidateLocalBindings xarg narg phase a b c d oldch)
      (SortKItem.inj_SortString "c") = some (SortKItem.inj_SortInt c) := by
  unfold «Map:lookup»
  candidateUnfoldMapModels
  simp [candidateLocalBindings, inj]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateContainsB
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "b")
      (candidateLocalBindings xarg narg phase a b c d oldch) = some true := by
  unfold «_in_keys(_)_MAP_Bool_KItem_Map»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp

private theorem candidateMapLookupB
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «Map:lookup» (candidateLocalBindings xarg narg phase a b c d oldch)
      (SortKItem.inj_SortString "b") = some (SortKItem.inj_SortInt b) := by
  unfold «Map:lookup»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp

private theorem candidateContainsD
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "d")
      (candidateLocalBindings xarg narg phase a b c d oldch) = some true := by
  unfold «_in_keys(_)_MAP_Bool_KItem_Map»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateMapLookupD
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «Map:lookup» (candidateLocalBindings xarg narg phase a b c d oldch)
      (SortKItem.inj_SortString "d") = some (SortKItem.inj_SortInt d) := by
  unfold «Map:lookup»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateContainsPart
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "part")
      (candidateLocalBindings xarg narg phase a b c d oldch) = some true := by
  unfold «_in_keys(_)_MAP_Bool_KItem_Map»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateMapLookupPart
    (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal) :
    «Map:lookup» (candidateLocalBindings xarg narg phase a b c d oldch)
      (SortKItem.inj_SortString "part") = some (SortKItem.inj_SortInt phase) := by
  unfold «Map:lookup»
  candidateUnfoldMapModels
  simp [candidateLocalBindings]
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp
  candidateUnfoldMapModels
  simp

private theorem candidateLookupCh
    (code : SortInt) (xarg narg : SortVal) (phase a b c d : SortInt)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ch" 1) cont) },
        env := env,
        scopes := { val := (candidateActiveScopes xarg narg phase a b c d
          (candidateCharValue code)) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          ((@inj SortVal SortKItem) (candidateCharValue code)) cont) },
        env := env,
        scopes := { val := (candidateActiveScopes xarg narg phase a b c d
          (candidateCharValue code)) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._db779c6
    (L := 1) (X := "ch")
    (M := candidateLocalBindings xarg narg phase a b c d
      (candidateCharValue code))
    (_DotVar2 := candidatePersistentScopes)
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := true)
    (_Val1 := candidateCalleeSingleton xarg narg phase a b c d
      (candidateCharValue code))
    (_Val2 := candidateActiveScopes xarg narg phase a b c d
      (candidateCharValue code))
    (_Val3 := (@inj SortVal SortKItem) (candidateCharValue code))
    (_Val4 := candidateCharValue code)
    (_Val5 := candidateCalleeSingleton xarg narg phase a b c d
      (candidateCharValue code))
    (_Val6 := candidateActiveScopes xarg narg phase a b c d
      (candidateCharValue code))
  case defn_Val0 =>
    have hString : (inj ("ch" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ch" := by rfl
    rw [hString]
    unfold «_in_keys(_)_MAP_Bool_KItem_Map»
    candidateUnfoldMapModels
    simp [candidateLocalBindings, candidateCharValue]
    candidateUnfoldMapModels
    simp
    candidateUnfoldMapModels
    simp
    candidateUnfoldMapModels
    simp
  case defn_Val1 => rfl
  case defn_Val2 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val3 =>
    have hString : (inj ("ch" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ch" := by rfl
    rw [hString]
    unfold «Map:lookup»
    candidateUnfoldMapModels
    simp [candidateLocalBindings, candidateCharValue]
    candidateUnfoldMapModels
    simp
    candidateUnfoldMapModels
    simp
    candidateUnfoldMapModels
    simp
  case defn_Val4 => rfl
  case defn_Val5 => rfl
  case defn_Val6 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case req => rfl

private theorem candidateLookOrdFromLocal
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" 1) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" 0) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._10452d5
    (L := 1) (P := 0) (X := "ord")
    (M := candidateLocalBindings xarg narg phase a b c d ch)
    (_DotVar2 := candidatePersistentScopes)
    (_Val0 := false) (_Val1 := true)
    (_Val2 := candidateCalleeSingleton xarg narg phase a b c d ch)
    (_Val3 := candidateActiveScopes xarg narg phase a b c d ch)
    (_Val4 := candidateCalleeSingleton xarg narg phase a b c d ch)
    (_Val5 := candidateActiveScopes xarg narg phase a b c d ch)
  case defn_Val0 =>
    have hString : (inj ("ord" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ord" := by rfl
    rw [hString]
    unfold «_in_keys(_)_MAP_Bool_KItem_Map»
    repeat
      candidateUnfoldMapModels
      simp [candidateLocalBindings]
  case defn_Val1 => candidateMapSolve
  case defn_Val2 => candidateMapSolve
  case defn_Val3 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val4 => candidateMapSolve
  case defn_Val5 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case req => rfl

private theorem candidateLookOrdFromRoot
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" 0) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" (-1)) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._10452d5
    (L := 0) (P := -1) (X := "ord") (M := «.Map»)
    (_DotVar2 := candidateWithoutRoot xarg narg phase a b c d ch)
    (_Val0 := false) (_Val1 := true)
    (_Val2 := candidateRootSingleton)
    (_Val3 := candidateActiveScopes xarg narg phase a b c d ch)
    (_Val4 := candidateRootSingleton)
    (_Val5 := candidateActiveScopes xarg narg phase a b c d ch)
  case defn_Val0 =>
    have hString : (inj ("ord" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ord" := by rfl
    rw [hString]
    unfold «_in_keys(_)_MAP_Bool_KItem_Map»
    repeat
      candidateUnfoldMapModels
      simp [«.Map»]
  case defn_Val1 => candidateMapSolve
  case defn_Val2 => candidateMapSolve
  case defn_Val3 => exact candidateMergeRoot _ _ _ _ _ _ _ _
  case defn_Val4 => candidateMapSolve
  case defn_Val5 => exact candidateMergeRoot _ _ _ _ _ _ _ _
  case req => rfl

private theorem candidateLookOrdFromBuiltins
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" (-1)) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          ((@inj SortVal SortKItem)
            (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord")) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._db779c6
    (L := -1) (X := "ord") (M := candidateBuiltinBindings)
    (_DotVar2 := candidateWithoutBuiltins xarg narg phase a b c d ch)
    (_Gen0 := SortParent.«root_MPY-CORE_Parent»)
    (_Val0 := true) (_Val1 := candidateBuiltinSingleton)
    (_Val2 := candidateActiveScopes xarg narg phase a b c d ch)
    (_Val3 := SortKItem.inj_SortVal
      (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"))
    (_Val4 := SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord")
    (_Val5 := candidateBuiltinSingleton)
    (_Val6 := candidateActiveScopes xarg narg phase a b c d ch)
  case defn_Val0 =>
    have hString : (inj ("ord" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ord" := by rfl
    rw [hString]
    unfold «_in_keys(_)_MAP_Bool_KItem_Map»
    repeat
      candidateUnfoldMapModels
      simp [candidateBuiltinBindings]
  case defn_Val1 => candidateMapSolve
  case defn_Val2 => exact candidateMergeBuiltins _ _ _ _ _ _ _ _
  case defn_Val3 =>
    have hString : (inj ("ord" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ord" := by rfl
    rw [hString]
    unfold «Map:lookup»
    repeat
      candidateUnfoldMapModels
      simp [candidateBuiltinBindings]
  case defn_Val4 => rfl
  case defn_Val5 => rfl
  case defn_Val6 => exact candidateMergeBuiltins _ _ _ _ _ _ _ _
  case req => rfl

private theorem candidateLookupOrd
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal)
    (cont : SortK) (env : SortEnvCell) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int» "ord" 1) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          ((@inj SortVal SortKItem)
            (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord")) cont) },
        env := env,
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites.tran
  · exact candidateLookOrdFromLocal _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
  · apply Rewrites.tran
    · exact candidateLookOrdFromRoot _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    · exact candidateLookOrdFromBuiltins _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

private theorem candidateUpdateCh
    (code : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (oldch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d oldch)
        (SortKItem.inj_SortString "ch")
        ((@inj SortVal SortKItem) (candidateCharValue code)) =
      some (candidateLocalBindings xarg narg phase a b c d
        (candidateCharValue code)) := by
  unfold «Map:update»
  unfold candidateLocalBindings candidateCharValue
  candidateUnfoldMapUpdate
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  candidateUnfoldMapDelete
  simp
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  candidateUnfoldMapInsert
  simp

macro "candidateLocalUpdateSolve" : tactic =>
  `(tactic|
    (unfold «Map:update» candidateLocalBindings
     candidateUnfoldMapUpdate
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     candidateUnfoldMapDelete
     simp
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     candidateUnfoldMapInsert
     simp))

private theorem candidateUpdatePart
    (newPhase : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
        (SortKItem.inj_SortString "part")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newPhase)) =
      some (candidateLocalBindings xarg narg newPhase a b c d ch) := by
  candidateLocalUpdateSolve
  unfold inj
  rfl

private theorem candidateUpdateA
    (newA : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
        (SortKItem.inj_SortString "a")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newA)) =
      some (candidateLocalBindings xarg narg phase newA b c d ch) := by
  candidateLocalUpdateSolve
  unfold inj
  rfl

private theorem candidateUpdateB
    (newB : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
        (SortKItem.inj_SortString "b")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newB)) =
      some (candidateLocalBindings xarg narg phase a newB c d ch) := by
  candidateLocalUpdateSolve
  unfold inj
  rfl

private theorem candidateUpdateC
    (newC : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
        (SortKItem.inj_SortString "c")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newC)) =
      some (candidateLocalBindings xarg narg phase a b newC d ch) := by
  candidateLocalUpdateSolve
  unfold inj
  rfl

private theorem candidateUpdateD
    (newD : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal) :
    «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
        (SortKItem.inj_SortString "d")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newD)) =
      some (candidateLocalBindings xarg narg phase a b c newD ch) := by
  candidateLocalUpdateSolve
  unfold inj
  rfl

private theorem candidateBindCh
    (code : SortInt) (xarg narg : SortVal)
    (phase a b c d : SortInt) (oldch : SortVal)
    (cont : SortK) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#bindTgt(_,_)_MPY-TUPLE_KItem_Expr_Val»
            (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "ch")
            (candidateCharValue code)) cont) },
        env := { val := 1 },
        scopes := { val := candidateActiveScopes xarg narg phase a b c d oldch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := cont },
        env := { val := 1 },
        scopes := { val := (candidateActiveScopes xarg narg phase a b c d
          (candidateCharValue code)) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._d5bec6c
    (L := 1)
    (M := candidateLocalBindings xarg narg phase a b c d oldch)
    (_DotVar2 := candidatePersistentScopes)
    (V := candidateCharValue code) (X := "ch")
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := candidateCalleeSingleton xarg narg phase a b c d oldch)
    (_Val1 := candidateActiveScopes xarg narg phase a b c d oldch)
    (_Val2 := candidateLocalBindings xarg narg phase a b c d
      (candidateCharValue code))
    (_Val3 := candidateCalleeSingleton xarg narg phase a b c d
      (candidateCharValue code))
    (_Val4 := candidateActiveScopes xarg narg phase a b c d
      (candidateCharValue code))
  case defn_Val0 =>
    unfold _root_.«_|->_» candidateCalleeSingleton
    rfl
  case defn_Val1 =>
    exact candidateMergeActive xarg narg phase a b c d oldch
  case defn_Val2 =>
    have hString : (inj ("ch" : SortString) : SortKItem) =
        SortKItem.inj_SortString "ch" := by rfl
    rw [hString]
    exact candidateUpdateCh code xarg narg phase a b c d oldch
  case defn_Val3 =>
    unfold _root_.«_|->_» candidateCalleeSingleton
    rfl
  case defn_Val4 =>
    exact candidateMergeActive xarg narg phase a b c d (candidateCharValue code)

private theorem candidateBindInt
    (field : SortString) (value : SortInt)
    (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal)
    (newPhase newA newB newC newD : SortInt)
    (cont : SortK) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell)
    (hUpdate :
      «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
          (SortKItem.inj_SortString field)
          ((@inj SortVal SortKItem) (SortVal.inj_SortInt value)) =
        some (candidateLocalBindings xarg narg
          newPhase newA newB newC newD ch)) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.«#bindTgt(_,_)_MPY-TUPLE_KItem_Expr_Val»
            (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» field)
            (SortVal.inj_SortInt value)) cont) },
        env := { val := 1 },
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := cont }, env := { val := 1 },
        scopes := { val := (candidateActiveScopes xarg narg
          newPhase newA newB newC newD ch) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._d5bec6c
    (L := 1)
    (M := candidateLocalBindings xarg narg phase a b c d ch)
    (_DotVar2 := candidatePersistentScopes)
    (V := SortVal.inj_SortInt value) (X := field)
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := candidateCalleeSingleton xarg narg phase a b c d ch)
    (_Val1 := candidateActiveScopes xarg narg phase a b c d ch)
    (_Val2 := candidateLocalBindings xarg narg
      newPhase newA newB newC newD ch)
    (_Val3 := candidateCalleeSingleton xarg narg
      newPhase newA newB newC newD ch)
    (_Val4 := candidateActiveScopes xarg narg
      newPhase newA newB newC newD ch)
  case defn_Val0 => rfl
  case defn_Val1 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val2 =>
    have hString : (inj field : SortKItem) =
        SortKItem.inj_SortString field := by rfl
    rw [hString]
    exact hUpdate
  case defn_Val3 => rfl
  case defn_Val4 => exact candidateMergeActive _ _ _ _ _ _ _ _

private theorem candidateAssignInt
    (field : SortString) (value : SortInt)
    (xarg narg : SortVal)
    (phase a b c d : SortInt) (ch : SortVal)
    (newPhase newA newB newC newD : SortInt)
    (cont : SortK) (scopeLoc : SortScopeLocCell)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell)
    (hUpdate :
      «Map:update» (candidateLocalBindings xarg narg phase a b c d ch)
          (SortKItem.inj_SortString field)
          ((@inj SortVal SortKItem) (SortVal.inj_SortInt value)) =
        some (candidateLocalBindings xarg narg
          newPhase newA newB newC newD ch)) :
    Rewrites
      {
        k := { val := (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» field)
              ((@inj SortVal SortExpr) (SortVal.inj_SortInt value)))) cont) },
        env := { val := 1 },
        scopes := { val := candidateActiveScopes xarg narg phase a b c d ch },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      }
      {
        k := { val := cont }, env := { val := 1 },
        scopes := { val := (candidateActiveScopes xarg narg
          newPhase newA newB newC newD ch) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc,
        stack := stack, ret := ret, exc := exc,
        exitCode := exitCode, generatedCounter := counter
      } := by
  apply Rewrites._e6f504a
    (L := 1)
    (M := candidateLocalBindings xarg narg phase a b c d ch)
    (_DotVar2 := candidatePersistentScopes)
    (V := SortVal.inj_SortInt value) (X := field)
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := candidateCalleeSingleton xarg narg phase a b c d ch)
    (_Val1 := candidateActiveScopes xarg narg phase a b c d ch)
    (_Val2 := candidateLocalBindings xarg narg
      newPhase newA newB newC newD ch)
    (_Val3 := candidateCalleeSingleton xarg narg
      newPhase newA newB newC newD ch)
    (_Val4 := candidateActiveScopes xarg narg
      newPhase newA newB newC newD ch)
  case defn_Val0 => rfl
  case defn_Val1 => exact candidateMergeActive _ _ _ _ _ _ _ _
  case defn_Val2 =>
    have hString : (inj field : SortKItem) =
        SortKItem.inj_SortString field := by rfl
    rw [hString]
    exact hUpdate
  case defn_Val3 => rfl
  case defn_Val4 => exact candidateMergeActive _ _ _ _ _ _ _ _

macro "candidateResultSolve" : tactic =>
  `(tactic|
    first
    | rfl
    | (unfold isKResult
       simp
       exact Or.inl rfl))

private theorem candidateAssignPartStep
    (phase : SortInt) (xarg narg : SortVal) (a b c d : SortInt)
    (ch : SortVal) (cont : SortK)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      (candidateLiveState
        (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
              (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "part")
              (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+"
                (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "part")
                (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))))
          cont)
        xarg narg phase a b c d ch exitCode counter)
      (candidateLiveState cont xarg narg (phase + 1) a b c d ch
        exitCode counter) := by
  unfold candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;> rfl
  · apply Rewrites.tran
    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
        rfl
    · apply Rewrites.tran
      · exact Rewrites._6d39855
      · apply Rewrites.tran
        · exact candidateLookupInt "part" phase
            xarg narg phase a b c d ch
            _ _ _ _ _ _ _ _ _ _
            (candidateContainsPart xarg narg phase a b c d ch)
            (candidateMapLookupPart xarg narg phase a b c d ch)
        · apply Rewrites.tran
          · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
              (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt phase))
              (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
          · apply Rewrites.tran
            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                (_Val0 := true) (_Val1 := true) (_Val2 := false)
                (_Val3 := true) (_Val4 := true) <;> candidateResultSolve
            · apply Rewrites.tran
              · exact Rewrites._665cd53
              · apply Rewrites.tran
                · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                    (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt 1))
                    (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
                · apply Rewrites.tran
                  · apply Rewrites._d9b5bba
                      (_Val0 := SortVal.inj_SortInt (phase + 1))
                    rfl
                  · apply Rewrites.tran
                    · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
                        (HOLE := (@inj SortVal SortExpr)
                          (SortVal.inj_SortInt (phase + 1)))
                        (_Val0 := true) (_Val1 := true) <;>
                        candidateResultSolve
                    · exact candidateAssignInt "part" (phase + 1)
                        xarg narg phase a b c d ch
                        (phase + 1) a b c d
                        _ _ _ _ _ _ _ _ _
                        (candidateUpdatePart (phase + 1) xarg narg
                          phase a b c d ch)

private theorem candidateResolveIfTrue
    (thenBranch elseBranch : SortStmts) (cont : SortK)
    (env : SortEnvCell) (scopes : SortScopesCell)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq (SortKItem.inj_SortBool true)
          (SortK.kseq
            (SortKItem.«#freezerIf(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts0_»
              (SortK.kseq (SortKItem.inj_SortStmts thenBranch) SortK.dotk)
              (SortK.kseq (SortKItem.inj_SortStmts elseBranch) SortK.dotk))
            cont)) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq (SortKItem.inj_SortStmts thenBranch) cont) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      } := by
  apply Rewrites.tran
  · simpa using
      (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
        (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortBool true))
        (_Val0 := true) (_Val1 := true)
        (by
          unfold isKResult
          simp
          exact Or.inl rfl)
        (by rfl) (by rfl))
  · apply Rewrites.tran
    · exact Rewrites._c82b7aa (_Val0 := true) (by rfl)
    · exact Rewrites._0fd4639

private theorem candidateResolveIfFalse
    (thenBranch elseBranch : SortStmts) (cont : SortK)
    (env : SortEnvCell) (scopes : SortScopesCell)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq (SortKItem.inj_SortBool false)
          (SortK.kseq
            (SortKItem.«#freezerIf(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts0_»
              (SortK.kseq (SortKItem.inj_SortStmts thenBranch) SortK.dotk)
              (SortK.kseq (SortKItem.inj_SortStmts elseBranch) SortK.dotk))
            cont)) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq (SortKItem.inj_SortStmts elseBranch) cont) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      } := by
  apply Rewrites.tran
  · simpa using
      (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
        (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortBool false))
        (_Val0 := true) (_Val1 := true)
        (by
          unfold isKResult
          simp
          exact Or.inl rfl)
        (by rfl) (by rfl))
  · apply Rewrites.tran
    · exact Rewrites._c82b7aa (_Val0 := false) (by rfl)
    · exact Rewrites._052f78e

private theorem candidateCompareLeftValue
    (value : SortVal) (comparison : SortCmpOp) (cont : SortK)
    (env : SortEnvCell) (scopes : SortScopesCell)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      {
        k := { val := (SortK.kseq
          ((@inj SortExpr SortKItem) ((@inj SortVal SortExpr) value))
          (SortK.kseq
            (SortKItem.«#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_»
              (SortK.kseq ((@inj SortCmpOp SortKItem) comparison) SortK.dotk))
            cont)) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      }
      {
        k := { val := (SortK.kseq
          ((@inj SortExpr SortKItem)
            (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
              ((@inj SortVal SortExpr) value) comparison)) cont) },
        env := env, scopes := scopes, scopeLoc := scopeLoc,
        heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode,
        generatedCounter := counter
      } := by
  simpa only using
    (Rewrites._dfb9e43
      (HOLE := (@inj SortVal SortExpr) value)
      (_Gen0 := comparison) (_DotVar1 := cont)
      (_Gen1 := env) (_Gen2 := scopes) (_Gen3 := scopeLoc)
      (_Gen4 := heap) (_Gen5 := heapLoc) (_Gen6 := stack)
      (_Gen7 := ret) (_Gen8 := exc) (_Gen9 := exitCode)
      (_Gen10 := counter) (_Val0 := true) (_Val1 := true)
      (by
        cases value <;>
        unfold isKResult
        all_goals simp
        all_goals exact Or.inl rfl)
      (by rfl) (by rfl))

macro "candidateSolve" : tactic =>
  `(tactic|
    first
    | rfl
    | (simp_all [candidateLoopStart, candidateLoopEnd,
        candidateMapContains, candidateMapsDisjoint, candidateKeyBefore,
        candidateMapInsert, candidateCanonicalMap, _Map_, «.Map», «.List»,
        «_|->_», ListItem, «builtinsScope_MPY-CORE_Scope»,
        «simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»,
        «simplifyLoopBody_VERIFICATION-SYNTAX_Stmts»,
        «simplifyReturn_VERIFICATION-SYNTAX_Stmt»,
        «isDigitC(_)_MPY-METHODS_Bool_Int»,
        «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
        «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
        pythonModuloTotal] <;> done)
    | candidateMapSolve)

macro "candidateStep" : tactic =>
  `(tactic|
    first
    | (apply Rewrites.VERIFICATION_KLEAN_EXPORT_kxExport0 <;> candidateSolve)
    | (apply Rewrites.VERIFICATION_KLEAN_EXPORT_kxExport1 <;> candidateSolve)
    | (apply Rewrites.VERIFICATION_KLEAN_EXPORT_kxExport2 <;> candidateSolve)
    | (apply Rewrites._00b027a <;> candidateSolve)
    | (apply Rewrites._00b786b <;> candidateSolve)
    | (apply Rewrites._01aecbc <;> candidateSolve)
    | (apply Rewrites._03fcca7 <;> candidateSolve)
    | (apply Rewrites._040b439 <;> candidateSolve)
    | (apply Rewrites._04d5465 <;> candidateSolve)
    | (apply Rewrites._052f78e <;> candidateSolve)
    | (apply Rewrites._055c2a4 <;> candidateSolve)
    | (apply Rewrites._0619f01 <;> candidateSolve)
    | (apply Rewrites._06d3a17 <;> candidateSolve)
    | (apply Rewrites._09d690a <;> candidateSolve)
    | (apply Rewrites._0b376b4 <;> candidateSolve)
    | (apply Rewrites._0b530f0 <;> candidateSolve)
    | (apply Rewrites._0bb8cbb <;> candidateSolve)
    | (apply Rewrites._0cbbe41 <;> candidateSolve)
    | (apply Rewrites._0d9d338 <;> candidateSolve)
    | (apply Rewrites._0e4c1b6 <;> candidateSolve)
    | (apply Rewrites._0e94041 <;> candidateSolve)
    | (apply Rewrites._0edcaa2 <;> candidateSolve)
    | (apply Rewrites._0fd4639 <;> candidateSolve)
    | (apply Rewrites._10452d5 <;> candidateSolve)
    | (apply Rewrites._1075f79 <;> candidateSolve)
    | (apply Rewrites._10db753 <;> candidateSolve)
    | (apply Rewrites._11abf7f <;> candidateSolve)
    | (apply Rewrites._11eed40 <;> candidateSolve)
    | (apply Rewrites._12d1079 <;> candidateSolve)
    | (apply Rewrites._13abaa9 <;> candidateSolve)
    | (apply Rewrites._13c31f0 <;> candidateSolve)
    | (apply Rewrites._1650340 <;> candidateSolve)
    | (apply Rewrites._1803647 <;> candidateSolve)
    | (apply Rewrites._1a401d8 <;> candidateSolve)
    | (apply Rewrites._1c2d5d9 <;> candidateSolve)
    | (apply Rewrites._1d613f5 <;> candidateSolve)
    | (apply Rewrites._1dc41fd <;> candidateSolve)
    | (apply Rewrites._1f0e78f <;> candidateSolve)
    | (apply Rewrites._1fe7f3b <;> candidateSolve)
    | (apply Rewrites._213214e <;> candidateSolve)
    | (apply Rewrites._215e352 <;> candidateSolve)
    | (apply Rewrites._225e25d <;> candidateSolve)
    | (apply Rewrites._24cbd3d <;> candidateSolve)
    | (apply Rewrites._268b33b <;> candidateSolve)
    | (apply Rewrites._27e89dd <;> candidateSolve)
    | (apply Rewrites._29a40bd <;> candidateSolve)
    | (apply Rewrites._2a0ddee <;> candidateSolve)
    | (apply Rewrites._2a7cb9e <;> candidateSolve)
    | (apply Rewrites._2b13ef0 <;> candidateSolve)
    | (apply Rewrites._2c586fd <;> candidateSolve)
    | (apply Rewrites._2d26257 <;> candidateSolve)
    | (apply Rewrites._2d60eb3 <;> candidateSolve)
    | (apply Rewrites._2d73ccf <;> candidateSolve)
    | (apply Rewrites._2e86270 <;> candidateSolve)
    | (apply Rewrites._2f12dab <;> candidateSolve)
    | (apply Rewrites._30db41c <;> candidateSolve)
    | (apply Rewrites._3110750 <;> candidateSolve)
    | (apply Rewrites._31b3ba1 <;> candidateSolve)
    | (apply Rewrites._32f4a67 <;> candidateSolve)
    | (apply Rewrites._342c8ad <;> candidateSolve)
    | (apply Rewrites._35ab37a <;> candidateSolve)
    | (apply Rewrites._35b77c9 <;> candidateSolve)
    | (apply Rewrites._36e4201 <;> candidateSolve)
    | (apply Rewrites._37c30c1 <;> candidateSolve)
    | (apply Rewrites._37c9c4d <;> candidateSolve)
    | (apply Rewrites._38833f2 <;> candidateSolve)
    | (apply Rewrites._3b3e0be <;> candidateSolve)
    | (apply Rewrites._3b733db <;> candidateSolve)
    | (apply Rewrites._3be4f5a <;> candidateSolve)
    | (apply Rewrites._3d156a6 <;> candidateSolve)
    | (apply Rewrites._3df9028 <;> candidateSolve)
    | (apply Rewrites._3e5aaf3 <;> candidateSolve)
    | (apply Rewrites._3ff423b <;> candidateSolve)
    | (apply Rewrites._40189f6 <;> candidateSolve)
    | (apply Rewrites._4213de4 <;> candidateSolve)
    | (apply Rewrites._42bd472 <;> candidateSolve)
    | (apply Rewrites._4361cf3 <;> candidateSolve)
    | (apply Rewrites._452c55a <;> candidateSolve)
    | (apply Rewrites._460aaab <;> candidateSolve)
    | (apply Rewrites._46d9f28 <;> candidateSolve)
    | (apply Rewrites._488c37d <;> candidateSolve)
    | (apply Rewrites._4991f93 <;> candidateSolve)
    | (apply Rewrites._4aae5e8 <;> candidateSolve)
    | (apply Rewrites._4ae9fa1 <;> candidateSolve)
    | (apply Rewrites._4c571cd <;> candidateSolve)
    | (apply Rewrites._4e14d84 <;> candidateSolve)
    | (apply Rewrites._4f8838c <;> candidateSolve)
    | (apply Rewrites._50048ad <;> candidateSolve)
    | (apply Rewrites._5116fe1 <;> candidateSolve)
    | (apply Rewrites._546416a <;> candidateSolve)
    | (apply Rewrites._546c464 <;> candidateSolve)
    | (apply Rewrites._5574006 <;> candidateSolve)
    | (apply Rewrites._5585886 <;> candidateSolve)
    | (apply Rewrites._576a857 <;> candidateSolve)
    | (apply Rewrites._577ab18 <;> candidateSolve)
    | (apply Rewrites._5860404 <;> candidateSolve)
    | (apply Rewrites._5d4a96e <;> candidateSolve)
    | (apply Rewrites._5e18747 <;> candidateSolve)
    | (apply Rewrites._5e85914 <;> candidateSolve)
    | (apply Rewrites._5ea93c9 <;> candidateSolve)
    | (apply Rewrites._5fef882 <;> candidateSolve)
    | (apply Rewrites._60240d4 <;> candidateSolve)
    | (apply Rewrites._6105b33 <;> candidateSolve)
    | (apply Rewrites._634174f <;> candidateSolve)
    | (apply Rewrites._6392d47 <;> candidateSolve)
    | (apply Rewrites._64553fb <;> candidateSolve)
    | (apply Rewrites._665cd53 <;> candidateSolve)
    | (apply Rewrites._68ec822 <;> candidateSolve)
    | (apply Rewrites._6c6875f <;> candidateSolve)
    | (apply Rewrites._6c70f99 <;> candidateSolve)
    | (apply Rewrites._6d39855 <;> candidateSolve)
    | (apply Rewrites._6fb501e <;> candidateSolve)
    | (apply Rewrites._6fed16d <;> candidateSolve)
    | (apply Rewrites._7034ef9 <;> candidateSolve)
    | (apply Rewrites._71c4731 <;> candidateSolve)
    | (apply Rewrites._722bb0c <;> candidateSolve)
    | (apply Rewrites._756078e <;> candidateSolve)
    | (apply Rewrites._761bdb5 <;> candidateSolve)
    | (apply Rewrites._77aced3 <;> candidateSolve)
    | (apply Rewrites._78ce5a7 <;> candidateSolve)
    | (apply Rewrites._78ebf13 <;> candidateSolve)
    | (apply Rewrites._7ae10d1 <;> candidateSolve)
    | (apply Rewrites._7b2edd7 <;> candidateSolve)
    | (apply Rewrites._7bef5d2 <;> candidateSolve)
    | (apply Rewrites._7e6f52e <;> candidateSolve)
    | (apply Rewrites._7fe18de <;> candidateSolve)
    | (apply Rewrites._81d2af8 <;> candidateSolve)
    | (apply Rewrites._8246250 <;> candidateSolve)
    | (apply Rewrites._824c4e0 <;> candidateSolve)
    | (apply Rewrites._83154cb <;> candidateSolve)
    | (apply Rewrites._837182e <;> candidateSolve)
    | (apply Rewrites._8593e9e <;> candidateSolve)
    | (apply Rewrites._8640bbc <;> candidateSolve)
    | (apply Rewrites._8708cea <;> candidateSolve)
    | (apply Rewrites._892d36a <;> candidateSolve)
    | (apply Rewrites._8b0c11c <;> candidateSolve)
    | (apply Rewrites._8c5cc47 <;> candidateSolve)
    | (apply Rewrites._8cae398 <;> candidateSolve)
    | (apply Rewrites._8e90948 <;> candidateSolve)
    | (apply Rewrites._8ea14d6 <;> candidateSolve)
    | (apply Rewrites._8ec1321 <;> candidateSolve)
    | (apply Rewrites._8eecfd5 <;> candidateSolve)
    | (apply Rewrites._91416c0 <;> candidateSolve)
    | (apply Rewrites._91cc527 <;> candidateSolve)
    | (apply Rewrites._9312d08 <;> candidateSolve)
    | (apply Rewrites._94bd14e <;> candidateSolve)
    | (apply Rewrites._951a10c <;> candidateSolve)
    | (apply Rewrites._9533001 <;> candidateSolve)
    | (apply Rewrites._9841898 <;> candidateSolve)
    | (apply Rewrites._9bdc687 <;> candidateSolve)
    | (apply Rewrites._9d3cbe1 <;> candidateSolve)
    | (apply Rewrites._9da7915 <;> candidateSolve)
    | (apply Rewrites._9e64116 <;> candidateSolve)
    | (apply Rewrites._a00964a <;> candidateSolve)
    | (apply Rewrites._a01239e <;> candidateSolve)
    | (apply Rewrites._a04aada <;> candidateSolve)
    | (apply Rewrites._a0dbc92 <;> candidateSolve)
    | (apply Rewrites._a17dc84 <;> candidateSolve)
    | (apply Rewrites._a1c192d <;> candidateSolve)
    | (apply Rewrites._a22a8d0 <;> candidateSolve)
    | (apply Rewrites._a3ba820 <;> candidateSolve)
    | (apply Rewrites._a40e438 <;> candidateSolve)
    | (apply Rewrites._a4af763 <;> candidateSolve)
    | (apply Rewrites._a6d8f3c <;> candidateSolve)
    | (apply Rewrites._a6f4dec <;> candidateSolve)
    | (apply Rewrites._a90a18b <;> candidateSolve)
    | (apply Rewrites._a998653 <;> candidateSolve)
    | (apply Rewrites._a99b04b <;> candidateSolve)
    | (apply Rewrites._aa2dbb1 <;> candidateSolve)
    | (apply Rewrites._aae3b52 <;> candidateSolve)
    | (apply Rewrites._ad459a5 <;> candidateSolve)
    | (apply Rewrites._ad78ca3 <;> candidateSolve)
    | (apply Rewrites._add2efa <;> candidateSolve)
    | (apply Rewrites._ae6cbe4 <;> candidateSolve)
    | (apply Rewrites._b13ae76 <;> candidateSolve)
    | (apply Rewrites._b378664 <;> candidateSolve)
    | (apply Rewrites._b680ae8 <;> candidateSolve)
    | (apply Rewrites._b817d8b <;> candidateSolve)
    | (apply Rewrites._b967e49 <;> candidateSolve)
    | (apply Rewrites._ba16b53 <;> candidateSolve)
    | (apply Rewrites._ba43682 <;> candidateSolve)
    | (apply Rewrites._bb17cff <;> candidateSolve)
    | (apply Rewrites._bb857a1 <;> candidateSolve)
    | (apply Rewrites._bc9ca2f <;> candidateSolve)
    | (apply Rewrites._bea722c <;> candidateSolve)
    | (apply Rewrites._c03debd <;> candidateSolve)
    | (apply Rewrites._c094fe7 <;> candidateSolve)
    | (apply Rewrites._c14e325 <;> candidateSolve)
    | (apply Rewrites._c209a34 <;> candidateSolve)
    | (apply Rewrites._c3051e0 <;> candidateSolve)
    | (apply Rewrites._c5775b3 <;> candidateSolve)
    | (apply Rewrites._c582d87 <;> candidateSolve)
    | (apply Rewrites._c65b0f2 <;> candidateSolve)
    | (apply Rewrites._c6d3850 <;> candidateSolve)
    | (apply Rewrites._c75b3bb <;> candidateSolve)
    | (apply Rewrites._c814244 <;> candidateSolve)
    | (apply Rewrites._c82b7aa <;> candidateSolve)
    | (apply Rewrites._c91bc55 <;> candidateSolve)
    | (apply Rewrites._ca92223 <;> candidateSolve)
    | (apply Rewrites._cdb8de8 <;> candidateSolve)
    | (apply Rewrites._cf456a9 <;> candidateSolve)
    | (apply Rewrites._cff49c0 <;> candidateSolve)
    | (apply Rewrites._d06f820 <;> candidateSolve)
    | (apply Rewrites._d1c9fe4 <;> candidateSolve)
    | (apply Rewrites._d30a3ae <;> candidateSolve)
    | (apply Rewrites._d39f07b <;> candidateSolve)
    | (apply Rewrites._d499ad9 <;> candidateSolve)
    | (apply Rewrites._d4f75ed <;> candidateSolve)
    | (apply Rewrites._d5bec6c <;> candidateSolve)
    | (apply Rewrites._d65f60a <;> candidateSolve)
    | (apply Rewrites._d77a1b8 <;> candidateSolve)
    | (apply Rewrites._d8a473b <;> candidateSolve)
    | (apply Rewrites._d9b5bba <;> candidateSolve)
    | (apply Rewrites._db779c6 <;> candidateSolve)
    | (apply Rewrites._dbbefa2 <;> candidateSolve)
    | (apply Rewrites._dd3be1a <;> candidateSolve)
    | (apply Rewrites._dd639c1 <;> candidateSolve)
    | (apply Rewrites._dfb9e43
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites._e024194 <;> candidateSolve)
    | (apply Rewrites._e1122bd <;> candidateSolve)
    | (apply Rewrites._e2d3680 <;> candidateSolve)
    | (apply Rewrites._e36d812 <;> candidateSolve)
    | (apply Rewrites._e5b40ae <;> candidateSolve)
    | (apply Rewrites._e63439b <;> candidateSolve)
    | (apply Rewrites._e6abb09 <;> candidateSolve)
    | (apply Rewrites._e6f504a <;> candidateSolve)
    | (apply Rewrites._e94f2d2 <;> candidateSolve)
    | (apply Rewrites._eaf4781 <;> candidateSolve)
    | (apply Rewrites._eb52494 <;> candidateSolve)
    | (apply Rewrites._ec6c120 <;> candidateSolve)
    | (apply Rewrites._ed2d6c4 <;> candidateSolve)
    | (apply Rewrites._edf0819 <;> candidateSolve)
    | (apply Rewrites._ef58c41 <;> candidateSolve)
    | (apply Rewrites._efacb65 <;> candidateSolve)
    | (apply Rewrites._f0c4941 <;> candidateSolve)
    | (apply Rewrites._f12645d <;> candidateSolve)
    | (apply Rewrites._f338107 <;> candidateSolve)
    | (apply Rewrites._f3fd256 <;> candidateSolve)
    | (apply Rewrites._f4b4e0c <;> candidateSolve)
    | (apply Rewrites._f5d43e4 <;> candidateSolve)
    | (apply Rewrites._f5ec525 <;> candidateSolve)
    | (apply Rewrites._fb01bed <;> candidateSolve)
    | (apply Rewrites._fb49878 <;> candidateSolve)
    | (apply Rewrites._fe0030b <;> candidateSolve)
    | (apply Rewrites._ffe0066 <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assert(_)_MPY_SYNTAX_Stmt_Expr1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assert(_)_MPY_SYNTAX_Stmt_Expr1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Attribute(_,_)_MPY_SYNTAX_Expr_Expr_String1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Attribute(_,_)_MPY_SYNTAX_Expr_Expr_String1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Expr(_)_MPY_SYNTAX_Stmt_Expr1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Expr(_)_MPY_SYNTAX_Stmt_Expr1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_For(_,_,_)_MPY_SYNTAX_Stmt_Expr_Expr_Stmts2_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_For(_,_,_)_MPY_SYNTAX_Stmt_Expr_Expr_Stmts2_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_IfExp(_,_,_)_MPY_SYNTAX_Expr_Expr_Expr_Expr1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_IfExp(_,_,_)_MPY_SYNTAX_Expr_Expr_Expr_Expr1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_UnaryOp(_,_)_MPY_SYNTAX_Expr_String_Expr2_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_UnaryOp(_,_)_MPY_SYNTAX_Expr_String_Expr2_heat» <;> candidateSolve))

macro "candidateSteps" : tactic =>
  `(tactic|
    repeat
      first
      | assumption
      | candidateStep
      | (apply Rewrites.tran
         · candidateStep))

/- The loop proof needs only this small, deterministic slice of the generated
   transition table.  Keeping it separate avoids asking elaboration to test
   every unrelated Python rule at each scan step. -/
macro "candidateScanStep" : tactic =>
  `(tactic|
    first
    | (apply candidateResolveIfTrue <;> candidateSolve)
    | (apply candidateResolveIfFalse <;> candidateSolve)
    | (apply candidateAssignPartStep <;> candidateSolve)
    | (apply candidateCompareLeftValue <;> candidateSolve)
    | (apply candidateLookupCh <;> candidateSolve)
    | (apply candidateLookupOrd <;> candidateSolve)
    | (apply candidateLookupInt <;> candidateSolve)
    | (apply candidateAssignInt <;> candidateSolve)
    | (apply Rewrites._94bd14e <;> candidateSolve)
    | (apply Rewrites._2a0ddee <;> candidateSolve)
    | (apply Rewrites._d499ad9 <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
        candidateSolve)
    | (apply Rewrites._1f0e78f <;> candidateSolve)
    | (apply Rewrites._6d39855 <;> candidateSolve)
    | (apply Rewrites._10452d5 <;> candidateSolve)
    | (apply Rewrites._db779c6 <;> candidateSolve)
    | (apply Rewrites._dfb9e43 <;> candidateSolve)
    | (apply Rewrites._e1122bd <;> candidateSolve)
    | (apply Rewrites._aae3b52
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites._a00964a <;> candidateSolve)
    | (apply Rewrites._00b027a <;> candidateSolve)
    | (apply Rewrites._665cd53 <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites._d9b5bba <;> candidateSolve)
    | (apply Rewrites._2d73ccf <;> candidateSolve)
    | (apply Rewrites._0619f01 <;> candidateSolve)
    | (apply Rewrites._f0c4941 <;> candidateSolve)
    | (apply Rewrites._c75b3bb <;> candidateSolve)
    | (apply Rewrites._4f8838c <;> candidateSolve)
    | (apply Rewrites._03fcca7 <;> candidateSolve))

macro "candidateScanSteps" : tactic =>
  `(tactic|
    repeat
      first
      | assumption
      | candidateScanStep
      | (apply Rewrites.tran
         · candidateScanStep))

macro "candidateDigitPrefixStep" : tactic =>
  `(tactic|
    first
    | (apply candidateLookupInt <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat» <;>
        candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := (@inj SortVal SortExpr) _) <;> candidateSolve)
    | (apply Rewrites._6d39855 <;> candidateSolve)
    | (apply Rewrites._665cd53 <;> candidateSolve)
    | (apply Rewrites._d9b5bba <;> candidateSolve)
    | (apply Rewrites._2d73ccf <;> candidateSolve))

macro "candidateDigitPrefixSteps" : tactic =>
  `(tactic|
    repeat
      first
      | candidateDigitPrefixStep
      | (apply Rewrites.tran
         · candidateDigitPrefixStep))

private def candidateDigitAssignStmt (field : SortString) : SortStmt :=
  SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
    (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» field)
    (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+"
      (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*"
        (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» field)
        (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))
      (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-"
        (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs»
          (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "ord")
          (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs»
            (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "ch")
            SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))
        (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 48)))

private theorem candidateDigitAssignStep
    (field : SortString) (current code : SortInt)
    (xarg narg : SortVal) (phase a b c d : SortInt)
    (newPhase newA newB newC newD : SortInt)
    (cont : SortK) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hContains :
      «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString field)
        (candidateLocalBindings xarg narg phase a b c d
          (candidateCharValue code)) = some true)
    (hLookup :
      «Map:lookup» (candidateLocalBindings xarg narg phase a b c d
          (candidateCharValue code))
        (SortKItem.inj_SortString field) =
          some (SortKItem.inj_SortInt current))
    (hUpdate :
      «Map:update» (candidateLocalBindings xarg narg phase a b c d
          (candidateCharValue code))
        (SortKItem.inj_SortString field)
        ((@inj SortVal SortKItem)
          (SortVal.inj_SortInt (current * 10 + (code - 48)))) =
      some (candidateLocalBindings xarg narg
        newPhase newA newB newC newD (candidateCharValue code))) :
    Rewrites
      (candidateLiveState
        (SortK.kseq (SortKItem.inj_SortStmt (candidateDigitAssignStmt field)) cont)
        xarg narg phase a b c d (candidateCharValue code) exitCode counter)
      (candidateLiveState cont xarg narg
        newPhase newA newB newC newD (candidateCharValue code)
        exitCode counter) := by
  unfold candidateDigitAssignStmt candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;> rfl
  · apply Rewrites.tran
    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> rfl
    · apply Rewrites.tran
      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> rfl
      · apply Rewrites.tran
        · exact Rewrites._6d39855
        · apply Rewrites.tran
          · exact candidateLookupInt field current xarg narg phase a b c d
              (candidateCharValue code) _ _ _ _ _ _ _ _ _ _ hContains hLookup
          · apply Rewrites.tran
            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt current))
                (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
            · apply Rewrites.tran
              · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                  (_Val0 := true) (_Val1 := true) (_Val2 := false)
                  (_Val3 := true) (_Val4 := true) <;> candidateResultSolve
              · apply Rewrites.tran
                · exact Rewrites._665cd53
                · apply Rewrites.tran
                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                      (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt 10))
                      (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
                  · apply Rewrites.tran
                    · apply Rewrites._d9b5bba
                        (_Val0 := SortVal.inj_SortInt (current * 10))
                      unfold «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
                      simp
                      exact Or.inl (by
                        simp [_13d6ee6, «_*Int_»]
                        unfold inj
                        rfl)
                    · apply Rewrites.tran
                      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                          (HOLE := (@inj SortVal SortExpr)
                            (SortVal.inj_SortInt (current * 10)))
                          (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
                      · apply Rewrites.tran
                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                            (_Val0 := true) (_Val1 := true) (_Val2 := false)
                            (_Val3 := true) (_Val4 := true) <;> candidateResultSolve
                        · apply Rewrites.tran
                          · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
                              rfl
                          · apply Rewrites.tran
                            · exact Rewrites._2d73ccf
                            · apply Rewrites.tran
                              · exact Rewrites._6d39855
                              · apply Rewrites.tran
                                · exact candidateLookupOrd xarg narg phase a b c d
                                    (candidateCharValue code) _ _ _ _ _ _ _ _ _ _
                                · apply Rewrites.tran
                                  · apply Rewrites._0619f01 <;> candidateSolve
                                  · apply Rewrites.tran
                                    · apply Rewrites._f0c4941 <;> candidateSolve
                                    · apply Rewrites.tran
                                      · exact Rewrites._6d39855
                                      · apply Rewrites.tran
                                        · exact candidateLookupCh code xarg narg phase a b c d
                                            _ _ _ _ _ _ _ _ _ _
                                        · apply Rewrites.tran
                                          · apply Rewrites._c75b3bb
                                              (_Val0 := SortVals.«_,__MPY-CORE_Vals_Val_Vals»
                                                (candidateCharValue code)
                                                SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)
                                            unfold «appendVal(_,_)_MPY-CORE_Vals_Vals_Val»
                                            unfold _1dc0c6c
                                            rfl
                                          · apply Rewrites.tran
                                            · apply Rewrites._4f8838c <;> candidateSolve
                                            · apply Rewrites.tran
                                              · apply Rewrites._03fcca7
                                                  (_Val0 := SortVal.inj_SortInt code)
                                                rfl
                                              · apply Rewrites.tran
                                                · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                    (HOLE := (@inj SortVal SortExpr)
                                                      (SortVal.inj_SortInt code))
                                                    (_Val0 := true) (_Val1 := true) <;>
                                                    candidateResultSolve
                                                · apply Rewrites.tran
                                                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                      (_Val0 := true) (_Val1 := true)
                                                      (_Val2 := false) (_Val3 := true)
                                                      (_Val4 := true) <;> candidateResultSolve
                                                  · apply Rewrites.tran
                                                    · exact Rewrites._665cd53
                                                    · apply Rewrites.tran
                                                      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                          (HOLE := (@inj SortVal SortExpr)
                                                            (SortVal.inj_SortInt 48))
                                                          (_Val0 := true) (_Val1 := true) <;>
                                                          candidateResultSolve
                                                      · apply Rewrites.tran
                                                        · apply Rewrites._d9b5bba
                                                            (_Val0 := SortVal.inj_SortInt
                                                              (code - 48))
                                                          rfl
                                                        · apply Rewrites.tran
                                                          · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                              (HOLE := (@inj SortVal SortExpr)
                                                                (SortVal.inj_SortInt
                                                                  (code - 48)))
                                                              (_Val0 := true) (_Val1 := true) <;>
                                                              candidateResultSolve
                                                          · apply Rewrites.tran
                                                            · apply Rewrites._d9b5bba
                                                                (_Val0 := SortVal.inj_SortInt
                                                                  (current * 10 + (code - 48)))
                                                              rfl
                                                            · apply Rewrites.tran
                                                              · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
                                                                  (HOLE := (@inj SortVal SortExpr)
                                                                    (SortVal.inj_SortInt
                                                                      (current * 10 + (code - 48))))
                                                                  (_Val0 := true) (_Val1 := true) <;>
                                                                  candidateResultSolve
                                                              · exact candidateAssignInt field
                                                                  (current * 10 + (code - 48))
                                                                  xarg narg phase a b c d
                                                                  (candidateCharValue code)
                                                                  newPhase newA newB newC newD
                                                                  _ _ _ _ _ _ _ _ _ hUpdate

private def candidateSlashTest : SortExpr :=
  SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
    (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "ch")
    (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "=="
      (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "/"))

private theorem candidateSlashIfFalse
    (code : SortInt) (thenBranch elseBranch : SortStmts) (cont : SortK)
    (xarg narg : SortVal) (phase a b c d : SortInt)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell)
    (hSlash : code ≠ 47) :
    Rewrites
      (candidateLiveState
        (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
              candidateSlashTest thenBranch elseBranch)) cont)
        xarg narg phase a b c d (candidateCharValue code) exitCode counter)
      (candidateLiveState
        (SortK.kseq (SortKItem.inj_SortStmts elseBranch) cont)
        xarg narg phase a b c d (candidateCharValue code) exitCode counter) := by
  unfold candidateSlashTest candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
      rfl
  · apply Rewrites.tran
    · apply Rewrites._1f0e78f <;> rfl
    · apply Rewrites.tran
      · exact Rewrites._6d39855
      · apply Rewrites.tran
        · exact candidateLookupCh code xarg narg phase a b c d
            _ _ _ _ _ _ _ _ _ _
        · apply Rewrites.tran
          · exact candidateCompareLeftValue
              (candidateCharValue code) _ _ _ _ _ _ _ _ _ _ _ _
          · apply Rewrites.tran
            · apply Rewrites._e1122bd <;> rfl
            · apply Rewrites.tran
              · apply Rewrites._00b027a
                rfl
              · apply Rewrites.tran
                · simpa only [candidateCharValue] using
                    (Rewrites._aae3b52
                      (HOLE := (@inj SortVal SortExpr) (candidateCharValue 47))
                      (_Gen0 := candidateCharValue code) (_Gen1 := "==")
                      (_Val0 := true) (_Val1 := true)
                      (by
                        unfold isKResult
                        simp
                        exact Or.inl rfl)
                      (by rfl) (by rfl))
                · apply Rewrites.tran
                  · apply Rewrites._a00964a (_Val0 := false)
                    simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
                      _03e60c5, candidateCharValue, _root_.«_==K_», hSlash]
                    intro hCodes
                    apply hSlash
                    cases hCodes
                    rfl
                  · exact candidateResolveIfFalse
                      _ _ _ _ _ _ _ _ _ _ _ _ _

private theorem candidateSlashIfTrue
    (thenBranch elseBranch : SortStmts) (cont : SortK)
    (xarg narg : SortVal) (phase a b c d : SortInt)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      (candidateLiveState
        (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
              candidateSlashTest thenBranch elseBranch)) cont)
        xarg narg phase a b c d (candidateCharValue 47) exitCode counter)
      (candidateLiveState
        (SortK.kseq (SortKItem.inj_SortStmts thenBranch) cont)
        xarg narg phase a b c d (candidateCharValue 47) exitCode counter) := by
  unfold candidateSlashTest candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
      rfl
  · apply Rewrites.tran
    · apply Rewrites._1f0e78f <;> rfl
    · apply Rewrites.tran
      · exact Rewrites._6d39855
      · apply Rewrites.tran
        · exact candidateLookupCh 47 xarg narg phase a b c d
            _ _ _ _ _ _ _ _ _ _
        · apply Rewrites.tran
          · exact candidateCompareLeftValue
              (candidateCharValue 47) _ _ _ _ _ _ _ _ _ _ _ _
          · apply Rewrites.tran
            · apply Rewrites._e1122bd <;> rfl
            · apply Rewrites.tran
              · apply Rewrites._00b027a
                  (_Val0 := SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                    47 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
                rfl
              · apply Rewrites.tran
                · simpa only [candidateCharValue] using
                    (Rewrites._aae3b52
                      (HOLE := (@inj SortVal SortExpr) (candidateCharValue 47))
                      (_Gen0 := candidateCharValue 47) (_Gen1 := "==")
                      (_Val0 := true) (_Val1 := true)
                      (by
                        unfold isKResult
                        simp
                        exact Or.inl rfl)
                      (by rfl) (by rfl))
                · apply Rewrites.tran
                  · apply Rewrites._a00964a (_Val0 := true)
                    simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
                      _03e60c5, candidateCharValue, _root_.«_==K_»]
                  · exact candidateResolveIfTrue
                      _ _ _ _ _ _ _ _ _ _ _ _ _

private def candidatePartTest (expected : SortInt) : SortExpr :=
  SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
    (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "part")
    (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "=="
      (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» expected))

private theorem candidatePartIfTrue
    (phase : SortInt) (thenBranch elseBranch : SortStmts) (cont : SortK)
    (xarg narg : SortVal) (a b c d : SortInt) (ch : SortVal)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell) :
    Rewrites
      (candidateLiveState
        (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
              (candidatePartTest phase) thenBranch elseBranch)) cont)
        xarg narg phase a b c d ch exitCode counter)
      (candidateLiveState
        (SortK.kseq (SortKItem.inj_SortStmts thenBranch) cont)
        xarg narg phase a b c d ch exitCode counter) := by
  unfold candidatePartTest candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
      rfl
  · apply Rewrites.tran
    · apply Rewrites._1f0e78f <;> rfl
    · apply Rewrites.tran
      · exact Rewrites._6d39855
      · apply Rewrites.tran
        · exact candidateLookupInt "part" phase xarg narg phase a b c d ch
            _ _ _ _ _ _ _ _ _ _
            (candidateContainsPart xarg narg phase a b c d ch)
            (candidateMapLookupPart xarg narg phase a b c d ch)
        · apply Rewrites.tran
          · exact candidateCompareLeftValue
              (SortVal.inj_SortInt phase) _ _ _ _ _ _ _ _ _ _ _ _
          · apply Rewrites.tran
            · apply Rewrites._e1122bd <;> rfl
            · apply Rewrites.tran
              · exact Rewrites._665cd53
              · apply Rewrites.tran
                · apply Rewrites._aae3b52
                    (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt phase))
                    (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
                · apply Rewrites.tran
                  · apply Rewrites._a00964a (_Val0 := true)
                    change some (phase == phase) = some true
                    simp
                  · exact candidateResolveIfTrue
                      _ _ _ _ _ _ _ _ _ _ _ _ _

private theorem candidatePartIfFalse
    (phase expected : SortInt) (thenBranch elseBranch : SortStmts) (cont : SortK)
    (xarg narg : SortVal) (a b c d : SortInt) (ch : SortVal)
    (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell)
    (hNe : phase ≠ expected) :
    Rewrites
      (candidateLiveState
        (SortK.kseq
          (SortKItem.inj_SortStmt
            (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
              (candidatePartTest expected) thenBranch elseBranch)) cont)
        xarg narg phase a b c d ch exitCode counter)
      (candidateLiveState
        (SortK.kseq (SortKItem.inj_SortStmts elseBranch) cont)
        xarg narg phase a b c d ch exitCode counter) := by
  unfold candidatePartTest candidateLiveState
  apply Rewrites.tran
  · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
      rfl
  · apply Rewrites.tran
    · apply Rewrites._1f0e78f <;> rfl
    · apply Rewrites.tran
      · exact Rewrites._6d39855
      · apply Rewrites.tran
        · exact candidateLookupInt "part" phase xarg narg phase a b c d ch
            _ _ _ _ _ _ _ _ _ _
            (candidateContainsPart xarg narg phase a b c d ch)
            (candidateMapLookupPart xarg narg phase a b c d ch)
        · apply Rewrites.tran
          · exact candidateCompareLeftValue
              (SortVal.inj_SortInt phase) _ _ _ _ _ _ _ _ _ _ _ _
          · apply Rewrites.tran
            · apply Rewrites._e1122bd <;> rfl
            · apply Rewrites.tran
              · exact Rewrites._665cd53
              · apply Rewrites.tran
                · apply Rewrites._aae3b52
                    (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt expected))
                    (_Val0 := true) (_Val1 := true) <;> candidateResultSolve
                · apply Rewrites.tran
                  · apply Rewrites._a00964a (_Val0 := false)
                    change some (phase == expected) = some false
                    simp [hNe]
                  · exact candidateResolveIfFalse
                      _ _ _ _ _ _ _ _ _ _ _ _ _

macro "candidateReturnStep" : tactic =>
  `(tactic|
    first
    | (apply Rewrites._1f0e78f <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat» <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool» <;> candidateSolve)
    | (apply Rewrites._6d39855 <;> candidateSolve)
    | (apply Rewrites._db779c6 <;> candidateSolve)
    | (apply Rewrites._d9b5bba <;> candidateSolve)
    | (apply Rewrites._665cd53 <;> candidateSolve)
    | (apply Rewrites._aae3b52 <;> candidateSolve)
    | (apply Rewrites._e1122bd <;> candidateSolve)
    | (apply Rewrites._a00964a <;> candidateSolve)
    | (apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool» <;> candidateSolve)
    | (apply Rewrites._b817d8b <;> candidateSolve)
    | (apply Rewrites._2a0ddee <;> candidateSolve)
    | (apply Rewrites._2f12dab <;> candidateSolve)
    | (apply Rewrites._9533001 <;> candidateSolve))

macro "candidateReturnSteps" : tactic =>
  `(tactic|
    repeat
      first
      | assumption
      | candidateReturnStep
      | (apply Rewrites.tran
         · candidateReturnStep))

macro "candidateReturnRflStep" : tactic =>
  `(tactic|
    first
    | (apply Rewrites._1f0e78f <;> rfl)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> rfl)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool» <;> rfl)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat» <;> rfl)
    | (apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool» <;> rfl)
    | (apply Rewrites._6d39855 <;> rfl)
    | (apply Rewrites._db779c6 <;> rfl)
    | (apply Rewrites._d9b5bba <;> rfl)
    | (apply Rewrites._665cd53 <;> rfl)
    | (apply Rewrites._aae3b52 <;> rfl)
    | (apply Rewrites._e1122bd <;> rfl)
    | (apply Rewrites._a00964a <;> rfl)
    | (apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool» <;> rfl)
    | (apply Rewrites._b817d8b <;> rfl)
    | (apply Rewrites._2a0ddee <;> rfl)
    | (apply Rewrites._2f12dab <;> rfl)
    | (apply Rewrites._9533001 <;> rfl))

macro "candidateReturnRflSteps" : tactic =>
  `(tactic|
    repeat
      first
      | assumption
      | candidateReturnRflStep
      | (apply Rewrites.tran
         · candidateReturnRflStep))

set_option maxHeartbeats 10000000 in
private theorem candidateLoopSound (codes : SortIntSeq) :
    ∀ (xarg narg : SortVal) (phase a b c d : SortInt) (oldch : SortVal)
      (exitCode : SortExitCodeCell) (counter : SortGeneratedCounterCell),
      «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»
          codes phase a b c d = true →
      Rewrites
        (candidateLoopStart codes xarg narg phase a b c d oldch exitCode counter)
        (candidateLoopEnd
          («scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»
            codes phase a b c d)
          exitCode counter) := by
  induction codes with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      intro xarg narg phase a b c d oldch exitCode counter hValid
      simp only [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
        decide_eq_true_eq] at hValid
      rcases hValid with ⟨rfl, ha, hb, hc, hd⟩
      unfold candidateLoopStart candidateLoopEnd
      apply Rewrites.tran
      · exact Rewrites._c65b0f2
          (IT := SortIterable.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
      · apply Rewrites.tran
        · exact Rewrites._7fe18de
        · apply Rewrites.tran
          · exact Rewrites._8e90948
          · apply Rewrites.tran
            · exact Rewrites._94bd14e
            · unfold «simplifyReturn_VERIFICATION-SYNTAX_Stmt»
              apply Rewrites.tran
              · apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_heat»
                · rfl
                · rfl
                · rfl
                · rfl
              · apply Rewrites.tran
                · apply Rewrites._1f0e78f <;> rfl
                · apply Rewrites.tran
                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;> rfl
                  · candidateReturnRflSteps
                    /- The phase split below belongs to the nonempty-code branch;
                       it is retained here temporarily only as inert text while the
                       active copy is placed at that branch.  -/
                    /-
                    by_cases hp2 : phase = 2
                    · subst phase
                      by_cases hSlash : code = 47
                      · subst code
                        simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                        apply Rewrites.tran
                        · exact candidateSlashIfTrue _ _ _ xarg narg 2
                            a b c d exitCode counter
                        · apply Rewrites.tran
                          · exact Rewrites._94bd14e
                          · apply Rewrites.tran
                            · exact candidateAssignPartStep 2 xarg narg a b c d
                                (candidateCharValue 47) _ exitCode counter
                            · apply Rewrites.tran
                              · exact Rewrites._2a0ddee
                              · apply Rewrites.tran
                                · exact Rewrites._2a0ddee
                                · apply Rewrites.tran
                                  · apply Rewrites._d499ad9
                                    rfl
                                  · simpa [candidateLoopStart,
                                      candidateLoopEnd,
                                      «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»] using
                                      (ih xarg narg 3 a b c d
                                        (candidateCharValue 47)
                                        exitCode counter hValid)
                      · simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          «isDigitC(_)_MPY-METHODS_Bool_Int», hSlash] at hValid
                        apply Rewrites.tran
                        · exact candidateSlashIfFalse code _ _ _ xarg narg 2
                            a b c d exitCode counter hSlash
                        · apply Rewrites.tran
                          · exact Rewrites._94bd14e
                          · apply Rewrites.tran
                            · exact candidatePartIfFalse 2 0 _ _ _ xarg narg
                                a b c d (candidateCharValue code)
                                exitCode counter (by omega)
                            · apply Rewrites.tran
                              · exact Rewrites._94bd14e
                              · apply Rewrites.tran
                                · exact candidatePartIfFalse 2 1 _ _ _ xarg narg
                                    a b c d (candidateCharValue code)
                                    exitCode counter (by omega)
                                · apply Rewrites.tran
                                  · exact Rewrites._94bd14e
                                  · apply Rewrites.tran
                                    · exact candidatePartIfTrue 2 _ _ _ xarg narg
                                        a b c d (candidateCharValue code)
                                        exitCode counter
                                    · apply Rewrites.tran
                                      · exact Rewrites._94bd14e
                                      · apply Rewrites.tran
                                        · exact candidateDigitAssignStep "c" c code
                                            xarg narg 2 a b c d
                                            2 a b (c * 10 + (code - 48)) d
                                            _ exitCode counter
                                            (candidateContainsC xarg narg 2 a b c d
                                              (candidateCharValue code))
                                            (candidateMapLookupC xarg narg 2 a b c d
                                              (candidateCharValue code))
                                            (candidateUpdateC (c * 10 + (code - 48))
                                              xarg narg 2 a b c d
                                              (candidateCharValue code))
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · exact Rewrites._2a0ddee
                                            · apply Rewrites.tran
                                              · exact Rewrites._2a0ddee
                                              · apply Rewrites.tran
                                                · exact Rewrites._2a0ddee
                                                · apply Rewrites.tran
                                                  · exact Rewrites._2a0ddee
                                                  · apply Rewrites.tran
                                                    · apply Rewrites._d499ad9
                                                      rfl
                                                    · simpa [candidateLoopStart,
                                                        candidateLoopEnd,
                                                        «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                        «isDigitC(_)_MPY-METHODS_Bool_Int»,
                                                        hSlash, hValid.1] using
                                                        (ih xarg narg 2 a b
                                                          (c * 10 + (code - 48)) d
                                                          (candidateCharValue code)
                                                          exitCode counter hValid.2)
                    · have hp3 : phase = 3 := Classical.byContradiction (fun hp3 => by
                        simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          hp0, hp1, hp2, hp3] at hValid)
                      subst phase
                      simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                        «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                      have hLo : 48 ≤ code := hValid.1.1
                      have hLo : 48 ≤ code := hValid.1.1
                      have hSlash : code ≠ 47 := by
                        intro hCode
                        subst code
                        exact (by decide : ¬ (48 : SortInt) ≤ 47) hValid.1.1
                      apply Rewrites.tran
                      · exact candidateSlashIfFalse code _ _ _ xarg narg 3
                          a b c d exitCode counter hSlash
                      · apply Rewrites.tran
                        · exact Rewrites._94bd14e
                        · apply Rewrites.tran
                          · exact candidatePartIfFalse 3 0 _ _ _ xarg narg
                              a b c d (candidateCharValue code)
                              exitCode counter (by omega)
                          · apply Rewrites.tran
                            · exact Rewrites._94bd14e
                            · apply Rewrites.tran
                              · exact candidatePartIfFalse 3 1 _ _ _ xarg narg
                                  a b c d (candidateCharValue code)
                                  exitCode counter (by omega)
                              · apply Rewrites.tran
                                · exact Rewrites._94bd14e
                                · apply Rewrites.tran
                                  · exact candidatePartIfFalse 3 2 _ _ _ xarg narg
                                      a b c d (candidateCharValue code)
                                      exitCode counter (by omega)
                                  · apply Rewrites.tran
                                    · exact Rewrites._94bd14e
                                    · apply Rewrites.tran
                                      · exact candidateDigitAssignStep "d" d code
                                          xarg narg 3 a b c d
                                          3 a b c (d * 10 + (code - 48))
                                          _ exitCode counter
                                          (candidateContainsD xarg narg 3 a b c d
                                            (candidateCharValue code))
                                          (candidateMapLookupD xarg narg 3 a b c d
                                            (candidateCharValue code))
                                          (candidateUpdateD (d * 10 + (code - 48))
                                            xarg narg 3 a b c d
                                            (candidateCharValue code))
                                      · apply Rewrites.tran
                                        · exact Rewrites._2a0ddee
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · exact Rewrites._2a0ddee
                                            · apply Rewrites.tran
                                              · exact Rewrites._2a0ddee
                                              · apply Rewrites.tran
                                                · exact Rewrites._2a0ddee
                                                · apply Rewrites.tran
                                                  · apply Rewrites._d499ad9
                                                    rfl
                                                  · simpa [candidateLoopStart,
                                                      candidateLoopEnd,
                                                      «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                      «isDigitC(_)_MPY-METHODS_Bool_Int»,
                                                      hSlash, hValid.1] using
                                                      (ih xarg narg 3 a b c
                                                        (d * 10 + (code - 48))
                                                        (candidateCharValue code)
                                                        exitCode counter hValid.2)
                    -/
                    apply Rewrites.tran
                    · exact candidateLookupA xarg narg 3 a b c d oldch _ _ _ _ _ _ _ _ _ _
                    · apply Rewrites.tran
                      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                          (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt a))
                          (_Val0 := true) (_Val1 := true)
                        case defn_Val0 =>
                          unfold isKResult
                          simp
                          exact Or.inl rfl
                        case defn_Val1 =>
                          unfold _root_._andBool_
                          simp
                          exact Or.inl rfl
                        case req => rfl
                      · apply Rewrites.tran
                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                            (_Val0 := true) (_Val1 := true) (_Val2 := false)
                            (_Val3 := true) (_Val4 := true)
                          case defn_Val0 =>
                            unfold isKResult
                            simp
                            exact Or.inl rfl
                          case defn_Val1 =>
                            unfold _root_._andBool_
                            simp
                            exact Or.inl rfl
                          case defn_Val2 => rfl
                          case defn_Val3 => rfl
                          case defn_Val4 => rfl
                          case req => rfl
                        · apply Rewrites.tran
                          · exact Rewrites._6d39855
                          · apply Rewrites.tran
                            · exact candidateLookupInt "c" c xarg narg 3 a b c d oldch
                                _ _ _ _ _ _ _ _ _ _
                                (candidateContainsC xarg narg 3 a b c d oldch)
                                (candidateMapLookupC xarg narg 3 a b c d oldch)
                            · apply Rewrites.tran
                              · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                  (HOLE := (@inj SortVal SortExpr) (SortVal.inj_SortInt c))
                                  (_Val0 := true) (_Val1 := true)
                                case defn_Val0 =>
                                  unfold isKResult
                                  simp
                                  exact Or.inl rfl
                                case defn_Val1 =>
                                  unfold _root_._andBool_
                                  simp
                                  exact Or.inl rfl
                                case req => rfl
                              · apply Rewrites.tran
                                · apply Rewrites._d9b5bba
                                    (_Val0 := SortVal.inj_SortInt (a * c))
                                  unfold «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
                                  simp
                                  exact Or.inl (by
                                    simp [_13d6ee6, «_*Int_»]
                                    unfold inj
                                    rfl)
                                · apply Rewrites.tran
                                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                      (HOLE := (@inj SortVal SortExpr)
                                        (SortVal.inj_SortInt (a * c)))
                                      (_Val0 := true) (_Val1 := true)
                                    case defn_Val0 =>
                                      unfold isKResult
                                      simp
                                      exact Or.inl rfl
                                    case defn_Val1 =>
                                      unfold _root_._andBool_
                                      simp
                                      exact Or.inl rfl
                                    case req => rfl
                                  · apply Rewrites.tran
                                    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                        (_Val0 := true) (_Val1 := true) (_Val2 := false)
                                        (_Val3 := true) (_Val4 := true)
                                      case defn_Val0 =>
                                        unfold isKResult
                                        simp
                                        exact Or.inl rfl
                                      case defn_Val1 =>
                                        unfold _root_._andBool_
                                        simp
                                        exact Or.inl rfl
                                      case defn_Val2 => rfl
                                      case defn_Val3 => rfl
                                      case defn_Val4 => rfl
                                      case req => rfl
                                    · apply Rewrites.tran
                                      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
                                          <;> rfl
                                      · apply Rewrites.tran
                                        · exact Rewrites._6d39855
                                        · apply Rewrites.tran
                                          · exact candidateLookupInt "b" b xarg narg 3 a b c d oldch
                                              _ _ _ _ _ _ _ _ _ _
                                              (candidateContainsB xarg narg 3 a b c d oldch)
                                              (candidateMapLookupB xarg narg 3 a b c d oldch)
                                          · apply Rewrites.tran
                                            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                (HOLE := (@inj SortVal SortExpr)
                                                  (SortVal.inj_SortInt b))
                                                (_Val0 := true) (_Val1 := true)
                                              case defn_Val0 =>
                                                unfold isKResult
                                                simp
                                                exact Or.inl rfl
                                              case defn_Val1 =>
                                                unfold _root_._andBool_
                                                simp
                                                exact Or.inl rfl
                                              case req => rfl
                                            · apply Rewrites.tran
                                              · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                  (_Val0 := true) (_Val1 := true) (_Val2 := false)
                                                  (_Val3 := true) (_Val4 := true)
                                                case defn_Val0 =>
                                                  unfold isKResult
                                                  simp
                                                  exact Or.inl rfl
                                                case defn_Val1 =>
                                                  unfold _root_._andBool_
                                                  simp
                                                  exact Or.inl rfl
                                                case defn_Val2 => rfl
                                                case defn_Val3 => rfl
                                                case defn_Val4 => rfl
                                                case req => rfl
                                              · apply Rewrites.tran
                                                · exact Rewrites._6d39855
                                                · apply Rewrites.tran
                                                  · exact candidateLookupInt "d" d xarg narg 3 a b c d oldch
                                                      _ _ _ _ _ _ _ _ _ _
                                                      (candidateContainsD xarg narg 3 a b c d oldch)
                                                      (candidateMapLookupD xarg narg 3 a b c d oldch)
                                                  · apply Rewrites.tran
                                                    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                        (HOLE := (@inj SortVal SortExpr)
                                                          (SortVal.inj_SortInt d))
                                                        (_Val0 := true) (_Val1 := true)
                                                      case defn_Val0 =>
                                                        unfold isKResult
                                                        simp
                                                        exact Or.inl rfl
                                                      case defn_Val1 =>
                                                        unfold _root_._andBool_
                                                        simp
                                                        exact Or.inl rfl
                                                      case req => rfl
                                                    · apply Rewrites.tran
                                                      · apply Rewrites._d9b5bba
                                                          (_Val0 := SortVal.inj_SortInt (b * d))
                                                        unfold «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
                                                        simp
                                                        exact Or.inl (by
                                                          simp [_13d6ee6, «_*Int_»]
                                                          unfold inj
                                                          rfl)
                                                      · apply Rewrites.tran
                                                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                            (HOLE := (@inj SortVal SortExpr)
                                                              (SortVal.inj_SortInt (b * d)))
                                                            (_Val0 := true) (_Val1 := true)
                                                          case defn_Val0 =>
                                                            unfold isKResult
                                                            simp
                                                            exact Or.inl rfl
                                                          case defn_Val1 =>
                                                            unfold _root_._andBool_
                                                            simp
                                                            exact Or.inl rfl
                                                          case req => rfl
                                                        · apply Rewrites.tran
                                                          · apply Rewrites._d9b5bba
                                                              (_Val0 := SortVal.inj_SortInt
                                                                (pythonModuloTotal (a * c) (b * d)))
                                                            have hbd : b * d ≠ 0 := by
                                                              exact Int.ne_of_gt (Int.mul_pos hb hd)
                                                            simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
                                                              _13d6ee6, _1909c2e, _2acce51, _30456db,
                                                              _3598da3, _42bfa12, _4f03d42, _4f373ea,
                                                              _50f1b5a, _614d946, _798d463, _7f23ecf,
                                                              «pyMod(_,_)_MPY-INT_Int_Int_Int», _2d78aae,
                                                              «_%Int_», «_+Int_», pythonModuloTotal, hbd]
                                                            unfold inj
                                                            rfl
                                                          · apply Rewrites.tran
                                                            · apply Rewrites._dfb9e43
                                                                (HOLE := (@inj SortVal SortExpr)
                                                                  (SortVal.inj_SortInt
                                                                    (pythonModuloTotal (a * c) (b * d))))
                                                                (_Val0 := true) (_Val1 := true)
                                                              case defn_Val0 =>
                                                                unfold isKResult
                                                                simp
                                                                exact Or.inl rfl
                                                              case defn_Val1 =>
                                                                unfold _root_._andBool_
                                                                simp
                                                                exact Or.inl rfl
                                                              case req => rfl
                                                            · apply Rewrites.tran
                                                              · apply Rewrites._e1122bd <;> rfl
                                                              · apply Rewrites.tran
                                                                · exact Rewrites._665cd53
                                                                · apply Rewrites.tran
                                                                  · apply Rewrites._aae3b52
                                                                      (HOLE := (@inj SortVal SortExpr)
                                                                        (SortVal.inj_SortInt 0))
                                                                      (_Val0 := true) (_Val1 := true)
                                                                    case defn_Val0 =>
                                                                      unfold isKResult
                                                                      simp
                                                                      exact Or.inl rfl
                                                                    case defn_Val1 =>
                                                                      unfold _root_._andBool_
                                                                      simp
                                                                      exact Or.inl rfl
                                                                    case req => rfl
                                                                  · apply Rewrites.tran
                                                                    · apply Rewrites._a00964a
                                                                        (_Val0 := decide
                                                                          (pythonModuloTotal
                                                                            (a * c) (b * d) = 0))
                                                                      rfl
                                                                    · apply Rewrites.tran
                                                                      · apply Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool»
                                                                          (HOLE := (@inj SortVal SortExpr)
                                                                            (SortVal.inj_SortBool
                                                                              (decide
                                                                                (pythonModuloTotal
                                                                                  (a * c) (b * d) = 0))))
                                                                          (_Val0 := true) (_Val1 := true)
                                                                        case defn_Val0 =>
                                                                          unfold isKResult
                                                                          simp
                                                                          exact Or.inl rfl
                                                                        case defn_Val1 =>
                                                                          unfold _root_._andBool_
                                                                          simp
                                                                          exact Or.inl rfl
                                                                        case req => rfl
                                                                      · apply Rewrites.tran
                                                                        · exact Rewrites._b817d8b
                                                                        · have hResult :
                                                                              «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»
                                                                                  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
                                                                                  3 a b c d =
                                                                                decide
                                                                                  (pythonModuloTotal
                                                                                    (a * c) (b * d) = 0) := by
                                                                            simp [«scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                                              ha, hb, hc, hd]
                                                                          rw [hResult]
                                                                          apply Rewrites._9533001
                                                                            (CALLERL := 0) (L := 1) (SAVEDL := 1)
                                                                            (CONT := SortK.dotk)
                                                                            (SC := candidateActiveScopes
                                                                              xarg narg 3 a b c d oldch)
                                                                            (V := SortVal.inj_SortBool
                                                                              (decide
                                                                                (pythonModuloTotal
                                                                                  (a * c) (b * d) = 0)))
                                                                            (_DotVar1 := «.List»)
                                                                            (_Val0 := ListItem
                                                                              (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
                                                                                SortK.dotk 0 1))
                                                                            (_Val1 := ListItem
                                                                              (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
                                                                                SortK.dotk 0 1))
                                                                            (_Val2 := candidatePersistentScopes)
                                                                            (_Gen0 := 2)
                                                                          case defn_Val0 =>
                                                                            unfold _root_.ListItem ListItem
                                                                            rfl
                                                                          case defn_Val1 =>
                                                                            unfold _root_._List_ ListItem «.List»
                                                                            rfl
                                                                          case defn_Val2 =>
                                                                            unfold «_[_<-undef]»
                                                                            candidateUnfoldMapModels
                                                                            simp [candidateActiveScopes,
                                                                              candidatePersistentScopes]
                                                                            have hinj :
                                                                                (inj (1 : SortInt) : SortKItem) =
                                                                                  SortKItem.inj_SortInt 1 := by
                                                                              rfl
                                                                            rw [hinj]
                                                                            simp
                                                                            candidateUnfoldMapModels
                                                                            simp
                                                                            candidateUnfoldMapModels
                                                                            simp
                                                                            candidateUnfoldMapModels
                                                                            rfl
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest ih =>
      intro xarg narg phase a b c d oldch exitCode counter hValid
      unfold candidateLoopStart candidateLoopEnd
      apply Rewrites.tran
      · exact Rewrites._c65b0f2
          (IT := SortIterable.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest)))
      · apply Rewrites.tran
        · exact Rewrites._e024194
        · apply Rewrites.tran
          · exact Rewrites._3ff423b
          · apply Rewrites.tran
            · simpa [candidateCharValue] using
                (candidateBindCh code xarg narg phase a b c d oldch
                  _ _ _ _ _ _ _ _ _)
            · unfold «simplifyLoopBody_VERIFICATION-SYNTAX_Stmts»
              apply Rewrites.tran
              · exact Rewrites._94bd14e
              · by_cases hp0 : phase = 0
                · subst phase
                  by_cases hSlash : code = 47
                  · subst code
                    simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                      «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                    apply Rewrites.tran
                    · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
                        candidateSolve
                    · apply Rewrites.tran
                      · apply Rewrites._1f0e78f <;> rfl
                      · apply Rewrites.tran
                        · exact Rewrites._6d39855
                        · apply Rewrites.tran
                          · exact candidateLookupCh 47 xarg narg 0 a b c d
                              _ _ _ _ _ _ _ _ _ _
                          · apply Rewrites.tran
                            · simpa only [candidateCharValue] using
                                (Rewrites._dfb9e43
                                  (HOLE := (@inj SortVal SortExpr)
                                    (candidateCharValue 47))
                                  (_Val0 := true) (_Val1 := true)
                                  (by
                                    unfold isKResult
                                    simp
                                    exact Or.inl rfl)
                                  (by rfl) (by rfl))
                            · apply Rewrites.tran
                              · apply Rewrites._e1122bd <;> rfl
                              · apply Rewrites.tran
                                · apply Rewrites._00b027a
                                    (_Val0 := SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                                      47 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
                                  rfl
                                · apply Rewrites.tran
                                  · simpa only [candidateCharValue] using
                                      (Rewrites._aae3b52
                                        (HOLE := (@inj SortVal SortExpr)
                                          (candidateCharValue 47))
                                        (_Gen0 := candidateCharValue 47)
                                        (_Val0 := true) (_Val1 := true)
                                        (by
                                          unfold isKResult
                                          simp
                                          exact Or.inl rfl)
                                        (by rfl) (by rfl))
                                  · apply Rewrites.tran
                                    · apply Rewrites._a00964a
                                        (_Val0 := true)
                                      simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
                                        _03e60c5, candidateCharValue, _root_.«_==K_»]
                                    · apply Rewrites.tran
                                      · exact candidateResolveIfTrue
                                          _ _ _ _ _ _ _ _ _ _ _ _ _
                                      · apply Rewrites.tran
                                        · exact Rewrites._94bd14e
                                        · apply Rewrites.tran
                                          · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;>
                                              rfl
                                          · apply Rewrites.tran
                                            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
                                                rfl
                                            · apply Rewrites.tran
                                              · exact Rewrites._6d39855
                                              · apply Rewrites.tran
                                                · exact candidateLookupInt "part" 0
                                                    xarg narg 0 a b c d
                                                    (candidateCharValue 47)
                                                    _ _ _ _ _ _ _ _ _ _
                                                    (candidateContainsPart xarg narg 0 a b c d
                                                      (candidateCharValue 47))
                                                    (candidateMapLookupPart xarg narg 0 a b c d
                                                      (candidateCharValue 47))
                                                · apply Rewrites.tran
                                                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                      (HOLE := (@inj SortVal SortExpr)
                                                        (SortVal.inj_SortInt 0))
                                                      (_Val0 := true) (_Val1 := true) <;>
                                                      candidateResultSolve
                                                  · apply Rewrites.tran
                                                    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                        (_Val0 := true) (_Val1 := true)
                                                        (_Val2 := false) (_Val3 := true)
                                                        (_Val4 := true) <;>
                                                        candidateResultSolve
                                                    · apply Rewrites.tran
                                                      · exact Rewrites._665cd53
                                                      · apply Rewrites.tran
                                                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                            (HOLE := (@inj SortVal SortExpr)
                                                              (SortVal.inj_SortInt 1))
                                                            (_Val0 := true) (_Val1 := true) <;>
                                                            candidateResultSolve
                                                        · apply Rewrites.tran
                                                          · apply Rewrites._d9b5bba
                                                              (_Val0 := SortVal.inj_SortInt 1)
                                                            rfl
                                                          · apply Rewrites.tran
                                                            · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
                                                                (HOLE := (@inj SortVal SortExpr)
                                                                  (SortVal.inj_SortInt 1))
                                                                (_Val0 := true) (_Val1 := true) <;>
                                                                candidateResultSolve
                                                            · apply Rewrites.tran
                                                              · exact candidateAssignInt
                                                                  "part" 1 xarg narg
                                                                  0 a b c d (candidateCharValue 47)
                                                                  1 a b c d
                                                                  _ _ _ _ _ _ _ _ _
                                                                  (candidateUpdatePart 1 xarg narg
                                                                    0 a b c d
                                                                    (candidateCharValue 47))
                                                              · apply Rewrites.tran
                                                                · exact Rewrites._2a0ddee
                                                                · apply Rewrites.tran
                                                                  · exact Rewrites._2a0ddee
                                                                  · apply Rewrites.tran
                                                                    · apply Rewrites._d499ad9
                                                                      rfl
                                                                    · simpa [candidateLoopStart,
                                                                        candidateLoopEnd,
                                                                        «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»] using
                                                                        (ih xarg narg 1 a b c d
                                                                          (candidateCharValue 47)
                                                                          exitCode counter hValid)
                  · simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                      hSlash, Bool.or_eq_true] at hValid
                    candidateScanSteps
                    apply Rewrites.tran
                    · simpa only [candidateCharValue] using
                        (candidateCompareLeftValue (candidateCharValue code)
                          _ _ _ _ _ _ _ _ _ _ _ _)
                    · apply Rewrites.tran
                      · apply Rewrites._e1122bd <;> rfl
                      · apply Rewrites.tran
                        · apply Rewrites._00b027a
                          rfl
                        · apply Rewrites.tran
                          · simpa only [candidateCharValue] using
                              (Rewrites._aae3b52
                                (HOLE := (@inj SortVal SortExpr)
                                  (candidateCharValue 47))
                                (_Gen0 := candidateCharValue code)
                                (_Gen1 := "==")
                                (_Val0 := true) (_Val1 := true)
                                (by
                                  unfold isKResult
                                  simp
                                  exact Or.inl rfl)
                                (by rfl) (by rfl))
                          · apply Rewrites.tran
                            · apply Rewrites._a00964a (_Val0 := false)
                              simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
                                _03e60c5, candidateCharValue,
                                _root_.«_==K_», hSlash]
                              intro hCodes
                              apply hSlash
                              cases hCodes
                              rfl
                            · apply Rewrites.tran
                              · apply candidateResolveIfFalse
                              · apply Rewrites.tran
                                · exact Rewrites._94bd14e
                                · apply Rewrites.tran
                                  · apply Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat» <;>
                                      candidateSolve
                                  · apply Rewrites.tran
                                    · apply Rewrites._1f0e78f <;> rfl
                                    · apply Rewrites.tran
                                      · exact Rewrites._6d39855
                                      · apply Rewrites.tran
                                        · exact candidateLookupInt "part" 0
                                            xarg narg 0 a b c d
                                            (candidateCharValue code)
                                            _ _ _ _ _ _ _ _ _ _
                                            (candidateContainsPart xarg narg 0 a b c d
                                              (candidateCharValue code))
                                            (candidateMapLookupPart xarg narg 0 a b c d
                                              (candidateCharValue code))
                                        · apply Rewrites.tran
                                          · apply Rewrites._dfb9e43
                                              (HOLE := (@inj SortVal SortExpr)
                                                (SortVal.inj_SortInt 0))
                                              (_Val0 := true) (_Val1 := true) <;>
                                              candidateResultSolve
                                          · apply Rewrites.tran
                                            · apply Rewrites._e1122bd <;> rfl
                                            · apply Rewrites.tran
                                              · exact Rewrites._665cd53
                                              · apply Rewrites.tran
                                                · apply Rewrites._aae3b52
                                                    (HOLE := (@inj SortVal SortExpr)
                                                      (SortVal.inj_SortInt 0))
                                                    (_Val0 := true) (_Val1 := true) <;>
                                                    candidateResultSolve
                                                · apply Rewrites.tran
                                                  · apply Rewrites._a00964a
                                                      (_Val0 := true)
                                                    rfl
                                                  · apply Rewrites.tran
                                                    · apply candidateResolveIfTrue
                                                    · apply Rewrites.tran
                                                      · exact Rewrites._94bd14e
                                                      · apply Rewrites.tran
                                                        · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat» <;>
                                                            rfl
                                                        · apply Rewrites.tran
                                                          · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
                                                              rfl
                                                          · apply Rewrites.tran
                                                            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
                                                                rfl
                                                            · apply Rewrites.tran
                                                              · exact Rewrites._6d39855
                                                              · apply Rewrites.tran
                                                                · exact candidateLookupA
                                                                    xarg narg 0 a b c d
                                                                    (candidateCharValue code)
                                                                    _ _ _ _ _ _ _ _ _ _
                                                                · candidateDigitPrefixSteps
                                                                  apply Rewrites.tran
                                                                  · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                                      (HOLE := (@inj SortVal SortExpr)
                                                                        (SortVal.inj_SortInt a))
                                                                      (_Val0 := true) (_Val1 := true) <;>
                                                                      candidateResultSolve
                                                                  · apply Rewrites.tran
                                                                    · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                                        (_Val0 := true) (_Val1 := true)
                                                                        (_Val2 := false) (_Val3 := true)
                                                                        (_Val4 := true) <;>
                                                                        candidateResultSolve
                                                                    · apply Rewrites.tran
                                                                      · exact Rewrites._665cd53
                                                                      · apply Rewrites.tran
                                                                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                                            (HOLE := (@inj SortVal SortExpr)
                                                                              (SortVal.inj_SortInt 10))
                                                                            (_Val0 := true) (_Val1 := true) <;>
                                                                            candidateResultSolve
                                                                        · apply Rewrites.tran
                                                                          · apply Rewrites._d9b5bba
                                                                              (_Val0 := SortVal.inj_SortInt
                                                                                (a * 10))
                                                                            unfold «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
                                                                            simp
                                                                            exact Or.inl (by
                                                                              simp [_13d6ee6, «_*Int_»]
                                                                              unfold inj
                                                                              rfl)
                                                                          · apply Rewrites.tran
                                                                            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                                                (HOLE := (@inj SortVal SortExpr)
                                                                                  (SortVal.inj_SortInt
                                                                                    (a * 10)))
                                                                                (_Val0 := true) (_Val1 := true) <;>
                                                                                candidateResultSolve
                                                                            · apply Rewrites.tran
                                                                              · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                                                  (_Val0 := true)
                                                                                  (_Val1 := true)
                                                                                  (_Val2 := false)
                                                                                  (_Val3 := true)
                                                                                  (_Val4 := true) <;>
                                                                                  candidateResultSolve
                                                                              · apply Rewrites.tran
                                                                                · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat» <;>
                                                                                    rfl
                                                                                · apply Rewrites.tran
                                                                                  · exact Rewrites._2d73ccf
                                                                                  · apply Rewrites.tran
                                                                                    · exact Rewrites._6d39855
                                                                                    · apply Rewrites.tran
                                                                                      · exact candidateLookupOrd
                                                                                          xarg narg 0 a b c d
                                                                                          (candidateCharValue code)
                                                                                          _ _ _ _ _ _ _ _ _ _
                                                                                      · apply Rewrites.tran
                                                                                        · apply Rewrites._0619f01 <;>
                                                                                            candidateSolve
                                                                                        · apply Rewrites.tran
                                                                                          · apply Rewrites._f0c4941 <;>
                                                                                              candidateSolve
                                                                                          · apply Rewrites.tran
                                                                                            · exact Rewrites._6d39855
                                                                                            · apply Rewrites.tran
                                                                                              · exact candidateLookupCh
                                                                                                  code xarg narg
                                                                                                  0 a b c d
                                                                                                  _ _ _ _ _ _ _ _ _ _
                                                                                              · apply Rewrites.tran
                                                                                                · apply Rewrites._c75b3bb
                                                                                                    (_Val0 :=
                                                                                                      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
                                                                                                        (candidateCharValue code)
                                                                                                        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)
                                                                                                  unfold «appendVal(_,_)_MPY-CORE_Vals_Vals_Val»
                                                                                                  unfold _1dc0c6c
                                                                                                  rfl
                                                                                                · apply Rewrites.tran
                                                                                                  · apply Rewrites._4f8838c <;>
                                                                                                      candidateSolve
                                                                                                  · apply Rewrites.tran
                                                                                                    · apply Rewrites._03fcca7
                                                                                                        (_Val0 := SortVal.inj_SortInt code)
                                                                                                      rfl
                                                                                                    · apply Rewrites.tran
                                                                                                      · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
                                                                                                          (HOLE := (@inj SortVal SortExpr)
                                                                                                            (SortVal.inj_SortInt code))
                                                                                                          (_Val0 := true) (_Val1 := true) <;>
                                                                                                          candidateResultSolve
                                                                                                      · apply Rewrites.tran
                                                                                                        · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
                                                                                                            (_Val0 := true)
                                                                                                            (_Val1 := true)
                                                                                                            (_Val2 := false)
                                                                                                            (_Val3 := true)
                                                                                                            (_Val4 := true) <;>
                                                                                                            candidateResultSolve
                                                                                                        · apply Rewrites.tran
                                                                                                          · exact Rewrites._665cd53
                                                                                                          · apply Rewrites.tran
                                                                                                            · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                                                                                (HOLE := (@inj SortVal SortExpr)
                                                                                                                  (SortVal.inj_SortInt 48))
                                                                                                                (_Val0 := true) (_Val1 := true) <;>
                                                                                                                candidateResultSolve
                                                                                                            · apply Rewrites.tran
                                                                                                              · apply Rewrites._d9b5bba
                                                                                                                  (_Val0 := SortVal.inj_SortInt
                                                                                                                    (code - 48))
                                                                                                                rfl
                                                                                                              · apply Rewrites.tran
                                                                                                                · apply Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
                                                                                                                    (HOLE := (@inj SortVal SortExpr)
                                                                                                                      (SortVal.inj_SortInt
                                                                                                                        (code - 48)))
                                                                                                                    (_Val0 := true) (_Val1 := true) <;>
                                                                                                                    candidateResultSolve
                                                                                                                · apply Rewrites.tran
                                                                                                                  · apply Rewrites._d9b5bba
                                                                                                                      (_Val0 := SortVal.inj_SortInt
                                                                                                                        (a * 10 + (code - 48)))
                                                                                                                    rfl
                                                                                                                  · apply Rewrites.tran
                                                                                                                    · apply Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
                                                                                                                        (HOLE := (@inj SortVal SortExpr)
                                                                                                                          (SortVal.inj_SortInt
                                                                                                                            (a * 10 + (code - 48))))
                                                                                                                        (_Val0 := true) (_Val1 := true) <;>
                                                                                                                        candidateResultSolve
                                                                                                                    · apply Rewrites.tran
                                                                                                                      · exact candidateAssignInt
                                                                                                                          "a" (a * 10 + (code - 48))
                                                                                                                          xarg narg 0 a b c d
                                                                                                                          (candidateCharValue code)
                                                                                                                          0 (a * 10 + (code - 48)) b c d
                                                                                                                          _ _ _ _ _ _ _ _ _
                                                                                                                          (candidateUpdateA
                                                                                                                            (a * 10 + (code - 48))
                                                                                                                            xarg narg 0 a b c d
                                                                                                                            (candidateCharValue code))
                                                                                                                      · apply Rewrites.tran
                                                                                                                        · exact Rewrites._2a0ddee
                                                                                                                        · apply Rewrites.tran
                                                                                                                          · exact Rewrites._2a0ddee
                                                                                                                          · apply Rewrites.tran
                                                                                                                            · exact Rewrites._2a0ddee
                                                                                                                            · apply Rewrites.tran
                                                                                                                              · apply Rewrites._d499ad9
                                                                                                                                rfl
                                                                                                                              · simpa [candidateLoopStart,
                                                                                                                                  candidateLoopEnd,
                                                                                                                                  «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                                                                                                  hSlash, hValid.1] using
                                                                                                                                  (ih xarg narg 0
                                                                                                                                    (a * 10 + (code - 48))
                                                                                                                                    b c d
                                                                                                                                    (candidateCharValue code)
                                                                                                                                    exitCode counter hValid.2)
                · by_cases hp1 : phase = 1
                  · subst phase
                    by_cases hSlash : code = 47
                    · subst code
                      simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                        «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                      candidateScanSteps
                      apply Rewrites.tran
                      · exact candidateCompareLeftValue
                          (candidateCharValue 47) _ _ _ _ _ _ _ _ _ _ _ _
                      · apply Rewrites.tran
                        · apply Rewrites._e1122bd <;> rfl
                        · apply Rewrites.tran
                          · apply Rewrites._00b027a
                              (_Val0 := SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                                47 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
                            rfl
                          · apply Rewrites.tran
                            · simpa only [candidateCharValue] using
                                (Rewrites._aae3b52
                                  (HOLE := (@inj SortVal SortExpr)
                                    (candidateCharValue 47))
                                  (_Gen0 := candidateCharValue 47)
                                  (_Val0 := true) (_Val1 := true)
                                  (by
                                    unfold isKResult
                                    simp
                                    exact Or.inl rfl)
                                  (by rfl) (by rfl))
                            · apply Rewrites.tran
                              · apply Rewrites._a00964a (_Val0 := true)
                                simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
                                  _03e60c5, candidateCharValue, _root_.«_==K_»]
                              · apply Rewrites.tran
                                · exact candidateResolveIfTrue
                                    _ _ _ _ _ _ _ _ _ _ _ _ _
                                · apply Rewrites.tran
                                  · exact Rewrites._94bd14e
                                  · apply Rewrites.tran
                                    · exact candidateAssignPartStep 1 xarg narg
                                        a b c d (candidateCharValue 47)
                                        _ exitCode counter
                                    · apply Rewrites.tran
                                      · exact Rewrites._2a0ddee
                                      · apply Rewrites.tran
                                        · exact Rewrites._2a0ddee
                                        · apply Rewrites.tran
                                          · apply Rewrites._d499ad9
                                            rfl
                                          · simpa [candidateLoopStart,
                                              candidateLoopEnd,
                                              «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»] using
                                              (ih xarg narg 2 a b c d
                                                (candidateCharValue 47)
                                                exitCode counter hValid)
                    · simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                        «isDigitC(_)_MPY-METHODS_Bool_Int», hSlash] at hValid
                      apply Rewrites.tran
                      · exact candidateSlashIfFalse code _ _ _ xarg narg 1
                          a b c d exitCode counter hSlash
                      · apply Rewrites.tran
                        · exact Rewrites._94bd14e
                        · apply Rewrites.tran
                          · exact candidatePartIfFalse 1 0 _ _ _ xarg narg
                              a b c d (candidateCharValue code)
                              exitCode counter (by omega)
                          · apply Rewrites.tran
                            · exact Rewrites._94bd14e
                            · apply Rewrites.tran
                              · exact candidatePartIfTrue 1 _ _ _ xarg narg
                                  a b c d (candidateCharValue code)
                                  exitCode counter
                              · apply Rewrites.tran
                                · exact Rewrites._94bd14e
                                · apply Rewrites.tran
                                  · exact candidateDigitAssignStep "b" b code
                                      xarg narg 1 a b c d
                                      1 a (b * 10 + (code - 48)) c d
                                      _ exitCode counter
                                      (candidateContainsB xarg narg 1 a b c d
                                        (candidateCharValue code))
                                      (candidateMapLookupB xarg narg 1 a b c d
                                        (candidateCharValue code))
                                      (candidateUpdateB (b * 10 + (code - 48))
                                        xarg narg 1 a b c d
                                        (candidateCharValue code))
                                  · apply Rewrites.tran
                                    · exact Rewrites._2a0ddee
                                    · apply Rewrites.tran
                                      · exact Rewrites._2a0ddee
                                      · apply Rewrites.tran
                                        · exact Rewrites._2a0ddee
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · apply Rewrites._d499ad9
                                              rfl
                                            · simpa [candidateLoopStart,
                                                candidateLoopEnd,
                                                «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                «isDigitC(_)_MPY-METHODS_Bool_Int»,
                                                hSlash, hValid.1] using
                                                (ih xarg narg 1 a
                                                  (b * 10 + (code - 48)) c d
                                                  (candidateCharValue code)
                                                  exitCode counter hValid.2)
                  · by_cases hp2 : phase = 2
                    · subst phase
                      by_cases hSlash : code = 47
                      · subst code
                        simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                        apply Rewrites.tran
                        · exact candidateSlashIfTrue _ _ _ xarg narg 2
                            a b c d exitCode counter
                        · apply Rewrites.tran
                          · exact Rewrites._94bd14e
                          · apply Rewrites.tran
                            · exact candidateAssignPartStep 2 xarg narg a b c d
                                (candidateCharValue 47) _ exitCode counter
                            · apply Rewrites.tran
                              · exact Rewrites._2a0ddee
                              · apply Rewrites.tran
                                · exact Rewrites._2a0ddee
                                · apply Rewrites.tran
                                  · apply Rewrites._d499ad9
                                    rfl
                                  · simpa [candidateLoopStart,
                                      candidateLoopEnd,
                                      «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»] using
                                      (ih xarg narg 3 a b c d
                                        (candidateCharValue 47)
                                        exitCode counter hValid)
                      · simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          «isDigitC(_)_MPY-METHODS_Bool_Int», hSlash] at hValid
                        apply Rewrites.tran
                        · exact candidateSlashIfFalse code _ _ _ xarg narg 2
                            a b c d exitCode counter hSlash
                        · apply Rewrites.tran
                          · exact Rewrites._94bd14e
                          · apply Rewrites.tran
                            · exact candidatePartIfFalse 2 0 _ _ _ xarg narg
                                a b c d (candidateCharValue code)
                                exitCode counter (by omega)
                            · apply Rewrites.tran
                              · exact Rewrites._94bd14e
                              · apply Rewrites.tran
                                · exact candidatePartIfFalse 2 1 _ _ _ xarg narg
                                    a b c d (candidateCharValue code)
                                    exitCode counter (by omega)
                                · apply Rewrites.tran
                                  · exact Rewrites._94bd14e
                                  · apply Rewrites.tran
                                    · exact candidatePartIfTrue 2 _ _ _ xarg narg
                                        a b c d (candidateCharValue code)
                                        exitCode counter
                                    · apply Rewrites.tran
                                      · exact Rewrites._94bd14e
                                      · apply Rewrites.tran
                                        · exact candidateDigitAssignStep "c" c code
                                            xarg narg 2 a b c d
                                            2 a b (c * 10 + (code - 48)) d
                                            _ exitCode counter
                                            (candidateContainsC xarg narg 2 a b c d
                                              (candidateCharValue code))
                                            (candidateMapLookupC xarg narg 2 a b c d
                                              (candidateCharValue code))
                                            (candidateUpdateC (c * 10 + (code - 48))
                                              xarg narg 2 a b c d
                                              (candidateCharValue code))
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · exact Rewrites._2a0ddee
                                            · apply Rewrites.tran
                                              · exact Rewrites._2a0ddee
                                              · apply Rewrites.tran
                                                · exact Rewrites._2a0ddee
                                                · apply Rewrites.tran
                                                  · exact Rewrites._2a0ddee
                                                  · apply Rewrites.tran
                                                    · apply Rewrites._d499ad9
                                                      rfl
                                                    · simpa [candidateLoopStart,
                                                        candidateLoopEnd,
                                                        «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                        «isDigitC(_)_MPY-METHODS_Bool_Int»,
                                                        hSlash, hValid.1] using
                                                        (ih xarg narg 2 a b
                                                          (c * 10 + (code - 48)) d
                                                          (candidateCharValue code)
                                                          exitCode counter hValid.2)
                    · have hp3 : phase = 3 := Classical.byContradiction (fun hp3 => by
                        simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                          hp0, hp1, hp2, hp3] at hValid)
                      subst phase
                      simp [«validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                        «isDigitC(_)_MPY-METHODS_Bool_Int»] at hValid
                      have hSlash : code ≠ 47 := by
                        intro hCode
                        subst code
                        exact (by decide : ¬ (48 : SortInt) ≤ 47) hValid.1.1
                      apply Rewrites.tran
                      · exact candidateSlashIfFalse code _ _ _ xarg narg 3
                          a b c d exitCode counter hSlash
                      · apply Rewrites.tran
                        · exact Rewrites._94bd14e
                        · apply Rewrites.tran
                          · exact candidatePartIfFalse 3 0 _ _ _ xarg narg
                              a b c d (candidateCharValue code)
                              exitCode counter (by omega)
                          · apply Rewrites.tran
                            · exact Rewrites._94bd14e
                            · apply Rewrites.tran
                              · exact candidatePartIfFalse 3 1 _ _ _ xarg narg
                                  a b c d (candidateCharValue code)
                                  exitCode counter (by omega)
                              · apply Rewrites.tran
                                · exact Rewrites._94bd14e
                                · apply Rewrites.tran
                                  · exact candidatePartIfFalse 3 2 _ _ _ xarg narg
                                      a b c d (candidateCharValue code)
                                      exitCode counter (by omega)
                                  · apply Rewrites.tran
                                    · exact Rewrites._94bd14e
                                    · apply Rewrites.tran
                                      · exact candidateDigitAssignStep "d" d code
                                          xarg narg 3 a b c d
                                          3 a b c (d * 10 + (code - 48))
                                          _ exitCode counter
                                          (candidateContainsD xarg narg 3 a b c d
                                            (candidateCharValue code))
                                          (candidateMapLookupD xarg narg 3 a b c d
                                            (candidateCharValue code))
                                          (candidateUpdateD (d * 10 + (code - 48))
                                            xarg narg 3 a b c d
                                            (candidateCharValue code))
                                      · apply Rewrites.tran
                                        · exact Rewrites._2a0ddee
                                        · apply Rewrites.tran
                                          · exact Rewrites._2a0ddee
                                          · apply Rewrites.tran
                                            · exact Rewrites._2a0ddee
                                            · apply Rewrites.tran
                                              · exact Rewrites._2a0ddee
                                              · apply Rewrites.tran
                                                · exact Rewrites._2a0ddee
                                                · apply Rewrites.tran
                                                  · apply Rewrites._d499ad9
                                                    rfl
                                                  · simpa [candidateLoopStart,
                                                      candidateLoopEnd,
                                                      «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int»,
                                                      «isDigitC(_)_MPY-METHODS_Bool_Int»,
                                                      hSlash, hValid.1] using
                                                      (ih xarg narg 3 a b c
                                                        (d * 10 + (code - 48))
                                                        (candidateCharValue code)
                                                        exitCode counter hValid.2)

set_option maxHeartbeats 10000000 in
private theorem candidateMergeRootCallee
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _root_._Map_ candidateRootSingleton
        (candidateCalleeSingleton xarg narg phase a b c d ch) =
      some (candidateWithoutBuiltins xarg narg phase a b c d ch) := by
  unfold _root_._Map_ candidateRootSingleton candidateCalleeSingleton
    candidateWithoutBuiltins
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true, eq_self]
  all_goals (try rfl)
  all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
  all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
  all_goals (candidateUnfoldMapModels; simp)

private theorem candidateMergeWithoutBuiltins
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _root_._Map_ (candidateWithoutBuiltins xarg narg phase a b c d ch)
        candidateBuiltinSingleton =
      some (candidateActiveScopes xarg narg phase a b c d ch) := by
  unfold _root_._Map_ candidateWithoutBuiltins candidateBuiltinSingleton
    candidateActiveScopes
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true, eq_self]
  all_goals (try rfl)
  all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
  all_goals (try (candidateUnfoldMapModels; try simp; try rfl))

private theorem candidateMergePersistentRight :
    _root_._Map_ candidateRootSingleton candidateBuiltinSingleton =
      some candidatePersistentScopes := by
  unfold _root_._Map_ candidateRootSingleton candidateBuiltinSingleton
    candidatePersistentScopes
  rw [if_pos (by
    candidateUnfoldMapModels
    candidateUnfoldMapModels
    simp
    all_goals (try rfl)
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (try (candidateUnfoldMapModels; try simp; try rfl))
    all_goals (candidateUnfoldMapModels; simp))]
  candidateUnfoldMapModels
  simp only [List.foldr, Int.reduceLT, decide_true, decide_false, if_true,
    if_false, Bool.false_eq_true, eq_self]
  candidateUnfoldMapModels
  rfl

private theorem candidateTargetActiveScopes
    (xarg narg : SortVal) (phase a b c d : SortInt) (ch : SortVal) :
    _Map_
        (_Map_
          («_|->_» (SortKItem.inj_SortInt 0)
            (SortKItem.inj_SortScope
              (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
                (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))))
          («_|->_» (SortKItem.inj_SortInt 1)
            (SortKItem.inj_SortScope
              («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
                xarg narg phase a b c d ch))))
        («_|->_» (SortKItem.inj_SortInt (-1))
          (SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»)) =
      candidateActiveScopes xarg narg phase a b c d ch := by
  have hRoot :
      «_|->_» (SortKItem.inj_SortInt 0)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
              (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))) =
        candidateRootSingleton := by
    unfold «_|->_» _root_.«_|->_» «.Map» candidateRootSingleton
    rfl
  have hCallee :
      «_|->_» (SortKItem.inj_SortInt 1)
          (SortKItem.inj_SortScope
            («simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val»
              xarg narg phase a b c d ch)) =
        candidateCalleeSingleton xarg narg phase a b c d ch := by
    unfold «_|->_» _root_.«_|->_» «.Map» candidateCalleeSingleton
    rfl
  have hBuiltin :
      «_|->_» (SortKItem.inj_SortInt (-1))
          (SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope») =
        candidateBuiltinSingleton := by
    unfold «_|->_» _root_.«_|->_» «.Map» candidateBuiltinSingleton
    rfl
  rw [hRoot, hCallee, hBuiltin]
  unfold _Map_
  rw [candidateMergeRootCallee]
  simp only [Option.getD_some]
  rw [candidateMergeWithoutBuiltins]
  rfl

set_option maxHeartbeats 10000000 in
private theorem candidateTargetPersistentScopes :
    _Map_
        («_|->_» (SortKItem.inj_SortInt 0)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
              (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))))
        («_|->_» (SortKItem.inj_SortInt (-1))
          (SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope»)) =
      candidatePersistentScopes := by
  have hRoot :
      «_|->_» (SortKItem.inj_SortInt 0)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» «.Map»
              (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))) =
        candidateRootSingleton := by
    unfold «_|->_» _root_.«_|->_» «.Map» candidateRootSingleton
    rfl
  have hBuiltin :
      «_|->_» (SortKItem.inj_SortInt (-1))
          (SortKItem.inj_SortScope «builtinsScope_MPY-CORE_Scope») =
        candidateBuiltinSingleton := by
    unfold «_|->_» _root_.«_|->_» «.Map» candidateBuiltinSingleton
    rfl
  rw [hRoot, hBuiltin]
  unfold _Map_
  rw [candidateMergePersistentRight]
  rfl

theorem final :
    Klean144Simplify.Lemmas.targetStatement «.List» «.Map» _Map_ _andBool_ «_<Int_» «_<=Int_» «_==K_» «_|->_» ListItem «builtinsScope_MPY-CORE_Scope» «isDigitC(_)_MPY-METHODS_Bool_Int» «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» «simplifyLoopBody_VERIFICATION-SYNTAX_Stmts» «simplifyReturn_VERIFICATION-SYNTAX_Stmt» «simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val» «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» := by
  unfold Klean144Simplify.Lemmas.targetStatement
  constructor
  · intro _Gen1 _Gen0 BUILTINSSCOPE CALLEESCOPE RETSTMTS LOOPBODY
      REST CODE D C B A P OLDCH NARG XARG h
    simp only [_andBool_, Bool.and_eq_true, «_==K_»,
      decide_eq_true_eq, «_<=Int_»,
      «isDigitC(_)_MPY-METHODS_Bool_Int»] at h
    rcases h with ⟨⟨⟨⟨⟨⟨⟨hBody, hReturn⟩, hScope⟩, hBuiltins⟩,
      hPhaseLo⟩, hPhaseHi⟩, hDigit⟩, hValid⟩
    obtain ⟨rfl, _⟩ := hBody
    obtain ⟨rfl, _⟩ := hReturn
    obtain ⟨rfl, _⟩ := hScope
    obtain ⟨rfl, _⟩ := hBuiltins
    simpa only [candidateLoopStart, candidateLoopEnd,
      candidateTargetActiveScopes, candidateTargetPersistentScopes] using
      (candidateLoopSound
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST)
        XARG NARG P A B C D OLDCH _Gen0 _Gen1 hValid)
  · intro _Gen1 _Gen0 BUILTINSSCOPE CALLEESCOPE RETSTMTS LOOPBODY
      REST D C B A P OLDCH NARG XARG h
    simp only [_andBool_, Bool.and_eq_true, «_==K_»,
      decide_eq_true_eq, «_<=Int_», «_<Int_»] at h
    rcases h with ⟨⟨⟨⟨⟨⟨hBody, hReturn⟩, hScope⟩, hBuiltins⟩,
      hPhaseLo⟩, hPhaseHi⟩, hValid⟩
    obtain ⟨rfl, _⟩ := hBody
    obtain ⟨rfl, _⟩ := hReturn
    obtain ⟨rfl, _⟩ := hScope
    obtain ⟨rfl, _⟩ := hBuiltins
    simpa only [candidateLoopStart, candidateLoopEnd,
      candidateTargetActiveScopes, candidateTargetPersistentScopes] using
      (candidateLoopSound
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 REST)
        XARG NARG P A B C D OLDCH _Gen0 _Gen1 hValid)

end Proof
