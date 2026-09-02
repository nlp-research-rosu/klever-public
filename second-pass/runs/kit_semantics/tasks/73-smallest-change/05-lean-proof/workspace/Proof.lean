import Klean73SmallestChange.Lemmas
import Lean.Elab.Tactic.Omega
import Lean.Meta.Tactic.Delta

namespace Proof

open Lean Meta Elab Tactic

set_option maxHeartbeats 0

elab "deltaPrivateMapModels" : tactic => do
  let goal ← getMainGoal
  let goal ← goal.deltaTarget fun name =>
    name.toString.endsWith "kleanMapLookupModel" ||
      name.toString.endsWith "kleanMapContainsModel" ||
      name.toString.endsWith "kleanMapDisjointModel" ||
      name.toString.endsWith "kleanMapDeleteModel" ||
      name.toString.endsWith "kleanMapInsertModel" ||
      name.toString.endsWith "kleanMapUpdateModel"
  replaceMainGoal [goal]

elab "deltaPrivateKeyOrderModel" : tactic => do
  let goal ← getMainGoal
  let goal ← goal.deltaTarget fun name =>
    name.toString.endsWith "kleanKeyOrderModel"
  replaceMainGoal [goal]

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

/- KORE symbol: Lbl'Stop'List; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «.List» : SortList := ⟨[]⟩
/- KORE symbol: Lbl'Stop'Map; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «.Map» : SortMap := ⟨[]⟩
/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y

