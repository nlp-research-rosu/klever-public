requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loading the exact AST represented by solutionProgram installs its body
  // and reaches the public entry call for every configured input string.
  claim [program-loads-solution]:
    <k> solutionProgram ~> #entry(S:String)
     => Call(Name("vowels_count"), strVal(S))
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  // The continuation, caller environment, and caller stack are generalized.
  // Consequently the same claim applies at every recursive call site.
  claim [vowels-count-correct]:
    <k> Call(Name("vowels_count"), strVal(S:String)) ~> KONT:K
     => intVal(#vowels(S)) ~> KONT
    </k>
    <env> _ENV:Map </env>
    <functions>
      "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> _STACK:List </stack>
endmodule
