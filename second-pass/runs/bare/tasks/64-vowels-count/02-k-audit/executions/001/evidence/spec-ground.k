requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // Reviewer-authored whole-program instances.  Each begins at the submitted
  // program macro with an initial state and constrains the final integer.
  claim [whole-empty]:
    <k> solutionProgram ~> #entry("")
      => intVal(0)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [whole-example-lower]:
    <k> solutionProgram ~> #entry("abcde")
      => intVal(2)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [whole-example-upper-y]:
    <k> solutionProgram ~> #entry("ACEDY")
      => intVal(3)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [whole-final-y]:
    <k> solutionProgram ~> #entry("ay")
      => intVal(2)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [whole-internal-y]:
    <k> solutionProgram ~> #entry("ya")
      => intVal(1)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>

  claim [whole-default]:
    <k> solutionProgram ~> #entry("rhythm")
      => intVal(0)
    </k>
    <env> .Map </env>
    <functions>
      .Map => "vowels_count" |-> function("s", vowelBody)
    </functions>
    <stack> .List </stack>
endmodule
