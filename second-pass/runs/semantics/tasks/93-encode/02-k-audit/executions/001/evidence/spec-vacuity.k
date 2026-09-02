requires "verification.k"

module ENCODE-SPEC-VACUITY
  imports ENCODE-VERIFICATION

  // Deliberately false mutation: prefix the correct result with code 88 ("X").
  // Satisfying witness INPUT=.IntSeq returns "", not "X".
  claim [encode-total-false-prefix]:
    <k>
      Call(
        closureVal(
          ("message", .ParamNames),
          encodeFunctionBody,
          0),
        (str(INPUT:IntSeq), .Exprs))
      =>
      str(iCons(88, encodeCodes(INPUT)))
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

  // The original support claims are retained so failure is at the mutated
  // result obligation rather than caused by removal of the loop invariant.
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