noncomputable def mapContainsModel
    (entries : List (SortKItem × SortKItem)) (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true else mapContainsModel rest key

def mapKeyLtModel : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortInt left, SortKItem.inj_SortInt right => decide (left < right)
  | SortKItem.inj_SortInt _, _ => true
  | _, SortKItem.inj_SortInt _ => false
  | SortKItem.inj_SortString left, SortKItem.inj_SortString right =>
      decide (left < right)
  | SortKItem.inj_SortString _, _ => true
  | _, SortKItem.inj_SortString _ => false
  | _, _ => false

noncomputable def mapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if mapContainsModel left key then false else mapDisjointModel left rest

def mapInsertModel (key value : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if mapKeyLtModel candidate key then
        (candidate, oldValue) :: mapInsertModel key value rest
      else (key, value) :: (candidate, oldValue) :: rest

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def _Map_ (left right : SortMap) : SortMap :=
  if mapDisjointModel left.coll right.coll then
    ⟨left.coll.foldr (fun entry result =>
      mapInsertModel entry.1 entry.2 result) right.coll⟩
  else ⟨[]⟩
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x ≤ y)
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap := ⟨[(key, value)]⟩
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526, rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: LblListItem; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
def ListItem (item : SortKItem) : SortList := ⟨[item]⟩
/- KORE symbol: LblallInts'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791, rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt _) rest =>
      «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» rest
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => false

def valSeqLengthModel : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + valSeqLengthModel rest

def valSeqAtModel : SortValSeq → SortInt → SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => SortVal.inj_SortInt 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, index =>
      if index = 0 then value
      else if 0 < index then valSeqAtModel rest (index - 1)
      else SortVal.inj_SortInt 0

noncomputable def applyCmpModel
    (operator : SortString) (left right : SortVal) : Option SortBool :=
  _root_.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» operator left right

/- KORE symbol: LblhalfLen'LParUndsRParUnds'VERIFICATION-BASE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791, rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» (values : SortValSeq) : SortInt :=
  let n := valSeqLengthModel values
  Int.tdiv (n - Int.tmod (Int.tmod n 2 + 2) 2) 2
/- KORE symbol: LblmismatchCount'LParUndsCommUndsCommUndsRParUnds'VERIFICATION-BASE'Unds'Int'Unds'ValSeq'Unds'Int'Unds'Int; frozen source obligations: rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def pairDiffModel (values : SortValSeq) (index : SortInt) : SortInt :=
  let mirror := valSeqLengthModel values - index - 1
  match applyCmpModel
      "!="
      (valSeqAtModel values index)
      (valSeqAtModel values mirror) with
  | some true => 1
  | _ => 0

noncomputable def mismatchCountFuelModel
    (values : SortValSeq) (index : SortInt) : Nat → SortInt
  | 0 => 0
  | fuel + 1 =>
      pairDiffModel values index +
        mismatchCountFuelModel values (index + 1) fuel

noncomputable def «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»
    (values : SortValSeq) (index stop : SortInt) : SortInt :=
  if index ≥ stop then 0
  else mismatchCountFuelModel values index (stop - index).toNat
/- KORE symbol: LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
    (values : SortValSeq) (index : SortInt) : SortVal :=
  valSeqAtModel values index
/- KORE symbol: LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «vsLen(_)_MPY-CORE_Int_ValSeq» (values : SortValSeq) : SortInt :=
  valSeqLengthModel values
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val?»
    (operator : SortString) (left right : SortVal) : Option SortBool :=
  applyCmpModel operator left right

def emptyStmts : SortStmts :=
  SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»

def oneStmt (statement : SortStmt) (rest : SortStmts := emptyStmts) : SortStmts :=
  SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» statement rest

def nameExpr (name : SortString) : SortExpr :=
  SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» name

def intExpr (value : SortInt) : SortExpr :=
  SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» value

def lenArrExpr : SortExpr :=
  SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (nameExpr "len")
    (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (nameExpr "arr")
      SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)

def halfExpr : SortExpr :=
  SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//"
    lenArrExpr (intExpr 2)

def loopCondExpr : SortExpr :=
  SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (nameExpr "i")
    (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" halfExpr)

def mirrorIndexExpr : SortExpr :=
  SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-"
    (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-"
      lenArrExpr (nameExpr "i")) (intExpr 1)

def indexedArrExpr (index : SortExpr) : SortExpr :=
  SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (nameExpr "arr")
    ((@inj SortExpr SortIndex) index)

def pairCondExpr : SortExpr :=
  SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
    (indexedArrExpr (nameExpr "i"))
    (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "!="
      (indexedArrExpr mirrorIndexExpr))

def incrementChangesStmt : SortStmt :=
  SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
    (nameExpr "changes") "+" (intExpr 1)

def incrementIndexStmt : SortStmt :=
  SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
    (nameExpr "i") "+" (intExpr 1)

def loopBodyStmts : SortStmts :=
  oneStmt
    (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» pairCondExpr
      (oneStmt incrementChangesStmt) emptyStmts)
    (oneStmt incrementIndexStmt)

def returnStmts : SortStmts :=
  oneStmt (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (nameExpr "changes"))

def functionBodyStmts : SortStmts :=
  oneStmt
    (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
      (nameExpr "changes") (intExpr 0))
    (oneStmt
      (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
        (nameExpr "i") (intExpr 0))
      (oneStmt
        (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts»
          loopCondExpr loopBodyStmts)
        returnStmts))

def builtinBindings : SortMap :=
  ⟨[
    (SortKItem.inj_SortString "abs", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs")),
    (SortKItem.inj_SortString "all", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all")),
    (SortKItem.inj_SortString "any", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any")),
    (SortKItem.inj_SortString "bin", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin")),
    (SortKItem.inj_SortString "chr", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr")),
    (SortKItem.inj_SortString "enumerate", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate")),
    (SortKItem.inj_SortString "eval", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval")),
    (SortKItem.inj_SortString "float", (@inj SortVal SortKItem) (SortVal.«typeV(_)_MPY-CORE_Val_String» "float")),
    (SortKItem.inj_SortString "int", (@inj SortVal SortKItem) (SortVal.«typeV(_)_MPY-CORE_Val_String» "int")),
    (SortKItem.inj_SortString "isinstance", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance")),
    (SortKItem.inj_SortString "len", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")),
    (SortKItem.inj_SortString "list", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list")),
    (SortKItem.inj_SortString "map", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map")),
    (SortKItem.inj_SortString "max", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max")),
    (SortKItem.inj_SortString "min", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min")),
    (SortKItem.inj_SortString "ord", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord")),
    (SortKItem.inj_SortString "range", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range")),
    (SortKItem.inj_SortString "round", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round")),
    (SortKItem.inj_SortString "set", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set")),
    (SortKItem.inj_SortString "sorted", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted")),
    (SortKItem.inj_SortString "str", (@inj SortVal SortKItem) (SortVal.«typeV(_)_MPY-CORE_Val_String» "str")),
    (SortKItem.inj_SortString "sum", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")),
    (SortKItem.inj_SortString "zip", (@inj SortVal SortKItem) (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip"))
  ]⟩

def globalBindings : SortMap :=
  ⟨[(SortKItem.inj_SortString "smallest_change",
    (@inj SortVal SortKItem)
      (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int»
        (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "arr"
          SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»)
        functionBodyStmts 0))]⟩

def outerMinusEntry : SortKItem × SortKItem :=
  (SortKItem.inj_SortInt (-1), SortKItem.inj_SortScope
    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» builtinBindings
      SortParent.«root_MPY-CORE_Parent»))

def outerZeroEntry : SortKItem × SortKItem :=
  (SortKItem.inj_SortInt 0, SortKItem.inj_SortScope
    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» globalBindings
      (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1))))

def outerScopes : SortMap := ⟨[outerMinusEntry, outerZeroEntry]⟩

def localBindings (values : SortValSeq) (changes index : SortInt) : SortMap :=
  ⟨[
    (SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)),
    (SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes),
    (SortKItem.inj_SortString "i", SortKItem.inj_SortInt index)
  ]⟩

def activeScopes (values : SortValSeq) (changes index : SortInt) : SortMap :=
  ⟨outerScopes.coll ++ [
    (SortKItem.inj_SortInt 1, SortKItem.inj_SortScope
      (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (localBindings values changes index)
        (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)))
  ]⟩

def localScopeSingleton (values : SortValSeq) (changes index : SortInt) : SortMap :=
  ⟨[(SortKItem.inj_SortInt 1, SortKItem.inj_SortScope
    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
      (localBindings values changes index)
      (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)))]⟩

def localScopeEntry (values : SortValSeq) (changes index : SortInt) :
    SortKItem × SortKItem :=
  (SortKItem.inj_SortInt 1, SortKItem.inj_SortScope
    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
      (localBindings values changes index)
      (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)))

def globalScopeSingleton : SortMap := ⟨[outerZeroEntry]⟩

def builtinsScopeSingleton : SortMap := ⟨[outerMinusEntry]⟩

def scopesWithoutGlobal (values : SortValSeq) (changes index : SortInt) : SortMap :=
  ⟨[outerMinusEntry, localScopeEntry values changes index]⟩

def scopesWithoutBuiltins (values : SortValSeq) (changes index : SortInt) : SortMap :=
  ⟨[outerZeroEntry, localScopeEntry values changes index]⟩

theorem generated_merge_local_outer
    (values : SortValSeq) (changes index : SortInt) :
    _root_._Map_ (localScopeSingleton values changes index) outerScopes =
      some (activeScopes values changes index) := by
  simp only [_root_._Map_, localScopeSingleton, outerScopes]
  change
    (if
      (if
        (if SortKItem.inj_SortInt 1 = SortKItem.inj_SortInt (-1)
          then true else false)
        then false
        else if
          (if SortKItem.inj_SortInt 1 = SortKItem.inj_SortInt 0
            then true else false)
          then false else true)
     then
       some ⟨
         if decide ((-1 : Int) < 1) then
           outerMinusEntry ::
             (if decide ((0 : Int) < 1) then
               outerZeroEntry ::
                 [(SortKItem.inj_SortInt 1,
                   SortKItem.inj_SortScope
                     (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                       (localBindings values changes index)
                       (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)))]
              else [])
          else []⟩
     else none) = some (activeScopes values changes index)
  simp [activeScopes, outerScopes]

theorem generated_merge_global_rest
    (values : SortValSeq) (changes index : SortInt) :
    _root_._Map_ globalScopeSingleton
      (scopesWithoutGlobal values changes index) =
      some (activeScopes values changes index) := by
  simp only [_root_._Map_, globalScopeSingleton, scopesWithoutGlobal]
  change
    (if
      (if
        (if SortKItem.inj_SortInt 0 = SortKItem.inj_SortInt (-1)
          then true else false)
        then false
        else if
          (if SortKItem.inj_SortInt 0 = SortKItem.inj_SortInt 1
            then true else false)
          then false else true)
     then
       some ⟨
         if decide ((-1 : Int) < 0) then
           outerMinusEntry ::
             (if decide ((1 : Int) < 0) then
               localScopeEntry values changes index :: [outerZeroEntry]
              else outerZeroEntry :: [localScopeEntry values changes index])
          else outerZeroEntry ::
            [outerMinusEntry, localScopeEntry values changes index]⟩
     else none) = some (activeScopes values changes index)
  simp [activeScopes, outerScopes, localScopeEntry]

theorem generated_merge_builtins_rest
    (values : SortValSeq) (changes index : SortInt) :
    _root_._Map_ builtinsScopeSingleton
      (scopesWithoutBuiltins values changes index) =
      some (activeScopes values changes index) := by
  simp only [_root_._Map_, builtinsScopeSingleton, scopesWithoutBuiltins]
  change
    (if
      (if
        (if SortKItem.inj_SortInt (-1) = SortKItem.inj_SortInt 0
          then true else false)
        then false
        else if
          (if SortKItem.inj_SortInt (-1) = SortKItem.inj_SortInt 1
            then true else false)
          then false else true)
     then
       some ⟨
         if decide ((0 : Int) < (-1)) then
           outerZeroEntry ::
             [outerMinusEntry, localScopeEntry values changes index]
          else outerMinusEntry ::
            [outerZeroEntry, localScopeEntry values changes index]⟩
     else none) = some (activeScopes values changes index)
  simp [activeScopes, outerScopes, localScopeEntry]

theorem eval_name_i
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) (nameExpr "i")) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt index) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply Rewrites.tran Rewrites._6d39855
  refine Rewrites._db779c6
    (L := 1) (M := localBindings values changes index) (_DotVar2 := outerScopes)
    (X := "i") (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := true) (_Val1 := localScopeSingleton values changes index)
    (_Val2 := activeScopes values changes index)
    (_Val3 := SortKItem.inj_SortInt index)
    (_Val4 := SortVal.inj_SortInt index)
    (_Val5 := localScopeSingleton values changes index)
    (_Val6 := activeScopes values changes index) ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_
  · change _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      (SortKItem.inj_SortString "i") (localBindings values changes index) = some true
    simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», localBindings,
      Option.some.injEq]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "i" then true
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "i" then true
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "i" then true
       else false) = true
    simp
  · change some (localScopeSingleton values changes index) =
      some (localScopeSingleton values changes index)
    rfl
  · exact generated_merge_local_outer values changes index
  · change _root_.«Map:lookup» (localBindings values changes index)
      (SortKItem.inj_SortString "i") = some (SortKItem.inj_SortInt index)
    simp only [_root_.«Map:lookup», localBindings]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "i" then
         some (SortKItem.inj_SortIterable
           (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "i" then
         some (SortKItem.inj_SortInt changes)
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "i" then
         some (SortKItem.inj_SortInt index)
       else none) = some (SortKItem.inj_SortInt index)
    simp
  · change some (SortVal.inj_SortInt index) = some (SortVal.inj_SortInt index)
    rfl
  · change some (localScopeSingleton values changes index) =
      some (localScopeSingleton values changes index)
    rfl
  · exact generated_merge_local_outer values changes index
  · rfl

theorem eval_local_name
    (values : SortValSeq) (changes index : SortInt)
    (variableName : SortString) (value : SortVal) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hContains : _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      ((@inj SortString SortKItem) variableName)
      (localBindings values changes index) = some true)
    (hLookup : _root_.«Map:lookup» (localBindings values changes index)
      ((@inj SortString SortKItem) variableName) =
        some ((@inj SortVal SortKItem) value))
    (hProject : _root_.«project:Val»
      (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) = some value) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) (nameExpr variableName)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq ((@inj SortVal SortKItem) value) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply Rewrites.tran Rewrites._6d39855
  refine Rewrites._db779c6
    (L := 1) (M := localBindings values changes index) (_DotVar2 := outerScopes)
    (X := variableName) (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (_Val0 := true) (_Val1 := localScopeSingleton values changes index)
    (_Val2 := activeScopes values changes index)
    (_Val3 := ((@inj SortVal SortKItem) value)) (_Val4 := value)
    (_Val5 := localScopeSingleton values changes index)
    (_Val6 := activeScopes values changes index)
    hContains (by change some (localScopeSingleton values changes index) = _; rfl)
    (generated_merge_local_outer values changes index) hLookup hProject
    (by change some (localScopeSingleton values changes index) = _; rfl)
    (generated_merge_local_outer values changes index) rfl

theorem eval_name_changes
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) (nameExpr "changes")) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt changes) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply eval_local_name values changes index "changes" (SortVal.inj_SortInt changes)
  · simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», localBindings,
      Option.some.injEq]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "changes" then true
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "changes" then true
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "changes" then true
       else false) = true
    simp
  · simp only [_root_.«Map:lookup», localBindings]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "changes" then
         some (SortKItem.inj_SortIterable
           (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "changes" then
         some (SortKItem.inj_SortInt changes)
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "changes" then
         some (SortKItem.inj_SortInt index)
       else none) = some (SortKItem.inj_SortInt changes)
    simp
  · change some (SortVal.inj_SortInt changes) = some (SortVal.inj_SortInt changes)
    rfl

theorem eval_name_arr
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) (nameExpr "arr")) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply eval_local_name values changes index "arr"
    (SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
  · simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», localBindings,
      Option.some.injEq]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "arr" then true
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "arr" then true
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "arr" then true
       else false) = true
    simp
  · simp only [_root_.«Map:lookup», localBindings]
    change
      (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "arr" then
         some (SortKItem.inj_SortIterable
           (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
       else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "arr" then
         some (SortKItem.inj_SortInt changes)
       else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "arr" then
         some (SortKItem.inj_SortInt index)
       else none) = some (SortKItem.inj_SortIterable
         (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
    simp
  · change
      some (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) =
      some (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
    rfl

theorem generated_local_not_contains_len
    (values : SortValSeq) (changes index : SortInt) :
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      (SortKItem.inj_SortString "len") (localBindings values changes index) =
      some false := by
  simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», localBindings,
    Option.some.injEq]
  change
    (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "len" then true
     else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "len" then true
     else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "len" then true
     else false) = false
  simp

theorem generated_global_not_contains_len :
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      (SortKItem.inj_SortString "len") globalBindings = some false := by
  simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», globalBindings,
    Option.some.injEq]
  change
    (if SortKItem.inj_SortString "smallest_change" = SortKItem.inj_SortString "len"
      then true else false) = false
  simp

theorem generated_builtins_contains_len :
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      (SortKItem.inj_SortString "len") builtinBindings = some true := by
  simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», builtinBindings,
    Option.some.injEq]
  change (if SortKItem.inj_SortString "abs" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "all" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "any" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "bin" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "chr" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "enumerate" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "eval" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "float" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "int" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "isinstance" = SortKItem.inj_SortString "len"
    then true else _) = true
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "len" = SortKItem.inj_SortString "len"
    then true else _) = true
  simp

theorem generated_builtins_lookup_len :
    _root_.«Map:lookup» builtinBindings (SortKItem.inj_SortString "len") =
      some ((@inj SortVal SortKItem)
        (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")) := by
  simp only [_root_.«Map:lookup», builtinBindings]
  change (if SortKItem.inj_SortString "abs" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "all" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "any" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "bin" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "chr" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "enumerate" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "eval" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "float" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "int" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "isinstance" = SortKItem.inj_SortString "len"
    then _ else _) = _
  rw [if_neg (by simp)]
  change (if SortKItem.inj_SortString "len" = SortKItem.inj_SortString "len"
    then some ((@inj SortVal SortKItem)
      (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")) else _) = _
  simp

theorem eval_name_len
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) (nameExpr "len")) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq ((@inj SortVal SortKItem)
          (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply Rewrites.tran Rewrites._6d39855
  apply Rewrites.tran
  · refine Rewrites._10452d5
      (L := 1) (P := 0) (M := localBindings values changes index)
      (_DotVar2 := outerScopes) (_Val0 := false) (_Val1 := true)
      (_Val2 := localScopeSingleton values changes index)
      (_Val3 := activeScopes values changes index)
      (_Val4 := localScopeSingleton values changes index)
      (_Val5 := activeScopes values changes index)
      (generated_local_not_contains_len values changes index) rfl
      (by change some (localScopeSingleton values changes index) = _; rfl)
      (generated_merge_local_outer values changes index)
      (by change some (localScopeSingleton values changes index) = _; rfl)
      (generated_merge_local_outer values changes index) rfl
  · apply Rewrites.tran
    · refine Rewrites._10452d5
        (L := 0) (P := -1) (M := globalBindings)
        (_DotVar2 := scopesWithoutGlobal values changes index)
        (_Val0 := false) (_Val1 := true) (_Val2 := globalScopeSingleton)
        (_Val3 := activeScopes values changes index)
        (_Val4 := globalScopeSingleton) (_Val5 := activeScopes values changes index)
        generated_global_not_contains_len rfl
        (by change some globalScopeSingleton = _; rfl)
        (generated_merge_global_rest values changes index)
        (by change some globalScopeSingleton = _; rfl)
        (generated_merge_global_rest values changes index) rfl
    · refine Rewrites._db779c6
        (L := -1) (M := builtinBindings)
        (_DotVar2 := scopesWithoutBuiltins values changes index)
        (X := "len") (_Gen0 := SortParent.«root_MPY-CORE_Parent»)
        (_Val0 := true) (_Val1 := builtinsScopeSingleton)
        (_Val2 := activeScopes values changes index)
        (_Val3 := ((@inj SortVal SortKItem)
          (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")))
        (_Val4 := SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")
        (_Val5 := builtinsScopeSingleton) (_Val6 := activeScopes values changes index)
        generated_builtins_contains_len
        (by change some builtinsScopeSingleton = _; rfl)
        (generated_merge_builtins_rest values changes index)
        generated_builtins_lookup_len
        (by change some (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len") = _; rfl)
        (by change some builtinsScopeSingleton = _; rfl)
        (generated_merge_builtins_rest values changes index) rfl

theorem generated_vsLen (values : SortValSeq) :
    _root_.«vsLen(_)_MPY-CORE_Int_ValSeq» values =
      some (valSeqLengthModel values) := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      simp [_root_.«vsLen(_)_MPY-CORE_Int_ValSeq», _root_._5d69a53,
        _root_._b662ad7, valSeqLengthModel]
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      simp [_root_.«vsLen(_)_MPY-CORE_Int_ValSeq», _root_._5d69a53,
        _root_._b662ad7, _root_.«_+Int_», valSeqLengthModel,
        generated_vsLen rest]
termination_by values

theorem generated_applyBuiltin_len (values : SortValSeq) :
    _root_.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "len"
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =
      some (SortVal.inj_SortInt (valSeqLengthModel values)) := by
  have hRetr : (@retr SortIterable SortVal)
      (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) =
      some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) := by
    rfl
  have hInj : (@inj SortInt SortVal) (valSeqLengthModel values) =
      SortVal.inj_SortInt (valSeqLengthModel values) := by
    rfl
  simp [_root_.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»,
    _root_._0d5862f, _root_._108b118, _root_._1b20c41, _root_._1de45ff,
    _root_._20b19cf, _root_._213f0c2, _root_._28eddda, _root_._2d8e778,
    _root_._437b04b, _root_._4807966, _root_._4b80f98, _root_._583f938,
    _root_._606434e, _root_._6d20a96, _root_._727142b, _root_._72eff8b,
    _root_._73630e2, _root_._853fa53, _root_._8f573a0, _root_._a4fd04a,
    _root_._a971c50, _root_._bb50555, _root_._d16bd47, _root_._d7fe6d3,
    _root_._dc46a10, _root_._e22316b, _root_._e4f0a30, _root_._e64428a,
    _root_._eb8c1ed, _root_._ecd3e5c, _root_._f1c888d,
    _root_.«seqLen(_)_MPY-BUILTINS_Int_Val», _root_._1719aa8,
    _root_._4b33ea6, _root_._8501a34, _root_._90ec921,
    _root_._d4293df, generated_vsLen, hRetr, hInj]

theorem eval_len_arr
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) lenArrExpr) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq
                    (SortKItem.inj_SortInt (valSeqLengthModel values)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let args := SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (nameExpr "arr")
    SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»
  let emptyVals := SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»
  let arrValue := SortVal.inj_SortIterable
    (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)
  let callee := SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"
  apply Rewrites.tran Rewrites._2d73ccf
  apply Rewrites.tran
    (eval_name_len values changes index
      (SortK.kseq (SortKItem.«#callee(_)_MPY-CALL_KItem_Exprs» args) tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran Rewrites._0619f01
  apply Rewrites.tran Rewrites._f0c4941
  apply Rewrites.tran
    (eval_name_arr values changes index
      (SortK.kseq
        (SortKItem.«#evalArgCont(_,_,_)_MPY-CORE_KItem_Exprs_Vals_ApplyK»
          SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» emptyVals
          (SortApplyK.«toCall(_)_MPY-CORE_ApplyK_Val» callee)) tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · refine Rewrites._c75b3bb
      (ACC := emptyVals) (V := arrValue)
      (_Val0 := SortVals.«_,__MPY-CORE_Vals_Val_Vals» arrValue emptyVals) ?_
    simp [emptyVals, arrValue, _root_.«appendVal(_,_)_MPY-CORE_Vals_Vals_Val»,
      _root_._1dc0c6c, _root_._b10f912]
  · apply Rewrites.tran Rewrites._4f8838c
    exact Rewrites._03fcca7 (generated_applyBuiltin_len values)

theorem generated_applyBin_half (n : SortInt) :
    _root_.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "//"
      (SortVal.inj_SortInt n) (SortVal.inj_SortInt 2) =
      some (SortVal.inj_SortInt
        (Int.tdiv (n - Int.tmod (Int.tmod n 2 + 2) 2) 2)) := by
  simp [_root_.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
    _root_._13d6ee6, _root_._1909c2e, _root_._2acce51, _root_._30456db,
    _root_._3598da3, _root_._42bfa12, _root_._4f03d42, _root_._4f373ea,
    _root_._50f1b5a, _root_._614d946, _root_._798d463, _root_._7f23ecf,
    _root_._7ff1b9f, _root_._a4f5818, _root_._a4f63fd, _root_._a6670cb,
    _root_._b009d60, _root_._bb59890, _root_._bc844c7, _root_._c2eab84,
    _root_._ca41a23, _root_._d8961f0, _root_._dece19f, _root_._e0a3283,
    _root_._ebcc6ed, _root_._f394023,
    _root_.«pyMod(_,_)_MPY-INT_Int_Int_Int», _root_._2d78aae,
    _root_.«_%Int_», _root_.«_+Int_», _root_.«_-Int_»,
    _root_.«_/Int_»]
  change SortVal.inj_SortInt
      (Int.tdiv (n - Int.tmod (Int.tmod n 2 + 2) 2) 2) = _
  rfl

theorem eval_half_expr
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) halfExpr) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt
          («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let freezerLeft :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_»
      (SortK.kseq (SortKItem.inj_SortString "//") SortK.dotk)
      (SortK.kseq ((@inj SortExpr SortKItem) (intExpr 2)) SortK.dotk)
  let n := valSeqLengthModel values
  let freezerRight :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_»
      (SortK.kseq (SortKItem.inj_SortString "//") SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortInt n) SortK.dotk)
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_len_arr values changes index (SortK.kseq freezerLeft tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · simpa [freezerLeft, n] using
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt n)))
        (K0 := "//") (K2 := intExpr 2) rfl rfl rfl :
        Rewrites
          { k := { val := SortK.kseq (SortKItem.inj_SortInt n)
                    (SortK.kseq freezerLeft tail) },
            env := { val := 1 }, scopes := { val := activeScopes values changes index },
            scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
            ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
          { k := { val := SortK.kseq ((@inj SortExpr SortKItem)
                    (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//"
                      ((@inj SortVal SortExpr) (SortVal.inj_SortInt n)) (intExpr 2))) tail },
            env := { val := 1 }, scopes := { val := activeScopes values changes index },
            scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
            ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter })
  · apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
        rfl rfl rfl rfl rfl rfl)
    apply Rewrites.tran (Rewrites._665cd53)
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt 2)))
        (K1 := ((@inj SortVal SortExpr) (SortVal.inj_SortInt n)))
        (K0 := "//") rfl rfl rfl)
    simpa [«halfLen(_)_VERIFICATION-BASE_Int_ValSeq», n] using
      (Rewrites._d9b5bba (generated_applyBin_half n) :
        Rewrites
          { k := { val := SortK.kseq ((@inj SortExpr SortKItem)
              (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//"
                ((@inj SortVal SortExpr) (SortVal.inj_SortInt n))
                ((@inj SortVal SortExpr) (SortVal.inj_SortInt 2)))) tail },
            env := { val := 1 }, scopes := { val := activeScopes values changes index },
            scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
            ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
          { k := { val := SortK.kseq (SortKItem.inj_SortInt
              (Int.tdiv (n - Int.tmod (Int.tmod n 2 + 2) 2) 2)) tail },
            env := { val := 1 }, scopes := { val := activeScopes values changes index },
            scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
            ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter })


theorem generated_applyCmp_lt (left right : SortInt) :
    _root_.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<"
      (SortVal.inj_SortInt left) (SortVal.inj_SortInt right) =
      some (decide (left < right)) := by
  rfl

theorem eval_loop_condition
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) loopCondExpr) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortBool
          (decide (index < «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let cmp := SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" halfExpr
  let leftFreezer :=
    SortKItem.«#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_»
      (SortK.kseq ((@inj SortCmpOp SortKItem) cmp) SortK.dotk)
  let rightFreezer :=
    SortKItem.«#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp2_»
      (SortK.kseq (SortKItem.inj_SortInt index) SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortString "<") SortK.dotk)
  apply Rewrites.tran (Rewrites._1f0e78f rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_name_i values changes index (SortK.kseq leftFreezer tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · simpa [cmp, leftFreezer] using
      (Rewrites._dfb9e43
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt index)))
        (_Gen0 := cmp) rfl rfl rfl)
  · apply Rewrites.tran (Rewrites._e1122bd rfl rfl rfl rfl)
    apply Rewrites.tran
      (eval_half_expr values changes index (SortK.kseq rightFreezer tail)
        scopeLoc heap heapLoc stack ret exc exitCode counter)
    apply Rewrites.tran
    · simpa [rightFreezer] using
        (Rewrites._aae3b52
          (HOLE := ((@inj SortVal SortExpr)
            (SortVal.inj_SortInt
              («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))))
          (_Gen0 := SortVal.inj_SortInt index) (_Gen1 := "<") rfl rfl rfl)
    · exact Rewrites._a00964a
        (generated_applyCmp_lt index
          («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))

theorem generated_valSeqAt_valid
    (values : SortValSeq) (index : SortInt)
    (hNonnegative : 0 ≤ index) (hBound : index < valSeqLengthModel values) :
    _root_.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» values index =
      some (valSeqAtModel values index) := by
  change Int at index
  change (0 : Int) ≤ index at hNonnegative
  change index < (valSeqLengthModel values : Int) at hBound
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      change index < 0 at hBound
      omega
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      by_cases hZero : index = 0
      · subst index
        cases hInner : _root_._86fc1c7 rest (-1) <;>
          simp [_root_.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»,
            _root_._86fc1c7, _root_._a66427b, _root_.«_>Int_»,
            _root_.«_-Int_», valSeqAtModel, hInner, guard] <;> rfl
      · have hPositive : 0 < index := by omega
        have hRestBound : index - 1 < valSeqLengthModel rest := by
          change index < 1 + valSeqLengthModel rest at hBound
          omega
        have hPredNonnegative : 0 ≤ index - 1 := by omega
        have hRec := generated_valSeqAt_valid rest (index - 1)
          hPredNonnegative hRestBound
        simpa [_root_.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»,
          _root_._86fc1c7, _root_._a66427b, _root_.«_>Int_»,
          _root_.«_-Int_», valSeqAtModel, hZero, hPositive,
          guard] using hRec
termination_by values

theorem generated_applyIndex_list
    (values : SortValSeq) (index : SortInt)
    (hNonnegative : 0 ≤ index) (hBound : index < valSeqLengthModel values) :
    _root_.«applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int»
      (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) index =
      some (valSeqAtModel values index) := by
  change Int at index
  change (0 : Int) ≤ index at hNonnegative
  change index < (valSeqLengthModel values : Int) at hBound
  have hNotNegative : ¬ index < 0 := by omega
  have hRetr : (@retr SortIterable SortVal)
      (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) =
      some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) := by
    rfl
  simpa [_root_.«applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int»,
    _root_._77afc7e, _root_._ae682a5, _root_._dff41b0,
    _root_.«normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int»,
    _root_._6e2ceae, _root_._92d2fec, _root_.«_<Int_»,
    _root_.«_>=Int_», _root_.«_+Int_»,
    hNonnegative, hNotNegative, hRetr, generated_vsLen, guard] using
      (generated_valSeqAt_valid values index hNonnegative hBound)

theorem eval_indexed_arr
    (values : SortValSeq) (changes current : SortInt)
    (indexExpression : SortExpr) (index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hNonnegative : 0 ≤ index) (hBound : index < valSeqLengthModel values)
    (hIndexPending : isKResult
      (SortK.kseq ((@inj SortExpr SortKItem) indexExpression) SortK.dotk) =
        some false)
    (hIndex :
      Rewrites
        { k := { val := (SortK.kseq
            ((@inj SortExpr SortKItem) indexExpression) (SortK.kseq
              (SortKItem.«#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index1_»
                (SortK.kseq (SortKItem.inj_SortIterable
                  (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
                  SortK.dotk)) tail)) },
          env := { val := 1 }, scopes := { val := activeScopes values changes current },
          scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
          ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
        { k := { val := (SortK.kseq
            (SortKItem.inj_SortInt index) (SortK.kseq
              (SortKItem.«#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index1_»
                (SortK.kseq (SortKItem.inj_SortIterable
                  (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
                  SortK.dotk)) tail)) },
          env := { val := 1 }, scopes := { val := activeScopes values changes current },
          scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
          ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem)
          (indexedArrExpr indexExpression)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes current },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq ((@inj SortVal SortKItem)
          (valSeqAtModel values index)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes current },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let objectFreezer :=
    SortKItem.«#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index0_»
      (SortK.kseq ((@inj SortIndex SortKItem)
        ((@inj SortExpr SortIndex) indexExpression)) SortK.dotk)
  apply Rewrites.tran (Rewrites._c5775b3 rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_name_arr values changes current (SortK.kseq objectFreezer tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · simpa [objectFreezer] using
      (Rewrites._5860404
        (HOLE := ((@inj SortVal SortExpr)
          (SortVal.inj_SortIterable
            (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))))
        (_Gen0 := ((@inj SortExpr SortIndex) indexExpression)) rfl rfl rfl)
  · apply Rewrites.tran
      (Rewrites._06d3a17
        (HOLE := indexExpression)
        (_Gen0 := SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        (_Val0 := false) (_Val1 := true) (_Val2 := true)
        hIndexPending rfl rfl rfl)
    apply Rewrites.tran hIndex
    apply Rewrites.tran
    · exact Rewrites._6105b33
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt index)))
        (_Gen0 := SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        rfl rfl rfl
    · exact Rewrites._f3fd256
        (generated_applyIndex_list values index hNonnegative hBound)

theorem generated_applyBin_sub (left right : SortInt) :
    _root_.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-"
      (SortVal.inj_SortInt left) (SortVal.inj_SortInt right) =
      some (SortVal.inj_SortInt (left - right)) := by
  rfl

theorem eval_len_minus_i
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem)
          (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-"
            lenArrExpr (nameExpr "i"))) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt
          (valSeqLengthModel values - index)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let leftFreezer :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_»
      (SortK.kseq (SortKItem.inj_SortString "-") SortK.dotk)
      (SortK.kseq ((@inj SortExpr SortKItem) (nameExpr "i")) SortK.dotk)
  let n := valSeqLengthModel values
  let rightFreezer :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_»
      (SortK.kseq (SortKItem.inj_SortString "-") SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortInt n) SortK.dotk)
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_len_arr values changes index (SortK.kseq leftFreezer tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · simpa [leftFreezer, n] using
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt n)))
        (K0 := "-") (K2 := nameExpr "i") rfl rfl rfl)
  · apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
        rfl rfl rfl rfl rfl rfl)
    apply Rewrites.tran
      (eval_name_i values changes index (SortK.kseq rightFreezer tail)
        scopeLoc heap heapLoc stack ret exc exitCode counter)
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt index)))
        (K1 := ((@inj SortVal SortExpr) (SortVal.inj_SortInt n)))
        (K0 := "-") rfl rfl rfl)
    exact Rewrites._d9b5bba (generated_applyBin_sub n index)

theorem eval_mirror_index
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) mirrorIndexExpr) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt
          (valSeqLengthModel values - index - 1)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let leftExpr := SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-"
    lenArrExpr (nameExpr "i")
  let leftValue := valSeqLengthModel values - index
  let leftFreezer :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_»
      (SortK.kseq (SortKItem.inj_SortString "-") SortK.dotk)
      (SortK.kseq ((@inj SortExpr SortKItem) (intExpr 1)) SortK.dotk)
  let rightFreezer :=
    SortKItem.«#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_»
      (SortK.kseq (SortKItem.inj_SortString "-") SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortInt leftValue) SortK.dotk)
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_len_minus_i values changes index (SortK.kseq leftFreezer tail)
      scopeLoc heap heapLoc stack ret exc exitCode counter)
  apply Rewrites.tran
  · simpa [leftExpr, leftValue, leftFreezer] using
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt leftValue)))
        (K0 := "-") (K2 := intExpr 1) rfl rfl rfl)
  · apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
        rfl rfl rfl rfl rfl rfl)
    apply Rewrites.tran Rewrites._665cd53
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt 1)))
        (K1 := ((@inj SortVal SortExpr) (SortVal.inj_SortInt leftValue)))
        (K0 := "-") rfl rfl rfl)
    simpa [leftValue] using
      (Rewrites._d9b5bba (generated_applyBin_sub leftValue 1))

def valSeqNatLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + valSeqNatLength rest

theorem valSeqLength_eq_natCast (values : SortValSeq) :
    valSeqLengthModel values = (valSeqNatLength values : Int) := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» => rfl
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      simp [valSeqLengthModel, valSeqNatLength, valSeqLength_eq_natCast rest]
termination_by values

theorem halfLen_eq_natDiv (values : SortValSeq) :
    «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values =
      ((valSeqNatLength values / 2 : Nat) : Int) := by
  let n := valSeqNatLength values
  rw [«halfLen(_)_VERIFICATION-BASE_Int_ValSeq»,
    valSeqLength_eq_natCast values]
  change Int.tdiv ((n : Int) - Int.tmod (Int.tmod (n : Int) 2 + 2) 2) 2 =
    (n / 2 : Nat)
  have hn : 0 ≤ (n : Int) := Int.ofNat_zero_le n
  rw [Int.tmod_eq_emod_of_nonneg hn]
  have hr : 0 ≤ (n : Int) % 2 + 2 := by
    have := Int.emod_nonneg (n : Int) (by decide : (2 : Int) ≠ 0)
    omega
  rw [Int.tmod_eq_emod_of_nonneg hr]
  simp only [Int.add_emod, Int.emod_self, Int.add_zero, Int.emod_emod]
  have hmod : n % 2 ≤ n := Nat.mod_le n 2
  change ((n : Int) - ((n % 2 : Nat) : Int)).tdiv 2 = (n / 2 : Nat)
  rw [← Int.ofNat_sub hmod]
  rw [Int.natCast_tdiv_eq_ediv]
  change (((n - n % 2) / 2 : Nat) : Int) = ((n / 2 : Nat) : Int)
  exact congrArg Int.ofNat (Nat.div_eq_sub_mod_div (m := n) (n := 2)).symm

