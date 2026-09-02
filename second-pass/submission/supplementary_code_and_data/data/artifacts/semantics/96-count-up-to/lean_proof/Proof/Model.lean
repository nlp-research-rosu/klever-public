import Klean96CountUpTo.Lemmas
import Proof.Operational

namespace Proof

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e, rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  { coll := right.coll ++ left.coll }
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e, rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool :=
  left && right
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e, rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool :=
  decide (left ≤ right)
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e, rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  { coll := [(key, value)] }
/- KORE symbol: LblnoDivisor; frozen source obligations: rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def pyModTotal (left right : SortInt) : SortInt :=
  Int.tmod (Int.tmod left right + right) right

def noDivisorSteps (candidate divisor : SortInt) : Nat → SortBool
  | 0 => true
  | steps + 1 =>
      decide (pyModTotal candidate divisor ≠ 0) &&
        noDivisorSteps candidate (divisor + 1) steps

def noDivisor (candidate divisor upper : SortInt) : SortBool :=
  noDivisorSteps candidate divisor (upper - divisor).toNat
/- KORE symbol: LblprimesAcc; frozen source obligations: rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def valSeqAppendInt (values : SortValSeq) (value : SortInt) : SortValSeq :=
  match values with
  | .«.ValSeq_MPY-CORE_ValSeq» =>
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (.inj_SortInt value)
        .«.ValSeq_MPY-CORE_ValSeq»
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head
        (valSeqAppendInt tail value)

theorem valSeqConcatSingleton (values : SortValSeq) (value : SortInt) :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» values
        (.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (.inj_SortInt value)
          .«.ValSeq_MPY-CORE_ValSeq») =
      some (valSeqAppendInt values value) := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        _218e890, _830ee66, valSeqAppendInt]
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
        _218e890, _830ee66, valSeqAppendInt,
        valSeqConcatSingleton tail value]
termination_by values

def primesAccSteps (values : SortValSeq) (candidate : SortInt) :
    Nat → SortValSeq
  | 0 => values
  | steps + 1 =>
      primesAccSteps
        (if noDivisor candidate 2 candidate then
          valSeqAppendInt values candidate
        else
          values)
        (candidate + 1) steps

def primesAcc (values : SortValSeq) (start upper : SortInt) : SortValSeq :=
  primesAccSteps values start (upper - start).toNat

def innerLocals
    (candidate divisor : SortInt) (isPrime : SortBool) (n : SortInt) :
    SortMap :=
  _Map_
    (_Map_
      (_Map_
        (_Map_
          («_|->_» (.inj_SortString "candidate") (.inj_SortInt candidate))
          («_|->_» (.inj_SortString "divisor") (.inj_SortInt divisor)))
        («_|->_» (.inj_SortString "is_prime") (.inj_SortBool isPrime)))
      («_|->_» (.inj_SortString "n") (.inj_SortInt n)))
    («_|->_» (.inj_SortString "result")
      (.inj_SortVal (.«ref(_)_MPY-CORE_Val_Int» 0)))

def outerLocals
    (n candidate : SortInt) (isPrime : SortBool) (divisor : SortInt) :
    SortMap :=
  _Map_
    (_Map_
      (_Map_
        (_Map_
          («_|->_» (.inj_SortString "n") (.inj_SortInt n))
          («_|->_» (.inj_SortString "candidate") (.inj_SortInt candidate)))
        («_|->_» (.inj_SortString "is_prime") (.inj_SortBool isPrime)))
      («_|->_» (.inj_SortString "divisor") (.inj_SortInt divisor)))
    («_|->_» (.inj_SortString "result")
      (.inj_SortVal (.«ref(_)_MPY-CORE_Val_Int» 0)))

def loopLocals
    (outerLayout : Bool) (candidate divisor : SortInt)
    (isPrime : SortBool) (n : SortInt) : SortMap :=
  if outerLayout then
    outerLocals n candidate isPrime divisor
  else
    innerLocals candidate divisor isPrime n

def ambientScopes (builtins moduleVars : SortMap) : SortMap :=
  _Map_
    («_|->_» (.inj_SortInt 0)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        moduleVars (.«parent(_)_MPY-CORE_Parent_Int» (-1)))))
    («_|->_» (.inj_SortInt (-1))
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        builtins .«root_MPY-CORE_Parent»)))

def allScopes
    (locals builtins moduleVars : SortMap) : SortMap :=
  _Map_ (ambientScopes builtins moduleVars)
    («_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        locals (.«parent(_)_MPY-CORE_Parent_Int» 0))))

