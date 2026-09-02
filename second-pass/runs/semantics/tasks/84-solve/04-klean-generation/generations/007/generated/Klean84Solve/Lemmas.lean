import Klean84Solve.Inj
import Klean84Solve.Rewrite

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean84Solve.Lemmas

def targetStatement
    : Prop :=
    (∀ (_Gen9 : SortGeneratedCounterCell) (_Gen8 : SortExitCodeCell) (_Gen7 : SortExcCell) (_Gen6 : SortRetCell) (_Gen5 : SortStackCell) (_Gen4 : SortHeapLocCell) (_Gen3 : SortHeapCell) (_Gen2 : SortScopeLocCell) (_Gen1 : SortScopesCell) (_Gen0 : SortEnvCell) (_DotVar1 : SortK) (REST : SortIntSeq), Rewrites { k := { val := SortK.kseq (SortKItem.inj_SortExpr (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 REST)))) (SortIndex.«Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» (SortBound.inj_SortExpr (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)) SortBound.«NoBound_MPY-SYNTAX_Bound» SortBound.«NoBound_MPY-SYNTAX_Bound»))) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 } { k := { val := SortK.kseq (SortKItem.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» REST)) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 })

end Klean84Solve.Lemmas
