requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation. For example A=148, B=412 satisfies the entry
  // precondition, the real result is 16, and this destination requires 17.
  claim
    <task>
      <k> multiplyProgram ~> #invoke("multiply", A, B) => .K </k>
      <env> .Map => ("a" |-> absInt(A)) ("b" |-> absInt(B)) </env>
      <functions>
        .Map => "multiply" |-> function("a", "b", multiplyBody)
      </functions>
      <result>
        noResult =>
          (unitDigit(A) *Int unitDigit(B)) +Int 1
      </result>
    </task>
endmodule
