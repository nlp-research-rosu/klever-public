requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed function term is materially changed to `return [99]`.
  // The original N=0 postcondition requires [1], so sound execution must refute it.
  claim [changed-executed-body]:
    <k> #loadAll(
           Module(
             FuncDef("tri", Params("n"),
               Return(ListExpr(Int(99))))))
         ~> Call(Name("tri"), Int(0))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
