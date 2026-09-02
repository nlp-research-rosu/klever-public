requires "verification.k"

module SPEC-TOTALITY-PROBE
  imports MPY-VERIFICATION

  // Coverage probe for the globally [total] bracketSpec declaration.
  // This is outside every theorem precondition (all uses have N >= 0).
  claim [negative-depth-nonopen]:
        <mpy>
          <k> bracketSpec(-1, ")") => false </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </mpy>
endmodule