theorem loop_index_bounds
    (values : SortValSeq) (index : SortInt)
    (hNonnegative : 0 ≤ index)
    (hLoop : index < «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values) :
    index < valSeqLengthModel values ∧
      0 ≤ valSeqLengthModel values - index - 1 ∧
      valSeqLengthModel values - index - 1 < valSeqLengthModel values := by
  change Int at index
  change (0 : Int) ≤ index at hNonnegative
  change index <
    («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values : Int) at hLoop
  rw [halfLen_eq_natDiv values] at hLoop
  change index < (((valSeqNatLength values / 2 : Nat) : Int)) at hLoop
  rw [valSeqLength_eq_natCast values]
  have hDivLe : valSeqNatLength values / 2 ≤ valSeqNatLength values :=
    Nat.div_le_self _ _
  have hDivLeInt :
      ((valSeqNatLength values / 2 : Nat) : Int) ≤
        (valSeqNatLength values : Int) := Int.ofNat_le.mpr hDivLe
  constructor
  · change index < (valSeqNatLength values : Int)
    omega
  constructor
  · change (0 : Int) ≤ (valSeqNatLength values : Int) - index - 1
    omega
  · change (valSeqNatLength values : Int) - index - 1 <
      (valSeqNatLength values : Int)
    omega

theorem generated_isKResult_valExpr (value : SortVal) :
    isKResult (SortK.kseq ((@inj SortExpr SortKItem)
      ((@inj SortVal SortExpr) value)) SortK.dotk) =
      some true := by
  cases value <;> rfl

@[simp] theorem generated_inj_val_expr_eq (value : SortVal) :
    ((@inj SortExpr SortKItem) ((@inj SortVal SortExpr) value)) =
      ((@inj SortVal SortKItem) value) := by
  cases value <;> rfl

theorem eval_pair_condition
    (values : SortValSeq) (changes index : SortInt) (result : SortBool)
    (tail : SortK) (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hNonnegative : 0 ≤ index)
    (hLoop : index < «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)
    (hCompare : applyCmpModel "!=" (valSeqAtModel values index)
      (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortExpr SortKItem) pairCondExpr) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortBool result) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  obtain ⟨hIndexBound, hMirrorNonnegative, hMirrorBound⟩ :=
    loop_index_bounds values index hNonnegative hLoop
  let mirror := valSeqLengthModel values - index - 1
  let cmp := SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "!="
    (indexedArrExpr mirrorIndexExpr)
  let leftFreezer :=
    SortKItem.«#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_»
      (SortK.kseq ((@inj SortCmpOp SortKItem) cmp) SortK.dotk)
  let firstIndexFreezer :=
    SortKItem.«#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index1_»
      (SortK.kseq (SortKItem.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) SortK.dotk)
  let rightFreezer :=
    SortKItem.«#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp2_»
      (SortK.kseq ((@inj SortVal SortKItem) (valSeqAtModel values index)) SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortString "!=") SortK.dotk)
  let mirrorIndexFreezer :=
    SortKItem.«#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index1_»
      (SortK.kseq (SortKItem.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) SortK.dotk)
  apply Rewrites.tran (Rewrites._1f0e78f rfl rfl rfl rfl)
  apply Rewrites.tran
  · apply eval_indexed_arr values changes index (nameExpr "i") index
      (SortK.kseq leftFreezer tail) scopeLoc heap heapLoc stack ret exc exitCode
      counter hNonnegative hIndexBound rfl
    simpa [firstIndexFreezer] using
      (eval_name_i values changes index
        (SortK.kseq firstIndexFreezer (SortK.kseq leftFreezer tail))
        scopeLoc heap heapLoc stack ret exc exitCode counter)
  · apply Rewrites.tran
    · simpa [cmp, leftFreezer] using
        (Rewrites._dfb9e43
          (HOLE := ((@inj SortVal SortExpr) (valSeqAtModel values index)))
          (_Gen0 := cmp) (_Val0 := true) (_Val1 := true)
          (generated_isKResult_valExpr (valSeqAtModel values index)) rfl rfl)
    · apply Rewrites.tran
        (Rewrites._e1122bd
          (HOLE := indexedArrExpr mirrorIndexExpr)
          (_Gen0 := valSeqAtModel values index) (_Gen1 := "!=")
          (_Val0 := false) (_Val1 := true) (_Val2 := true)
          rfl rfl rfl rfl)
      apply Rewrites.tran
      · apply eval_indexed_arr values changes index mirrorIndexExpr mirror
          (SortK.kseq rightFreezer tail) scopeLoc heap heapLoc stack ret exc
          exitCode counter hMirrorNonnegative hMirrorBound rfl
        simpa [mirror, mirrorIndexFreezer] using
          (eval_mirror_index values changes index
            (SortK.kseq mirrorIndexFreezer (SortK.kseq rightFreezer tail))
            scopeLoc heap heapLoc stack ret exc exitCode counter)
      · apply Rewrites.tran
        · simpa [mirror, rightFreezer] using
            (Rewrites._aae3b52
              (HOLE := ((@inj SortVal SortExpr)
                (valSeqAtModel values mirror)))
              (_Gen0 := valSeqAtModel values index) (_Gen1 := "!=")
              (_Val0 := true) (_Val1 := true)
              (generated_isKResult_valExpr (valSeqAtModel values mirror))
              rfl rfl)
        · exact Rewrites._a00964a hCompare
