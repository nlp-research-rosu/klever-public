requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for the satisfying witness S = "", execution returns
  // intVal(0), while this destination demands intVal(#vowels("") +Int 1) = 1.
  claim [false-off-by-one]:
    <k> Call(Name("vowels_count"), strVal(S:String)) ~> KONT:K
      => intVal(#vowels(S) +Int 1) ~> KONT
    </k>
    <env> _ENV:Map </env>
    <functions>
      "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> _STACK:List </stack>
endmodule
