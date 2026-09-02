requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Reviewer mutation: the real program result is required to be one larger.
  // Witness A=0, B=0 satisfies the original precondition, returns 0, while
  // this destination requires 1.
  claim
    <task>
      <k> multiplyProgram ~> #invoke("multiply", A, B) => .K </k>
      <env> .Map => ("a" |-> absInt(A)) ("b" |-> absInt(B)) </env>
      <functions>
        .Map => "multiply" |-> function("a", "b", multiplyBody)
      </functions>
      <result>
        noResult => (unitDigit(A) *Int unitDigit(B)) +Int 1
      </result>
    </task>
endmodule
