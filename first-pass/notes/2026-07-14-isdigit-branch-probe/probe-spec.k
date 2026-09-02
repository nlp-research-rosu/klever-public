requires "probe.k"

module ISDIGIT-BRANCH-PROBE-SPEC
  imports ISDIGIT-BRANCH-PROBE

  // If on the isdigit-echo composite over an abstract field; the true arm
  // demands BOTH halves back (the dg-composite guard shape)
  claim
    <k>
      If(notBool (isLen(F:IntSeq) ==Int 0) andBool dgN(F) ==Int 1,
         #pbS(notBool (isLen(F) ==Int 0) andBool dgN(F) ==Int 1) .Stmts,
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
