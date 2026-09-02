requires "probe.k"

module ISDIGIT-BRANCH-PROBE-SPEC3
  imports ISDIGIT-BRANCH-PROBE

  // round 3 — the ECHO's exact emission (==K .IntSeq + allDigit) over P124's
  // REAL field term (takeField of the stripped codes); the true arm demands
  // the dg spelling (isLen + dgN) back
  claim
    <k>
      If(notBool (revISAcc(trimWS(CS:IntSeq), .IntSeq) ==K .IntSeq)
         andBool allDigit(revISAcc(trimWS(CS), .IntSeq)),
         #pbS(notBool (isLen(revISAcc(trimWS(CS), .IntSeq)) ==Int 0)
      andBool dgN(revISAcc(trimWS(CS), .IntSeq)) ==Int 1) .Stmts,
         .Stmts)
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
