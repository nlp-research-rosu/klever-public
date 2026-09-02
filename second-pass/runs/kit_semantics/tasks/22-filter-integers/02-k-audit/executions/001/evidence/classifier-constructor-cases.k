requires "reference-semantics/semantics.k"

module CLASSIFIER-CONSTRUCTOR-CASES
  imports MPY

  claim [int-case]:        <k> isIntV(I:Int) => true </k>
  claim [bool-case]:       <k> isIntV(B:Bool) => true </k>
  claim [none-case]:       <k> isIntV(noneV) => false </k>
  claim [list-case]:       <k> isIntV(list(VS:ValSeq)) => false </k>
  claim [tuple-case]:      <k> isIntV(tuple(VS:ValSeq)) => false </k>
  claim [str-case]:        <k> isIntV(str(IS:IntSeq)) => false </k>
  claim [range-case]:      <k> isIntV(rangeObj(A:Int, B:Int, S:Int)) => false </k>
  claim [zip-case]:        <k> isIntV(zipObj(A:ValSeq, B:ValSeq)) => false </k>
  claim [zip-str-case]:    <k> isIntV(zipObjS(A:IntSeq, B:IntSeq)) => false </k>
  claim [ref-case]:        <k> isIntV(ref(H:Int)) => false </k>
  claim [cell-ref-case]:   <k> isIntV(cellRef(H:Int)) => false </k>
  claim [closure-case]:
    <k> isIntV(closureVal(P:ParamNames, BODY:Stmts, L:Int)) => false </k>
  claim [type-case]:       <k> isIntV(typeV(T:String)) => false </k>
  claim [builtin-case]:    <k> isIntV(builtinV(N:String)) => false </k>
  claim [method-case]:
    <k> isIntV(boundMethodV(V:Val, N:String)) => false </k>
  claim [keyword-case]:
    <k> isIntV(kwV(N:String, V:Val)) => false </k>
  claim [cells-case]:
    <k> isIntV(cellsMark(P:ParamNames)) => false </k>
  claim [annotated-closure-case]:
    <k>
      isIntV(closureValC(P:ParamNames, C:ParamNames, BODY:Stmts, M:Map))
      =>
      false
    </k>
  claim [float-case]:      <k> isIntV(F:Float) => false </k>
  claim [set-case]:        <k> isIntV(setV(IS:IntSeq)) => false </k>
  claim [dict-case]:
    <k> isIntV(dictV(KS:ValSeq, VS:ValSeq)) => false </k>
  claim [md5-case]:        <k> isIntV(md5Obj(IS:IntSeq)) => false </k>
endmodule
