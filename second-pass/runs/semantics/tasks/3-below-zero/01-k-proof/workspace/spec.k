requires "verification.k"

module AUX-SPEC
  imports MPY-VERIFICATION

  claim
    <k> #loop(list(asValSeq(IS:IntVals)), Name("operation"), belowZeroLoopBody)
         ~> (Return(Bool(false)) .Stmts) ~> #endcall
      => prefixBelow(B, IS)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(MODULE:Map, parent(-1))
      -1 |-> BUILTINS:Scope
      1 |-> scope(
        "operations" |-> list(asValSeq(INPUT:IntVals))
        "operation"  |-> OLD:Val
        "balance"    |-> B:Int,
        parent(0))
      =>
      0 |-> scope(MODULE, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module MAIN-SPEC
  imports MPY-VERIFICATION-LEMMA

  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("below_zero"), list(asValSeq(IS:IntVals)))
      => prefixBelow(0, IS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "below_zero" |-> closureVal(
          "operations", belowZeroFunctionBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
