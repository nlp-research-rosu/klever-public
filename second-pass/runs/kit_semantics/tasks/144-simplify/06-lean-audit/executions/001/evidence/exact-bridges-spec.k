requires "/reference/k-proof/verification.k"

module EXACT-BRIDGES-SPEC
  imports VERIFICATION-BASE

  claim [exact-loop-digit-bridge]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), LOOPBODY:Stmts)
      ~> RETSTMTS:Stmts
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), P, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> CALLEESCOPE:Scope
       -1 |-> BUILTINSSCOPE:Scope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> BUILTINSSCOPE)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires LOOPBODY ==K simplifyLoopBody
     andBool RETSTMTS ==K (simplifyReturn .Stmts)
     andBool CALLEESCOPE
       ==K simplifyScope(XARG, NARG, P, A, B, C, D, OLDCH)
     andBool BUILTINSSCOPE ==K builtinsScope
     andBool 0 <=Int P andBool P <=Int 3
     andBool isDigitC(CODE)
     andBool validScan(iCons(CODE, REST), P, A, B, C, D)

  claim [exact-loop-slash-bridge]:
    <k>
      #loop(str(iCons(47, REST)), Name("ch"), LOOPBODY:Stmts)
      ~> RETSTMTS:Stmts
      ~> #endcall
      =>
      scanResult(iCons(47, REST), P, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> CALLEESCOPE:Scope
       -1 |-> BUILTINSSCOPE:Scope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> BUILTINSSCOPE)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires LOOPBODY ==K simplifyLoopBody
     andBool RETSTMTS ==K (simplifyReturn .Stmts)
     andBool CALLEESCOPE
       ==K simplifyScope(XARG, NARG, P, A, B, C, D, OLDCH)
     andBool BUILTINSSCOPE ==K builtinsScope
     andBool 0 <=Int P andBool P <Int 3
     andBool validScan(iCons(47, REST), P, A, B, C, D)
endmodule
