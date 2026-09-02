requires "probe.k"

module ISDIGIT-BRANCH-PROBE-SPEC4
  imports ISDIGIT-BRANCH-PROBE

  // round 4 — the full P124 shape: not(and(c1,c2,c3)) staging over three
  // ECHO-spelled composites (==K .IntSeq + allDigit) on fn terms; the FALSE
  // arm demands the dg spellings back
  claim
    <k>
      If(UnaryOp("not",
           BoolOp("and",
             (notBool (trimWS(C1:IntSeq) ==K .IntSeq) andBool allDigit(trimWS(C1)),
              notBool (trimWS(C2:IntSeq) ==K .IntSeq) andBool allDigit(trimWS(C2)),
              notBool (trimWS(C3:IntSeq) ==K .IntSeq) andBool allDigit(trimWS(C3))))),
         .Stmts,
         #pbS((notBool (isLen(trimWS(C1)) ==Int 0) andBool dgN(trimWS(C1)) ==Int 1)
      andBool (notBool (isLen(trimWS(C2)) ==Int 0) andBool dgN(trimWS(C2)) ==Int 1)
      andBool (notBool (isLen(trimWS(C3)) ==Int 0) andBool dgN(trimWS(C3)) ==Int 1)) .Stmts)
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
