requires "verification.k"

module ENCODE-SPEC
  imports ENCODE-VERIFICATION

  // End-to-end contract.  During the joint proof this composes encode-init
  // with the independently inductive encode-loop claim below.
  claim [encode-total]:
    <k>
      Call(
        closureVal(
          ("message", .ParamNames),
          encodeFunctionBody,
          0),
        (str(INPUT:IntSeq), .Exprs))
      =>
      str(encodeCodes(INPUT))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Phase 1: normal function-call setup reaches the loop invariant with the
  // original message and an empty output accumulator.
  claim [encode-init]:
    <k>
      Call(
        closureVal(
          ("message", .ParamNames),
          encodeFunctionBody,
          0),
        (str(INPUT:IntSeq), .Exprs))
      =>
      #loop(str(INPUT), Name("char"), encodeLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
             "message" |-> str(INPUT)
             "result"  |-> str(.IntSeq)
             "char"    |-> str(.IntSeq)
             "code"    |-> 0,
             parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List => ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Phase 2: K proves the loop invariant by circularity over INPUT.
  claim [encode-loop]:
    <k>
      #loop(str(INPUT:IntSeq), Name("char"), encodeLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      =>
      str(encodeAcc(INPUT, ACC))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
             "message" |-> str(_MESSAGE:IntSeq)
             "result"  |-> str(ACC:IntSeq)
             "char"    |-> str(_OLDCHAR:IntSeq)
             "code"    |-> _OLDCODE:Int,
             parent(0))
      -1 |-> builtinsScope
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
