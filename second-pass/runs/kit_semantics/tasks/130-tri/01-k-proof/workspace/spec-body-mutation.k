requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Material mutation: replace the implementation with `return [2]` while
  // retaining the original theorem's expected n=0 result [1].
  claim [changed-body]:
    <k> #loadAll(
           Module(
             FuncDef("tri", Params("n"),
               Return(ListExpr(Int(2))))))
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
