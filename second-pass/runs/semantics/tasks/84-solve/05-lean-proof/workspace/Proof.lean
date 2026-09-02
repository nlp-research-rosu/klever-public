import Klean84Solve.Lemmas
import Proof.BuildIS

namespace Proof

theorem final :
    Klean84Solve.Lemmas.targetStatement := by
  unfold Klean84Solve.Lemmas.targetStatement
  intro _Gen9 _Gen8 _Gen7 _Gen6 _Gen5 _Gen4 _Gen3 _Gen2 _Gen1 _Gen0
    _DotVar1 REST
  refine Rewrites.tran (Rewrites._1a401d8
    (OBJ := SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 REST))))) ?_
  refine Rewrites.tran (Rewrites._1fe7f3b
    (E := SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)) ?_
  apply Rewrites.tran Rewrites._665cd53
  apply Rewrites.tran Rewrites._a1c192d
  apply Rewrites.tran Rewrites._c094fe7
  apply Rewrites.tran Rewrites._bb17cff
  apply Rewrites.tran Rewrites._04d5465
  apply Rewrites.tran Rewrites._bb17cff
  apply Rewrites._7e6f52e
    (OBJ := SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 REST))))
    (LO := SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
    (HI := SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»)
    (ST := SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»)
    (_Val0 := SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» REST))
  exact Proof.BuildIS.doSlice_drop_binary_prefix REST

end Proof
