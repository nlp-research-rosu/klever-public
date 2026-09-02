requires "verification.k"

module SPEC-CONCRETE-WITNESS
  imports VERIFICATION

  claim [loader-witness]:
    <k> solutionProgram ~> #entry("abcde")
     => Call(Name("vowels_count"), strVal("abcde"))
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [call-witness]:
    <k> Call(Name("vowels_count"), strVal("abcde"))
     => intVal(2)
    </k>
    <env> .Map </env>
    <functions>
      "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [combined-program-witness]:
    <k> solutionProgram ~> #entry("abcde")
     => intVal(2)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>
endmodule
