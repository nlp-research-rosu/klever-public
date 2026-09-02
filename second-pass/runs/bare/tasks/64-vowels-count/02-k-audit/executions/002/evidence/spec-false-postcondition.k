requires "verification.k"

module SPEC-FALSE-POSTCONDITION
  imports VERIFICATION

  // Fresh audit mutation: the real result for "abcde" is 2, not 3.
  claim [false-plus-one-abcde]:
    <k> Call(Name("vowels_count"), strVal("abcde"))
     => intVal(3)
    </k>
    <env> .Map </env>
    <functions>
      "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>
endmodule
