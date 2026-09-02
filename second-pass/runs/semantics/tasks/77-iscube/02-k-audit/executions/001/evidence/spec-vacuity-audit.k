requires "verification.k"

module ISCUBE-SPEC-VACUITY-AUDIT
  imports ISCube-VERIFICATION

  // Fresh audit mutation of the result-bearing positive-cube obligation.
  // The precondition is satisfiable at the concrete witness input 1, and both
  // Python implementations return true there; the deliberately false target
  // below requires false.
  claim [false-result-at-one]:
    <k>
      Call(Name("iscube"), (Int(1), .Exprs))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
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
