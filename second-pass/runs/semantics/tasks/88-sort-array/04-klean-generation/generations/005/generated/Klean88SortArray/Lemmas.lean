import Klean88SortArray.Inj
import Klean88SortArray.Rewrite

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean88SortArray.Lemmas

def targetStatement
    : Prop :=
    (∀ (_Gen9 : SortGeneratedCounterCell) (_Gen8 : SortExitCodeCell) (_Gen7 : SortExcCell) (_Gen6 : SortRetCell) (_Gen5 : SortStackCell) (_Gen4 : SortHeapLocCell) (_Gen3 : SortHeapCell) (_Gen2 : SortScopeLocCell) (_Gen1 : SortScopesCell) (_Gen0 : SortEnvCell) (_DotVar1 : SortK) (L : SortInt) (_M : SortValSeq) (_F : SortInt), Rewrites { k := { val := SortK.kseq (SortKItem.inj_SortExpr (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _F) (SortValSeq.«snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» _M (SortVal.inj_SortInt L))))) (SortIndex.inj_SortExpr (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))))) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 } { k := { val := SortK.kseq (SortKItem.inj_SortInt L) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 })

end Klean88SortArray.Lemmas