theorem allInts_valSeqAtModel_int
    (values : SortValSeq) (index : SortInt)
    (hAll : «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» values = true) :
    ∃ value : SortInt,
      valSeqAtModel values index = SortVal.inj_SortInt value := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      exact ⟨0, rfl⟩
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      cases value <;>
        simp [«allInts(_)_VERIFICATION-BASE_Bool_ValSeq»] at hAll
      case inj_SortInt value =>
        by_cases hZero : index = 0
        · exact ⟨value, by simp [valSeqAtModel, hZero]⟩
        · by_cases hPositive : 0 < index
          · obtain ⟨result, hResult⟩ :=
              allInts_valSeqAtModel_int rest (index - 1) hAll
            exact ⟨result, by simp [valSeqAtModel, hZero, hPositive, hResult]⟩
          · exact ⟨0, by simp [valSeqAtModel, hZero, hPositive]⟩
termination_by values

theorem applyCmpModel_int_ne_isSome (left right : SortInt) :
    (applyCmpModel "!=" (SortVal.inj_SortInt left)
      (SortVal.inj_SortInt right)).isSome = true := by
  cases hEq : left == right <;>
    simp [applyCmpModel,
      _root_.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      _root_._c986c4d, _root_.«_=/=Int_», _root_._4de6e05,
      _root_.«_==Int_», _root_.notBool_, _root_._17ebc68,
      _root_._53fc758, hEq]

def arrBindingSingleton (values : SortValSeq) : SortMap :=
  ⟨[(SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
    (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))]⟩

def changesBindingSingleton (changes : SortInt) : SortMap :=
  ⟨[(SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes)]⟩

def indexBindingSingleton (index : SortInt) : SortMap :=
  ⟨[(SortKItem.inj_SortString "i", SortKItem.inj_SortInt index)]⟩

def arrChangesBindings (values : SortValSeq) (changes : SortInt) : SortMap :=
  ⟨[
    (SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)),
    (SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes)
  ]⟩

theorem generated_merge_arr_changes (values : SortValSeq) (changes : SortInt) :
    _root_._Map_ (arrBindingSingleton values)
      (changesBindingSingleton changes) =
      some (arrChangesBindings values changes) := by
  simp [_root_._Map_, arrBindingSingleton, changesBindingSingleton,
    arrChangesBindings]
  constructor
  · change
      (if
        (if SortKItem.inj_SortString "arr" =
            SortKItem.inj_SortString "changes" then true else false) = true
       then false else true) = true
    simp
  · change
      (if decide ("changes" < "arr") = true then
        [(SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes),
         (SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))]
       else
        [(SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)),
         (SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes)]) =
       [(SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)),
        (SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes)]
    simp

theorem generated_merge_arrChanges_i
    (values : SortValSeq) (changes index : SortInt) :
    _root_._Map_ (arrChangesBindings values changes)
      (indexBindingSingleton index) =
      some (localBindings values changes index) := by
  simp [_root_._Map_, arrChangesBindings, indexBindingSingleton,
    localBindings]
  constructor
  · change
      (if
        (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "i"
          then true
         else if SortKItem.inj_SortString "changes" =
            SortKItem.inj_SortString "i" then true else false) = true
       then false else true) = true
    simp
  · change
      (if decide ("changes" < "arr") = true then [] else
        (SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) ::
        ((if decide ("i" < "changes") = true then [] else
          [(SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes),
           (SortKItem.inj_SortString "i", SortKItem.inj_SortInt index)]))) =
       [(SortKItem.inj_SortString "arr", SortKItem.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)),
        (SortKItem.inj_SortString "changes", SortKItem.inj_SortInt changes),
        (SortKItem.inj_SortString "i", SortKItem.inj_SortInt index)]
    simp

def boolIncrement (condition : SortBool) : SortInt :=
  if condition then 1 else 0

theorem generated_kite_increment (condition : SortBool) :
    _root_.kite condition 1 0 = some (boolIncrement condition) := by
  cases condition <;> rfl

theorem execute_branch
    (values : SortValSeq) (changes index : SortInt) (condition : SortBool)
    (tail : SortK) (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := (SortK.kseq
          (SortKItem.«#branch(_,_,_)_MPY-CONTROLS_KItem_Bool_Stmts_Stmts»
            condition (oneStmt incrementChangesStmt) emptyStmts) tail) },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := tail }, env := { val := 1 },
        scopes := { val := (activeScopes values
          (changes + boolIncrement condition) index) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  refine Rewrites._c06c8fe
    (B := condition) (C := changes) (I := index)
    (REST := outerScopes)
    (_Val0 := arrBindingSingleton values)
    (_Val1 := changesBindingSingleton changes)
    (_Val2 := arrChangesBindings values changes)
    (_Val3 := indexBindingSingleton index)
    (_Val4 := localBindings values changes index)
    (_Val5 := localScopeSingleton values changes index)
    (_Val6 := activeScopes values changes index)
    (_Val7 := arrBindingSingleton values)
    (_Val8 := boolIncrement condition)
    (_Val9 := changes + boolIncrement condition)
    (_Val10 := changesBindingSingleton (changes + boolIncrement condition))
    (_Val11 := arrChangesBindings values (changes + boolIncrement condition))
    (_Val12 := indexBindingSingleton index)
    (_Val13 := localBindings values (changes + boolIncrement condition) index)
    (_Val14 := localScopeSingleton values (changes + boolIncrement condition) index)
    (_Val15 := activeScopes values (changes + boolIncrement condition) index)
    (by rfl) (by rfl) (generated_merge_arr_changes values changes)
    (by rfl) (generated_merge_arrChanges_i values changes index)
    (by rfl) (generated_merge_local_outer values changes index)
    (by rfl) (generated_kite_increment condition) (by rfl)
    (by rfl) (generated_merge_arr_changes values
      (changes + boolIncrement condition))
    (by rfl) (generated_merge_arrChanges_i values
      (changes + boolIncrement condition) index)
    (by rfl) (generated_merge_local_outer values
      (changes + boolIncrement condition) index)

theorem generated_contains_i
    (values : SortValSeq) (changes index : SortInt) :
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
      (SortKItem.inj_SortString "i") (localBindings values changes index) =
      some true := by
  simp only [_root_.«_in_keys(_)_MAP_Bool_KItem_Map», localBindings,
    Option.some.injEq]
  change
    (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "i" then true
     else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "i"
       then true
     else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "i"
       then true else false) = true
  simp

theorem generated_lookup_i
    (values : SortValSeq) (changes index : SortInt) :
    _root_.«Map:lookup» (localBindings values changes index)
      (SortKItem.inj_SortString "i") = some (SortKItem.inj_SortInt index) := by
  simp only [_root_.«Map:lookup», localBindings]
  change
    (if SortKItem.inj_SortString "arr" = SortKItem.inj_SortString "i" then _
     else if SortKItem.inj_SortString "changes" = SortKItem.inj_SortString "i"
       then _
     else if SortKItem.inj_SortString "i" = SortKItem.inj_SortString "i"
       then some (SortKItem.inj_SortInt index) else none) = _
  simp

set_option maxHeartbeats 1000000 in
theorem generated_update_i
    (values : SortValSeq) (changes index : SortInt) :
    _root_.«Map:update» (localBindings values changes index)
      (SortKItem.inj_SortString "i") (SortKItem.inj_SortInt (index + 1)) =
      some (localBindings values changes (index + 1)) := by
  unfold _root_.«Map:update»
  deltaPrivateMapModels
  deltaPrivateMapModels
  simp [localBindings]
  deltaPrivateKeyOrderModel
  have hArrNe :
      SortKItem.inj_SortString "arr" ≠ SortKItem.inj_SortString "i" := by
    simp
  have hChangesNe :
      SortKItem.inj_SortString "changes" ≠ SortKItem.inj_SortString "i" := by
    simp
  have hArrLt : decide ("arr" < "i") = true := by rfl
  have hChangesLt : decide ("changes" < "i") = true := by rfl
  rw [if_neg hArrNe, if_neg hChangesNe, if_pos rfl]
  simp only [List.rec]
  rw [hArrLt, hChangesLt]
  simp only [if_pos True.intro]

theorem generated_applyBin_add (left right : SortInt) :
    _root_.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
      (SortVal.inj_SortInt left) (SortVal.inj_SortInt right) =
      some (SortVal.inj_SortInt (left + right)) := by
  rfl

theorem execute_increment_index
    (values : SortValSeq) (changes index : SortInt) (tail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortStmt SortKItem) incrementIndexStmt) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := tail }, env := { val := 1 },
        scopes := { val := activeScopes values changes (index + 1) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran Rewrites._665cd53
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_cool»
      (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt 1)))
      (K0 := nameExpr "i") (K1 := "+") rfl rfl rfl)
  refine Rewrites._460aaab
    (L := 1) (M := localBindings values changes index)
    (_DotVar2 := outerScopes) (OP := "+") (X := "i")
    (V := SortVal.inj_SortInt 1)
    (_Val0 := true)
    (_Val1 := localScopeSingleton values changes index)
    (_Val2 := activeScopes values changes index)
    (_Val3 := SortKItem.inj_SortInt index)
    (_Val4 := SortVal.inj_SortInt index)
    (_Val5 := SortVal.inj_SortInt (index + 1))
    (_Val6 := localBindings values changes (index + 1))
    (_Val7 := localScopeSingleton values changes (index + 1))
    (_Val8 := activeScopes values changes (index + 1))
    (_Gen0 := SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)
    (generated_contains_i values changes index) (by rfl)
    (generated_merge_local_outer values changes index)
    (generated_lookup_i values changes index) (by rfl)
    (generated_applyBin_add index 1)
    (generated_update_i values changes index) (by rfl)
    (generated_merge_local_outer values changes (index + 1)) rfl

