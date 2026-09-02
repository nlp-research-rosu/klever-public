requires "probe.k"

module ISDIGIT-BRANCH-PROBE-SPEC2
  imports ISDIGIT-BRANCH-PROBE

  // round 2 — the REAL P124 shape: not(and(c1, c2, c3)) over three field
  // composites; the FALSE arm (all pass) demands all three composites back
  claim
    <k>
      If(UnaryOp("not",
           BoolOp("and",
             (notBool (isLen(F1:IntSeq) ==Int 0) andBool dgN(F1) ==Int 1,
              notBool (isLen(F2:IntSeq) ==Int 0) andBool dgN(F2) ==Int 1,
              notBool (isLen(F3:IntSeq) ==Int 0) andBool dgN(F3) ==Int 1))),
         .Stmts,
         #pbS((notBool (isLen(F1) ==Int 0) andBool dgN(F1) ==Int 1)
      andBool (notBool (isLen(F2) ==Int 0) andBool dgN(F2) ==Int 1)
      andBool (notBool (isLen(F3) ==Int 0) andBool dgN(F3) ==Int 1)) .Stmts)
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
