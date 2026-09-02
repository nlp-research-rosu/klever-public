requires "verification.k"

module SPEC
  imports VERIFICATION

  // For all mathematical integers, execution returns the product of the
  // non-negative decimal unit digits.  absInt makes the sign convention
  // explicit (in particular, unitDigit(-15) is 5).
  claim
    <task>
      <k> multiplyProgram ~> #invoke("multiply", A, B) => .K </k>
      <env> .Map => ("a" |-> absInt(A)) ("b" |-> absInt(B)) </env>
      <functions>
        .Map => "multiply" |-> function("a", "b", multiplyBody)
      </functions>
      <result>
        noResult => unitDigit(A) *Int unitDigit(B)
      </result>
    </task>
endmodule