def heapList (values : SortValSeq) : SortMap :=
  «_|->_» (.inj_SortInt 0)
    (.inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» values))

def machine
    (code : SortK) (locals builtins moduleVars : SortMap)
    (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) : SortGeneratedTopCell :=
  { k := { val := code }
    env := { val := 1 }
    scopes := { val := allScopes locals builtins moduleVars }
    scopeLoc := scopeLoc
    heap := { val := heapList values }
    heapLoc := heapLoc
    stack := stack
    ret := ret
    exc := exc
    exitCode := exitCode
    generatedCounter := generatedCounter }

def innerCondition : SortExpr :=
  .«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
    (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
    (.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<"
      (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate"))

def innerBody : SortStmts :=
  .«___MPY-SYNTAX_Stmts_Stmt_Stmts»
    (.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
      (.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
        (.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%"
          (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
          (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor"))
        (.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "=="
          (.«Int(_)_MPY-SYNTAX_Expr_Int» 0)))
      (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
        (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
          (.«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
          (.«Bool(_)_MPY-SYNTAX_Expr_Bool» false))
        .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
      .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
    (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
      (.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
        (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor") "+"
        (.«Int(_)_MPY-SYNTAX_Expr_Int» 1))
      .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)

def innerLoop : SortKItem :=
  .«#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts» innerCondition innerBody

def innerWhileStatement : SortStmt :=
  .«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» innerCondition innerBody

def appendStatement : SortStmt :=
  .«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
    (.«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
    (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
      (.«Expr(_)_MPY-SYNTAX_Stmt_Expr»
        (.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs»
          (.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "result") "append")
          (.«_,__MPY-SYNTAX_Exprs_Expr_Exprs»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
            .«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))
      .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
    .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»

def outerTail : SortStmts :=
  .«___MPY-SYNTAX_Stmts_Stmt_Stmts»
    (.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts»
      (.«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
      (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
        (.«Expr(_)_MPY-SYNTAX_Stmt_Expr»
          (.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs»
            (.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String»
              (.«Name(_)_MPY-SYNTAX_Expr_String» "result") "append")
            (.«_,__MPY-SYNTAX_Exprs_Expr_Exprs»
              (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
              .«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))
        .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
      .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
    (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
      (.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
        (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate") "+"
        (.«Int(_)_MPY-SYNTAX_Expr_Int» 1))
      (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
        (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
          (.«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
          (.«Bool(_)_MPY-SYNTAX_Expr_Bool» true))
        (.«___MPY-SYNTAX_Stmts_Stmt_Stmts»
          (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
            (.«Int(_)_MPY-SYNTAX_Expr_Int» 2))
          .«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))

def outerBody : SortStmts :=
  .«___MPY-SYNTAX_Stmts_Stmt_Stmts» innerWhileStatement outerTail

def outerCondition : SortExpr :=
  .«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
    (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
    (.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<"
      (.«Name(_)_MPY-SYNTAX_Expr_String» "n"))

def outerLoop : SortKItem :=
  .«#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts» outerCondition outerBody

theorem lookupInner
    (outerLayout : Bool) (candidate divisor : SortInt)
    (isPrime : SortBool) (n : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell)
    (name : SortString) (value : SortVal) (rest : SortK)
    (contains :
      «_in_keys(_)_MAP_Bool_KItem_Map»
        ((@inj SortString SortKItem) name)
        (loopLocals outerLayout candidate divisor isPrime n) = some true)
    (lookup :
      «Map:lookup» (loopLocals outerLayout candidate divisor isPrime n)
        ((@inj SortString SortKItem) name) =
          some ((@inj SortVal SortKItem) value))
    (project :
      «project:Val»
          (.kseq ((@inj SortVal SortKItem) value) .dotk) =
        some value) :
    Rewrites
      (machine (.kseq (.inj_SortExpr
          (.«Name(_)_MPY-SYNTAX_Expr_String» name)) rest)
        (loopLocals outerLayout candidate divisor isPrime n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine (.kseq ((@inj SortVal SortKItem) value) rest)
        (loopLocals outerLayout candidate divisor isPrime n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter) := by
  unfold machine heapList
  apply Rewrites.tran Rewrites._6d39855
  exact Rewrites.localLookup
    (M := loopLocals outerLayout candidate divisor isPrime n)
    (outer := ambientScopes builtins moduleVars)
    (scopes := allScopes
      (loopLocals outerLayout candidate divisor isPrime n)
      builtins moduleVars)
    (singleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (loopLocals outerLayout candidate divisor isPrime n)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (X := name) (V := value)
    (parent := .«parent(_)_MPY-CORE_Parent_Int» 0) (L := 1)
    contains
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
    lookup
    project

theorem assignInnerBool
    (outerLayout : Bool) (candidate divisor : SortInt)
    (oldValue newValue : SortBool)
    (n : SortInt) (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK) :
    Rewrites
      (machine (.kseq (.inj_SortStmt
          (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
            (.«Bool(_)_MPY-SYNTAX_Expr_Bool» newValue))) rest)
        (loopLocals outerLayout candidate divisor oldValue n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine rest
        (loopLocals outerLayout candidate divisor newValue n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter) := by
  unfold machine heapList
  kstep Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat»
  kstep Rewrites._d77a1b8
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
      (HOLE := (@inj SortVal SortExpr) (.inj_SortBool newValue))
      (K0 := .«Name(_)_MPY-SYNTAX_Expr_String» "is_prime")
      rfl rfl rfl)
  exact Rewrites.localAssign
    (M := loopLocals outerLayout candidate divisor oldValue n)
    (updated := loopLocals outerLayout candidate divisor newValue n)
    (outer := ambientScopes builtins moduleVars)
    (scopes := allScopes
      (loopLocals outerLayout candidate divisor oldValue n)
      builtins moduleVars)
    (newScopes := allScopes
      (loopLocals outerLayout candidate divisor newValue n)
      builtins moduleVars)
    (singleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (loopLocals outerLayout candidate divisor oldValue n)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (newSingleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (loopLocals outerLayout candidate divisor newValue n)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (X := "is_prime") (V := .inj_SortBool newValue)
    (parent := .«parent(_)_MPY-CORE_Parent_Int» 0) (L := 1)
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
    (by
      cases outerLayout <;>
        simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
          _Map_, «_|->_», «Map:update»]
      all_goals unfold_kmap_models
      all_goals
        simp [inj, Inj.inj, instInjSortStringSortKItem,
          instInjSortValSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])

theorem incrementInnerDivisor
    (outerLayout : Bool) (candidate divisor : SortInt)
    (isPrime : SortBool) (n : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK) :
    Rewrites
      (machine (.kseq (.inj_SortStmt
          (.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor") "+"
            (.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) rest)
        (loopLocals outerLayout candidate divisor isPrime n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine rest
        (loopLocals outerLayout candidate (divisor + 1) isPrime n)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter) := by
  unfold machine heapList
  kstep Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_heat»
  kstep Rewrites._665cd53
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_cool»
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt 1))
      (K0 := .«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
      (K1 := "+") rfl rfl rfl)
  exact Rewrites.localAugAssign
    (M := loopLocals outerLayout candidate divisor isPrime n)
    (updated := loopLocals outerLayout candidate (divisor + 1) isPrime n)
    (outer := ambientScopes builtins moduleVars)
    (scopes := allScopes
      (loopLocals outerLayout candidate divisor isPrime n)
      builtins moduleVars)
    (newScopes := allScopes
      (loopLocals outerLayout candidate (divisor + 1) isPrime n)
      builtins moduleVars)
    (singleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (loopLocals outerLayout candidate divisor isPrime n)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (newSingleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (loopLocals outerLayout candidate (divisor + 1) isPrime n)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (X := "divisor") (OP := "+") (old := .inj_SortInt divisor)
    (rhs := .inj_SortInt 1) (value := .inj_SortInt (divisor + 1))
    (parent := .«parent(_)_MPY-CORE_Parent_Int» 0) (L := 1)
    (by
      cases outerLayout <;>
        simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
          _Map_, «_|->_»,
          «_in_keys(_)_MAP_Bool_KItem_Map»]
      all_goals unfold_kmap_models
      all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
    (by
      cases outerLayout <;>
        simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
          _Map_, «_|->_», «Map:lookup»]
      all_goals unfold_kmap_models
      all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
    (by rfl)
    (by
      simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        _13d6ee6, _1909c2e, _2acce51, _30456db, _3598da3,
        _42bfa12, _4f03d42, _4f373ea, _50f1b5a, _614d946,
        _798d463, _7f23ecf, _7ff1b9f, _a4f5818, _a4f63fd,
        _a6670cb, _b009d60, _bb59890, _bc844c7,
        «_+Int_», inj, Inj.inj, instInjSortIntSortVal])
    (by
      cases outerLayout <;>
        simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
          _Map_, «_|->_», «Map:update»]
      all_goals unfold_kmap_models
      all_goals
        simp [inj, Inj.inj, instInjSortStringSortKItem,
          instInjSortValSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])

theorem incrementOuterCandidate
    (n candidate : SortInt) (isPrime : SortBool) (divisor : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK) :
    Rewrites
      (machine (.kseq (.inj_SortStmt
          (.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate") "+"
            (.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) rest)
        (outerLocals n candidate isPrime divisor)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter)
      (machine rest
        (outerLocals n (candidate + 1) isPrime divisor)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter) := by
  unfold machine heapList
  kstep Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_heat»
  kstep Rewrites._665cd53
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_AugAssign(_,_,_)_MPY_SYNTAX_Stmt_Expr_String_Expr3_cool»
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt 1))
      (K0 := .«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
      (K1 := "+") rfl rfl rfl)
  exact Rewrites.localAugAssign
    (M := outerLocals n candidate isPrime divisor)
    (updated := outerLocals n (candidate + 1) isPrime divisor)
    (outer := ambientScopes builtins moduleVars)
    (scopes := allScopes
      (outerLocals n candidate isPrime divisor) builtins moduleVars)
    (newScopes := allScopes
      (outerLocals n (candidate + 1) isPrime divisor)
      builtins moduleVars)
    (singleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (outerLocals n candidate isPrime divisor)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (newSingleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (outerLocals n (candidate + 1) isPrime divisor)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (X := "candidate") (OP := "+") (old := .inj_SortInt candidate)
    (rhs := .inj_SortInt 1) (value := .inj_SortInt (candidate + 1))
    (parent := .«parent(_)_MPY-CORE_Parent_Int» 0) (L := 1)
    (by
      simp only [outerLocals, _Map_, «_|->_»,
        «_in_keys(_)_MAP_Bool_KItem_Map»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortStringSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
    (by
      simp only [outerLocals, _Map_, «_|->_», «Map:lookup»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortStringSortKItem])
    (by rfl)
    (by
      simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        _13d6ee6, _1909c2e, _2acce51, _30456db, _3598da3,
        _42bfa12, _4f03d42, _4f373ea, _50f1b5a, _614d946,
        _798d463, _7f23ecf, _7ff1b9f, _a4f5818, _a4f63fd,
        _a6670cb, _b009d60, _bb59890, _bc844c7,
        «_+Int_», inj, Inj.inj, instInjSortIntSortVal])
    (by
      simp only [outerLocals, _Map_, «_|->_», «Map:update»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortStringSortKItem,
        instInjSortValSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])

theorem assignOuterDivisor
    (n candidate : SortInt) (isPrime : SortBool)
    (oldValue newValue : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK) :
    Rewrites
      (machine (.kseq (.inj_SortStmt
          (.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
            (.«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
            (.«Int(_)_MPY-SYNTAX_Expr_Int» newValue))) rest)
        (outerLocals n candidate isPrime oldValue)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter)
      (machine rest (outerLocals n candidate isPrime newValue)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter) := by
  unfold machine heapList
  kstep Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat»
  kstep Rewrites._665cd53
  apply Rewrites.tran
    (Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt newValue))
      (K0 := .«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
      rfl rfl rfl)
  exact Rewrites.localAssign
    (M := outerLocals n candidate isPrime oldValue)
    (updated := outerLocals n candidate isPrime newValue)
    (outer := ambientScopes builtins moduleVars)
    (scopes := allScopes
      (outerLocals n candidate isPrime oldValue) builtins moduleVars)
    (newScopes := allScopes
      (outerLocals n candidate isPrime newValue) builtins moduleVars)
    (singleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (outerLocals n candidate isPrime oldValue)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (newSingleton := «_|->_» (.inj_SortInt 1)
      (.inj_SortScope (.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
        (outerLocals n candidate isPrime newValue)
        (.«parent(_)_MPY-CORE_Parent_Int» 0))))
    (X := "divisor") (V := .inj_SortInt newValue)
    (parent := .«parent(_)_MPY-CORE_Parent_Int» 0) (L := 1)
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
    (by
      simp only [outerLocals, _Map_, «_|->_», «Map:update»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortStringSortKItem,
        instInjSortValSortKItem])
    (by
      simp [«_|->_», _root_.«_|->_», inj, Inj.inj,
        instInjSortIntSortKItem, instInjSortScopeSortKItem])
    (by
      simp only [allScopes, ambientScopes, _Map_, «_|->_»,
        _root_._Map_, _root_.«_|->_»]
      unfold_kmap_models
      simp [inj, Inj.inj, instInjSortIntSortKItem,
        instInjSortScopeSortKItem])
end Proof
