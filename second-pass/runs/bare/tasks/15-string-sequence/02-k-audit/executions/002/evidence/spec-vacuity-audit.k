requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim [wrong-zero-result]:
    <mpy>
      <k> init(targetProgram(), 0) => SVal("1") </k>
      <env> .Map </env>
      <functions>
        .Map => "string_sequence" |-> targetFunction()
      </functions>
      <stack> .List </stack>
    </mpy>
endmodule