theorem pair_comparison_exists
    (values : SortValSeq) (index : SortInt)
    (hAll : «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» values = true) :
    ∃ result : SortBool,
      applyCmpModel "!=" (valSeqAtModel values index)
        (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result := by
  obtain ⟨left, hLeft⟩ := allInts_valSeqAtModel_int values index hAll
  obtain ⟨right, hRight⟩ := allInts_valSeqAtModel_int values
    (valSeqLengthModel values - index - 1) hAll
  have hSome := applyCmpModel_int_ne_isSome left right
  rw [hLeft, hRight]
  cases hCompare : applyCmpModel "!=" (SortVal.inj_SortInt left)
      (SortVal.inj_SortInt right) with
  | none => simp [hCompare] at hSome
  | some result => exact ⟨result, rfl⟩

theorem pairDiff_eq_boolIncrement
    (values : SortValSeq) (index : SortInt) (result : SortBool)
    (hCompare : applyCmpModel "!=" (valSeqAtModel values index)
      (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result) :
    pairDiffModel values index = boolIncrement result := by
  cases result <;> simp [pairDiffModel, boolIncrement, hCompare]

theorem mismatchCount_step
    (values : SortValSeq) (index stop : SortInt) (result : SortBool)
    (hLoop : index < stop)
    (hCompare : applyCmpModel "!=" (valSeqAtModel values index)
      (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result) :
    «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»
        values index stop =
      boolIncrement result +
        «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»
          values (index + 1) stop := by
  change Int at index stop
  have hPositive : 0 < stop - index := Int.sub_pos.mpr hLoop
  have hNotStart : ¬ index ≥ stop := Int.not_le_of_gt hLoop
  have hNextDifference : stop - (index + 1) = stop - index - 1 := by omega
  have hNextNonnegative : 0 ≤ stop - index - 1 := by omega
  have hFuel : (stop - index).toNat =
      Nat.succ (stop - (index + 1)).toNat := by
    have hSplit : stop - index = (stop - index - 1) + 1 := by omega
    calc
      (stop - index).toNat = ((stop - index - 1) + 1).toNat :=
        congrArg Int.toNat hSplit
      _ = (stop - index - 1).toNat + 1 :=
        Int.toNat_add_nat hNextNonnegative 1
      _ = Nat.succ (stop - (index + 1)).toNat := by
        rw [hNextDifference]
  rw [«mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»]
  simp only [if_neg hNotStart, hFuel,
    mismatchCountFuelModel]
  rw [pairDiff_eq_boolIncrement values index result hCompare]
  by_cases hLast : index + 1 ≥ stop
  · have hEq : index + 1 = stop := by omega
    simp [«mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»,
      hLast, hEq, mismatchCountFuelModel]
  · simp [«mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int», hLast]

theorem remaining_toNat_succ (index stop : SortInt) (hLoop : index < stop) :
    (stop - index).toNat = Nat.succ (stop - (index + 1)).toNat := by
  change Int at index stop
  have hPositive : 0 < stop - index := Int.sub_pos.mpr hLoop
  have hNextDifference : stop - (index + 1) = stop - index - 1 := by omega
  have hNextNonnegative : 0 ≤ stop - index - 1 := by omega
  have hSplit : stop - index = (stop - index - 1) + 1 := by omega
  calc
    (stop - index).toNat = ((stop - index - 1) + 1).toNat :=
      congrArg Int.toNat hSplit
    _ = (stop - index - 1).toNat + 1 :=
      Int.toNat_add_nat hNextNonnegative 1
    _ = Nat.succ (stop - (index + 1)).toNat := by rw [hNextDifference]

theorem generated_truthy_bool (condition : SortBool) :
    _root_.«truthy(_)_MPY-CORE_Bool_Val»
      (SortVal.inj_SortBool condition) = some condition := by
  cases condition <;> rfl

theorem execute_pair_if
    (values : SortValSeq) (changes index : SortInt) (result : SortBool)
    (tail : SortK) (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hNonnegative : 0 ≤ index)
    (hLoop : index < «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)
    (hCompare : applyCmpModel "!=" (valSeqAtModel values index)
      (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result) :
    Rewrites
      { k := { val := SortK.kseq ((@inj SortStmt SortKItem)
          (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» pairCondExpr
            (oneStmt incrementChangesStmt) emptyStmts)) tail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := tail }, env := { val := 1 },
        scopes := { val := (activeScopes values
          (changes + boolIncrement result) index) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let freezer :=
    SortKItem.«#freezerIf(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts0_»
      (SortK.kseq ((@inj SortStmts SortKItem)
        (oneStmt incrementChangesStmt)) SortK.dotk)
      (SortK.kseq ((@inj SortStmts SortKItem) emptyStmts) SortK.dotk)
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_pair_condition values changes index result
      (SortK.kseq freezer tail) scopeLoc heap heapLoc stack ret exc exitCode
      counter hNonnegative hLoop hCompare)
  apply Rewrites.tran
  · simpa [freezer] using
      (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortBool result)))
        (K1 := oneStmt incrementChangesStmt) (K2 := emptyStmts)
        (generated_isKResult_valExpr (SortVal.inj_SortBool result)) rfl rfl)
  apply Rewrites.tran
  · simpa using
      (Rewrites._c82b7aa
        (C := SortVal.inj_SortBool result)
        (T := oneStmt incrementChangesStmt) (E := emptyStmts)
        (generated_truthy_bool result))
  exact execute_branch values changes index result tail scopeLoc heap heapLoc
    stack ret exc exitCode counter

def whileControlItem : SortKItem :=
  SortKItem.«#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts»
    loopCondExpr loopBodyStmts

def whileControl (tail : SortK) : SortK := SortK.kseq whileControlItem tail

def loopLabelControl (tail : SortK) : SortK :=
  SortK.kseq (SortKItem.«#loopLbl(_)_MPY-CONTROLS_KItem_K»
    (SortK.kseq whileControlItem SortK.dotk)) tail

def loopBodyControl (tail : SortK) : SortK :=
  SortK.kseq (SortKItem.inj_SortStmts loopBodyStmts)
    (loopLabelControl tail)

theorem execute_loop_body
    (values : SortValSeq) (changes index : SortInt) (result : SortBool)
    (loopTail : SortK) (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hNonnegative : 0 ≤ index)
    (hLoop : index < «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)
    (hCompare : applyCmpModel "!=" (valSeqAtModel values index)
      (valSeqAtModel values (valSeqLengthModel values - index - 1)) =
        some result) :
    Rewrites
      { k := { val := loopBodyControl loopTail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := whileControl loopTail },
        env := { val := 1 }, scopes := { val := (activeScopes values
          (changes + boolIncrement result) (index + 1)) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let afterIf := SortK.kseq ((@inj SortStmts SortKItem)
      (oneStmt incrementIndexStmt))
    (SortK.kseq (SortKItem.«#loopLbl(_)_MPY-CONTROLS_KItem_K»
      (SortK.kseq (SortKItem.«#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts»
        loopCondExpr loopBodyStmts) SortK.dotk)) loopTail)
  apply Rewrites.tran Rewrites._94bd14e
  apply Rewrites.tran
  · simpa [loopBodyStmts, afterIf] using
      (execute_pair_if values changes index result afterIf scopeLoc heap
        heapLoc stack ret exc exitCode counter hNonnegative hLoop hCompare)
  apply Rewrites.tran Rewrites._94bd14e
  apply Rewrites.tran
  · apply execute_increment_index values (changes + boolIncrement result) index
      (SortK.kseq ((@inj SortStmts SortKItem) emptyStmts)
        (SortK.kseq (SortKItem.«#loopLbl(_)_MPY-CONTROLS_KItem_K»
          (SortK.kseq (SortKItem.«#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts»
            loopCondExpr loopBodyStmts) SortK.dotk)) loopTail))
      scopeLoc heap heapLoc stack ret exc exitCode counter
  apply Rewrites.tran Rewrites._2a0ddee
  exact Rewrites._d499ad9 (by rfl)

theorem execute_loop
    (values : SortValSeq) (changes index : SortInt) (loopTail : SortK)
    (scopeLoc : SortScopeLocCell) (heap : SortHeapCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell)
    (hAll : «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» values = true)
    (hNonnegative : 0 ≤ index)
    (hAtMost : index ≤ «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values) :
    Rewrites
      { k := { val := whileControl loopTail },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := loopTail }, env := { val := 1 },
        scopes := { val := (activeScopes values
          (changes + «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»
            values index («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))
          («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)) },
        scopeLoc := scopeLoc, heap := heap, heapLoc := heapLoc, stack := stack,
        ret := ret, exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let stop := «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values
  let conditionTail := SortK.kseq
    (SortKItem.«#whileCond(_,_)_MPY-CONTROLS_KItem_Expr_Stmts»
      loopCondExpr loopBodyStmts) loopTail
  apply Rewrites.tran
  · simpa [whileControl, whileControlItem] using
      (Rewrites._0edcaa2 (C := loopCondExpr) (B := loopBodyStmts))
  apply Rewrites.tran
    (eval_loop_condition values changes index conditionTail scopeLoc heap
      heapLoc stack ret exc exitCode counter)
  by_cases hLoop : index < stop
  · change (index : Int) < (stop : Int) at hLoop
    have hNonnegativeInt : (0 : Int) ≤ (index : Int) := by
      exact hNonnegative
    have hAtMostStop : (index : Int) ≤ (stop : Int) := by
      simpa [stop] using hAtMost
    apply Rewrites.tran
    · simpa [stop, conditionTail, loopBodyControl, loopLabelControl,
          whileControl, whileControlItem, hLoop] using
        (Rewrites._0d9d338
          (C := loopCondExpr) (B := loopBodyStmts)
          (V := SortVal.inj_SortBool true)
          (generated_truthy_bool true) rfl)
    obtain ⟨result, hCompare⟩ := pair_comparison_exists values index hAll
    apply Rewrites.tran
      (execute_loop_body values changes index result loopTail scopeLoc heap
        heapLoc stack ret exc exitCode counter hNonnegative
        (by simpa [stop] using hLoop) hCompare)
    have hNextNonnegative : (0 : Int) ≤ (index : Int) + 1 :=
      Int.add_nonneg hNonnegativeInt (by decide)
    have hNextAtMost : (index : Int) + 1 ≤ (stop : Int) :=
      Int.lt_iff_add_one_le.mp hLoop
    have hStep := mismatchCount_step values index stop result hLoop hCompare
    have hRecursive := execute_loop values
      (changes + boolIncrement result) (index + 1) loopTail scopeLoc heap
      heapLoc stack ret exc exitCode counter hAll hNextNonnegative
      (by simpa [stop] using hNextAtMost)
    simpa [stop, hStep, Int.add_assoc] using hRecursive
  · change ¬(index : Int) < (stop : Int) at hLoop
    have hAtMostStop : (index : Int) ≤ (stop : Int) := by
      simpa [stop] using hAtMost
    have hEq : index = stop :=
      Int.le_antisymm hAtMostStop (Int.le_of_not_gt hLoop)
    simpa [stop, conditionTail, hLoop, hEq,
        «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»] using
      (Rewrites._b13ae76
        (V := SortVal.inj_SortBool false)
        (_C := loopCondExpr) (_B := loopBodyStmts)
        (generated_truthy_bool false) rfl rfl)
termination_by
  («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values - index).toNat
decreasing_by
  have hRemain := remaining_toNat_succ index
    («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values) (by simpa [stop] using hLoop)
  omega

theorem generated_delete_local
    (values : SortValSeq) (changes index : SortInt) :
    _root_.«_[_<-undef]» (activeScopes values changes index)
      (SortKItem.inj_SortInt 1) = some outerScopes := by
  unfold _root_.«_[_<-undef]»
  deltaPrivateMapModels
  simp [activeScopes, outerScopes, outerMinusEntry, outerZeroEntry,
    localScopeEntry]

def callFrame : SortKItem :=
  SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int» SortK.dotk 0 1

def callStack : SortList := ⟨[callFrame]⟩

theorem generated_root_listItem_frame :
    _root_.ListItem callFrame = some callStack := by rfl

theorem generated_root_list_merge_frame :
    _root_._List_ callStack ⟨[]⟩ = some callStack := by rfl

def returnControl : SortK :=
  SortK.kseq (SortKItem.inj_SortStmts returnStmts)
    (SortK.kseq SortKItem.«#endcall_MPY-FUNCTIONS_KItem» SortK.dotk)

theorem execute_return
    (values : SortValSeq) (changes index : SortInt)
    (heap : SortHeapCell) (heapLoc : SortHeapLocCell)
    (exc : SortExcCell) (exitCode : SortExitCodeCell)
    (counter : SortGeneratedCounterCell) :
    Rewrites
      { k := { val := returnControl },
        env := { val := 1 }, scopes := { val := activeScopes values changes index },
        scopeLoc := { val := 2 }, heap := heap, heapLoc := heapLoc,
        stack := { val := callStack },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := exc, exitCode := exitCode, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt changes) SortK.dotk },
        env := { val := 0 }, scopes := { val := outerScopes },
        scopeLoc := { val := 1 }, heap := heap, heapLoc := heapLoc,
        stack := { val := ⟨[]⟩ },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := exc, exitCode := exitCode, generatedCounter := counter } := by
  let afterReturn := SortK.kseq (SortKItem.inj_SortStmts emptyStmts)
    (SortK.kseq SortKItem.«#endcall_MPY-FUNCTIONS_KItem» SortK.dotk)
  apply Rewrites.tran Rewrites._94bd14e
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_heat»
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (eval_name_changes values changes index
      (SortK.kseq SortKItem.«#freezerReturn(_)_MPY-SYNTAX_Stmt_Expr0_»
        afterReturn)
      { val := 2 } heap heapLoc { val := callStack }
      { val := SortRetState.«noRet_MPY-CORE_RetState» }
      exc exitCode counter)
  apply Rewrites.tran
  · simpa using
      (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool»
        (HOLE := ((@inj SortVal SortExpr) (SortVal.inj_SortInt changes)))
        (generated_isKResult_valExpr (SortVal.inj_SortInt changes)) rfl rfl)
  apply Rewrites.tran (Rewrites._b817d8b (V := SortVal.inj_SortInt changes))
  exact Rewrites._9533001
    (CALLERL := 0) (L := 1) (SAVEDL := 1) (CONT := SortK.dotk)
    (SC := activeScopes values changes index) (V := SortVal.inj_SortInt changes)
    (_DotVar1 := ⟨[]⟩) (_Val0 := callStack) (_Val1 := callStack)
    (_Val2 := outerScopes) (generated_root_listItem_frame)
    (generated_root_list_merge_frame)
    (generated_delete_local values changes index)

theorem halfLen_nonnegative (values : SortValSeq) :
    0 ≤ «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values := by
  rw [halfLen_eq_natDiv values]
  exact Int.ofNat_zero_le _

theorem execute_canonical
    (values : SortValSeq) (counter : SortGeneratedCounterCell)
    (hAll : «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» values = true) :
    Rewrites
      { k := { val := whileControl returnControl },
        env := { val := 1 }, scopes := { val := activeScopes values 0 0 },
        scopeLoc := { val := 2 }, heap := { val := «.Map» },
        heapLoc := { val := 0 }, stack := { val := callStack },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
        exitCode := { val := 0 }, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt
          («mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int» values 0
            («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))) SortK.dotk },
        env := { val := 0 }, scopes := { val := outerScopes },
        scopeLoc := { val := 1 }, heap := { val := «.Map» },
        heapLoc := { val := 0 }, stack := { val := «.List» },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
        exitCode := { val := 0 }, generatedCounter := counter } := by
  let answer := «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int»
    values 0 («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)
  apply Rewrites.tran
    (execute_loop values 0 0 returnControl { val := 2 } { val := «.Map» }
      { val := 0 } { val := callStack }
      { val := SortRetState.«noRet_MPY-CORE_RetState» }
      { val := SortExc.«NoExc_MPY-CORE_Exc» } { val := 0 } counter hAll
      (by decide) (halfLen_nonnegative values))
  simpa [answer] using
    (execute_return values answer
      («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values)
      { val := «.Map» } { val := 0 }
      { val := SortExc.«NoExc_MPY-CORE_Exc» } { val := 0 } counter)

def builtinSourceEntries : List (SortString × SortVal) := [
  ("len", SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
  ("set", SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
  ("sum", SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
  ("abs", SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
  ("min", SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
  ("max", SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
  ("ord", SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
  ("chr", SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
  ("range", SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
  ("all", SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
  ("any", SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
  ("zip", SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip"),
  ("isinstance", SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
  ("sorted", SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
  ("list", SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
  ("round", SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
  ("bin", SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
  ("enumerate", SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
  ("map", SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
  ("eval", SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"),
  ("int", SortVal.«typeV(_)_MPY-CORE_Val_String» "int"),
  ("str", SortVal.«typeV(_)_MPY-CORE_Val_String» "str"),
  ("float", SortVal.«typeV(_)_MPY-CORE_Val_String» "float")]

def candidateBindingSingleton (entry : SortString × SortVal) : SortMap :=
  «_|->_» (SortKItem.inj_SortString entry.1)
    ((@inj SortVal SortKItem) entry.2)

noncomputable def candidateBindingsFromEntries : List (SortString × SortVal) → SortMap
  | [] => «.Map»
  | first :: rest =>
      rest.foldl (fun result entry =>
        _Map_ result (candidateBindingSingleton entry))
        (candidateBindingSingleton first)

noncomputable def candidateBuiltinBindings : SortMap :=
  candidateBindingsFromEntries builtinSourceEntries

def builtinMapEntry (name : SortString) (value : SortVal) :
    SortKItem × SortKItem :=
  (SortKItem.inj_SortString name, (@inj SortVal SortKItem) value)

theorem mapContainsModel_false
    (entries : List (SortKItem × SortKItem)) (key : SortKItem)
    (hAbsent : ∀ entry ∈ entries, entry.1 ≠ key) :
    mapContainsModel entries key = false := by
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
      rw [mapContainsModel, if_neg (hAbsent entry (by simp))]
      exact ih (fun candidate membership =>
        hAbsent candidate (by simp [membership]))

theorem mapDisjointModel_singleton
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem)
    (hAbsent : mapContainsModel entries key = false) :
    mapDisjointModel entries [(key, value)] = true := by
  simp [mapDisjointModel, hAbsent]

theorem candidateMap_merge_when
    (left right result : SortMap)
    (hDisjoint : mapDisjointModel left.coll right.coll = true)
    (hMerge : left.coll.foldr
      (fun entry accumulated =>
        mapInsertModel entry.1 entry.2 accumulated)
      right.coll = result.coll) :
    _Map_ left right = result := by
  simp [Proof._Map_, hDisjoint, hMerge]
  cases result
  rfl

noncomputable def candidateBuiltinStage0 : SortMap :=
  candidateBindingSingleton ("len", SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")

theorem candidateBuiltinStage0_eq :
    candidateBuiltinStage0 = ⟨[builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len")]⟩ := by rfl

noncomputable def candidateBuiltinStage1 : SortMap :=
  _Map_ candidateBuiltinStage0
    (candidateBindingSingleton ("set", SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"))

theorem candidateBuiltinStage1_eq :
    candidateBuiltinStage1 = ⟨[
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set")
    ]⟩ := by
  unfold candidateBuiltinStage1
  rw [candidateBuiltinStage0_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [Proof.«_|->_», List.mem_singleton] at hEntry
    subst entry
    simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage2 : SortMap :=
  _Map_ candidateBuiltinStage1
    (candidateBindingSingleton ("sum", SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"))

theorem candidateBuiltinStage2_eq :
    candidateBuiltinStage2 = ⟨[
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage2
  rw [candidateBuiltinStage1_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage3 : SortMap :=
  _Map_ candidateBuiltinStage2
    (candidateBindingSingleton ("abs", SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"))

theorem candidateBuiltinStage3_eq :
    candidateBuiltinStage3 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage3
  rw [candidateBuiltinStage2_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage4 : SortMap :=
  _Map_ candidateBuiltinStage3
    (candidateBindingSingleton ("min", SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"))

theorem candidateBuiltinStage4_eq :
    candidateBuiltinStage4 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage4
  rw [candidateBuiltinStage3_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage5 : SortMap :=
  _Map_ candidateBuiltinStage4
    (candidateBindingSingleton ("max", SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"))

theorem candidateBuiltinStage5_eq :
    candidateBuiltinStage5 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage5
  rw [candidateBuiltinStage4_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage6 : SortMap :=
  _Map_ candidateBuiltinStage5
    (candidateBindingSingleton ("ord", SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"))

theorem candidateBuiltinStage6_eq :
    candidateBuiltinStage6 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage6
  rw [candidateBuiltinStage5_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage7 : SortMap :=
  _Map_ candidateBuiltinStage6
    (candidateBindingSingleton ("chr", SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"))

theorem candidateBuiltinStage7_eq :
    candidateBuiltinStage7 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage7
  rw [candidateBuiltinStage6_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage8 : SortMap :=
  _Map_ candidateBuiltinStage7
    (candidateBindingSingleton ("range", SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"))

theorem candidateBuiltinStage8_eq :
    candidateBuiltinStage8 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage8
  rw [candidateBuiltinStage7_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage9 : SortMap :=
  _Map_ candidateBuiltinStage8
    (candidateBindingSingleton ("all", SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"))

theorem candidateBuiltinStage9_eq :
    candidateBuiltinStage9 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage9
  rw [candidateBuiltinStage8_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage10 : SortMap :=
  _Map_ candidateBuiltinStage9
    (candidateBindingSingleton ("any", SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"))

theorem candidateBuiltinStage10_eq :
    candidateBuiltinStage10 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum")
    ]⟩ := by
  unfold candidateBuiltinStage10
  rw [candidateBuiltinStage9_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage11 : SortMap :=
  _Map_ candidateBuiltinStage10
    (candidateBindingSingleton ("zip", SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip"))

theorem candidateBuiltinStage11_eq :
    candidateBuiltinStage11 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage11
  rw [candidateBuiltinStage10_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage12 : SortMap :=
  _Map_ candidateBuiltinStage11
    (candidateBindingSingleton ("isinstance", SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"))

theorem candidateBuiltinStage12_eq :
    candidateBuiltinStage12 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage12
  rw [candidateBuiltinStage11_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage13 : SortMap :=
  _Map_ candidateBuiltinStage12
    (candidateBindingSingleton ("sorted", SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"))

theorem candidateBuiltinStage13_eq :
    candidateBuiltinStage13 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage13
  rw [candidateBuiltinStage12_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage14 : SortMap :=
  _Map_ candidateBuiltinStage13
    (candidateBindingSingleton ("list", SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"))

theorem candidateBuiltinStage14_eq :
    candidateBuiltinStage14 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage14
  rw [candidateBuiltinStage13_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage15 : SortMap :=
  _Map_ candidateBuiltinStage14
    (candidateBindingSingleton ("round", SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"))

theorem candidateBuiltinStage15_eq :
    candidateBuiltinStage15 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage15
  rw [candidateBuiltinStage14_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage16 : SortMap :=
  _Map_ candidateBuiltinStage15
    (candidateBindingSingleton ("bin", SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"))

theorem candidateBuiltinStage16_eq :
    candidateBuiltinStage16 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage16
  rw [candidateBuiltinStage15_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage17 : SortMap :=
  _Map_ candidateBuiltinStage16
    (candidateBindingSingleton ("enumerate", SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"))

theorem candidateBuiltinStage17_eq :
    candidateBuiltinStage17 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage17
  rw [candidateBuiltinStage16_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage18 : SortMap :=
  _Map_ candidateBuiltinStage17
    (candidateBindingSingleton ("map", SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"))

theorem candidateBuiltinStage18_eq :
    candidateBuiltinStage18 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "map" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage18
  rw [candidateBuiltinStage17_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage19 : SortMap :=
  _Map_ candidateBuiltinStage18
    (candidateBindingSingleton ("eval", SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"))

theorem candidateBuiltinStage19_eq :
    candidateBuiltinStage19 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "eval" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "map" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage19
  rw [candidateBuiltinStage18_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage20 : SortMap :=
  _Map_ candidateBuiltinStage19
    (candidateBindingSingleton ("int", SortVal.«typeV(_)_MPY-CORE_Val_String» "int"))

theorem candidateBuiltinStage20_eq :
    candidateBuiltinStage20 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "eval" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"),
      builtinMapEntry "int" (SortVal.«typeV(_)_MPY-CORE_Val_String» "int"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "map" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage20
  rw [candidateBuiltinStage19_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage21 : SortMap :=
  _Map_ candidateBuiltinStage20
    (candidateBindingSingleton ("str", SortVal.«typeV(_)_MPY-CORE_Val_String» "str"))

theorem candidateBuiltinStage21_eq :
    candidateBuiltinStage21 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "eval" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"),
      builtinMapEntry "int" (SortVal.«typeV(_)_MPY-CORE_Val_String» "int"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "map" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "str" (SortVal.«typeV(_)_MPY-CORE_Val_String» "str"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage21
  rw [candidateBuiltinStage20_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

noncomputable def candidateBuiltinStage22 : SortMap :=
  _Map_ candidateBuiltinStage21
    (candidateBindingSingleton ("float", SortVal.«typeV(_)_MPY-CORE_Val_String» "float"))

theorem candidateBuiltinStage22_eq :
    candidateBuiltinStage22 = ⟨[
      builtinMapEntry "abs" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "abs"),
      builtinMapEntry "all" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "all"),
      builtinMapEntry "any" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "any"),
      builtinMapEntry "bin" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "bin"),
      builtinMapEntry "chr" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "chr"),
      builtinMapEntry "enumerate" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "enumerate"),
      builtinMapEntry "eval" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "eval"),
      builtinMapEntry "float" (SortVal.«typeV(_)_MPY-CORE_Val_String» "float"),
      builtinMapEntry "int" (SortVal.«typeV(_)_MPY-CORE_Val_String» "int"),
      builtinMapEntry "isinstance" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "isinstance"),
      builtinMapEntry "len" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "len"),
      builtinMapEntry "list" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "list"),
      builtinMapEntry "map" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "map"),
      builtinMapEntry "max" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "max"),
      builtinMapEntry "min" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "min"),
      builtinMapEntry "ord" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "ord"),
      builtinMapEntry "range" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "range"),
      builtinMapEntry "round" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "round"),
      builtinMapEntry "set" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "set"),
      builtinMapEntry "sorted" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sorted"),
      builtinMapEntry "str" (SortVal.«typeV(_)_MPY-CORE_Val_String» "str"),
      builtinMapEntry "sum" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "sum"),
      builtinMapEntry "zip" (SortVal.«builtinV(_)_MPY-CORE_Val_String» "zip")
    ]⟩ := by
  unfold candidateBuiltinStage22
  rw [candidateBuiltinStage21_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hEntry
    rcases hEntry with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
    all_goals simp [builtinMapEntry]
  · rfl

theorem candidateBuiltinBindings_eq_stage :
    candidateBuiltinBindings = candidateBuiltinStage22 := by rfl

theorem candidateBuiltinBindings_eq :
    candidateBuiltinBindings = builtinBindings := by
  rw [candidateBuiltinBindings_eq_stage, candidateBuiltinStage22_eq]
  rfl

noncomputable def candidateGlobalBindings : SortMap :=
  «_|->_» (SortKItem.inj_SortString "smallest_change")
    ((@inj SortVal SortKItem)
      (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int»
        (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "arr"
          SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»)
        functionBodyStmts 0))

noncomputable def candidateOuterScopes : SortMap :=
  _Map_
    («_|->_» (SortKItem.inj_SortInt (-1))
      (SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
          candidateBuiltinBindings SortParent.«root_MPY-CORE_Parent»)))
    («_|->_» (SortKItem.inj_SortInt 0)
      (SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
          candidateGlobalBindings
          (SortParent.«parent(_)_MPY-CORE_Parent_Int» (-1)))))

noncomputable def candidateArrChanges
    (values : SortValSeq) (changes : SortInt) : SortMap :=
  _Map_
    («_|->_» (SortKItem.inj_SortString "arr")
      (SortKItem.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)))
    («_|->_» (SortKItem.inj_SortString "changes")
      (SortKItem.inj_SortInt changes))

noncomputable def candidateLocalBindings
    (values : SortValSeq) (changes index : SortInt) : SortMap :=
  _Map_ (candidateArrChanges values changes)
    («_|->_» (SortKItem.inj_SortString "i")
      (SortKItem.inj_SortInt index))

noncomputable def candidateActiveScopes
    (values : SortValSeq) (changes index : SortInt) : SortMap :=
  _Map_ candidateOuterScopes
    («_|->_» (SortKItem.inj_SortInt 1)
      (SortKItem.inj_SortScope
        (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
          (candidateLocalBindings values changes index)
          (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0))))

theorem candidateGlobalBindings_eq :
    candidateGlobalBindings = globalBindings := by rfl

theorem candidateOuterScopes_eq : candidateOuterScopes = outerScopes := by
  unfold candidateOuterScopes
  rw [candidateBuiltinBindings_eq, candidateGlobalBindings_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [Proof.«_|->_», List.mem_singleton] at hEntry
    subst entry
    simp [Proof.«_|->_», builtinBindings, globalBindings]
  · rfl

theorem candidateArrChanges_eq
    (values : SortValSeq) (changes : SortInt) :
    candidateArrChanges values changes = arrChangesBindings values changes := by
  unfold candidateArrChanges
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [Proof.«_|->_», List.mem_singleton] at hEntry
    subst entry
    simp [Proof.«_|->_»]
  · rfl

theorem candidateLocalBindings_eq
    (values : SortValSeq) (changes index : SortInt) :
    candidateLocalBindings values changes index =
      localBindings values changes index := by
  unfold candidateLocalBindings
  rw [candidateArrChanges_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [arrChangesBindings, List.mem_cons, List.not_mem_nil, or_false]
      at hEntry
    rcases hEntry with (rfl | rfl)
    all_goals simp [Proof.«_|->_»]
  · rfl

theorem candidateActiveScopes_eq
    (values : SortValSeq) (changes index : SortInt) :
    candidateActiveScopes values changes index =
      activeScopes values changes index := by
  unfold candidateActiveScopes
  rw [candidateOuterScopes_eq, candidateLocalBindings_eq]
  apply candidateMap_merge_when
  · apply mapDisjointModel_singleton
    apply mapContainsModel_false
    intro entry hEntry
    simp only [outerScopes, List.mem_cons, List.not_mem_nil, or_false]
      at hEntry
    rcases hEntry with (rfl | rfl)
    all_goals simp [Proof.«_|->_», outerMinusEntry, outerZeroEntry]
  · rfl


set_option maxHeartbeats 0 in
theorem final :
    Klean73SmallestChange.Lemmas.targetStatement «.List» «.Map» «_-Int_» _Map_ _andBool_ «_<Int_» «_<=Int_» «_|->_» «_+Int_» ListItem «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» «halfLen(_)_VERIFICATION-BASE_Int_ValSeq» «mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int» «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» «vsLen(_)_MPY-CORE_Int_ValSeq» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val?» := by
  unfold Klean73SmallestChange.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_⟩
  · intro counter values hAll
    change Rewrites
      { k := { val := whileControl returnControl },
        env := { val := 1 },
        scopes := { val := (candidateActiveScopes values 0 0) },
        scopeLoc := { val := 2 }, heap := { val := «.Map» },
        heapLoc := { val := 0 }, stack := { val := callStack },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
        exitCode := { val := 0 }, generatedCounter := counter }
      { k := { val := SortK.kseq (SortKItem.inj_SortInt
          («mismatchCount(_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Int» values 0
            («halfLen(_)_VERIFICATION-BASE_Int_ValSeq» values))) SortK.dotk },
        env := { val := 0 }, scopes := { val := candidateOuterScopes },
        scopeLoc := { val := 1 }, heap := { val := «.Map» },
        heapLoc := { val := 0 }, stack := { val := «.List» },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := { val := SortExc.«NoExc_MPY-CORE_Exc» },
        exitCode := { val := 0 }, generatedCounter := counter }
    rw [candidateActiveScopes_eq, candidateOuterScopes_eq]
    exact execute_canonical values counter hAll
  · intro index values hGuard
    constructor
    · intro _
      trivial
    · intro _
      have hParts := hGuard
      simp [Proof._andBool_, Proof.«_<=Int_», Proof.«_<Int_»] at hParts
      have hAll :
          «allInts(_)_VERIFICATION-BASE_Bool_ValSeq» values = true :=
        hParts.1.1
      obtain ⟨left, hLeft⟩ :=
        allInts_valSeqAtModel_int values index hAll
      obtain ⟨right, hRight⟩ :=
        allInts_valSeqAtModel_int values
          («_+Int_» («_-Int_» («vsLen(_)_MPY-CORE_Int_ValSeq» values) index) (-1))
          hAll
      simpa [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val?»,
        «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int», hLeft, hRight] using
        applyCmpModel_int_ne_isSome left right
  · intro c b a
    simp [«_+Int_», Int.add_assoc]

end Proof
