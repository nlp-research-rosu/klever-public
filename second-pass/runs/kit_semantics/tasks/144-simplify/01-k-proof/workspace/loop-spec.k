requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  claim [loop-phase-0]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), 0, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 0, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires isDigitC(CODE)
     andBool validScan(
       REST, 0, A *Int 10 +Int (CODE -Int 48), B, C, D)

  claim [loop-slash-0]:
    <k>
      #loop(str(iCons(47, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(47, REST), 0, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 0, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires validScan(REST, 1, A, B, C, D)

  claim [loop-phase-1]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), 1, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 1, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires isDigitC(CODE)
     andBool validScan(
       REST, 1, A, B *Int 10 +Int (CODE -Int 48), C, D)

  claim [loop-slash-1]:
    <k>
      #loop(str(iCons(47, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(47, REST), 1, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 1, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires validScan(REST, 2, A, B, C, D)

  claim [loop-phase-2]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), 2, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 2, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires isDigitC(CODE)
     andBool validScan(
       REST, 2, A, B, C *Int 10 +Int (CODE -Int 48), D)

  claim [loop-slash-2]:
    <k>
      #loop(str(iCons(47, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(47, REST), 2, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 2, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires validScan(REST, 3, A, B, C, D)

  claim [loop-phase-3]:
    <k>
      #loop(str(iCons(CODE, REST)), Name("ch"), simplifyLoopBody)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      scanResult(iCons(CODE, REST), 3, A, B, C, D)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(XARG, NARG, 3, A, B, C, D, OLDCH)
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires isDigitC(CODE)
     andBool validScan(
       REST, 3, A, B, C, D *Int 10 +Int (CODE -Int 48))

endmodule
