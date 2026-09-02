requires "verification.k"

module SPEC-INPUT-BRIDGE
  imports MPY-VERIFICATION

  // Reviewer-authored connection check for the entry theorem's structural
  // Encoded input and the concrete Raw string boundary.
  claim [raw-encoded-input-value]:
    <mpy>
      <k>
        #inputValue(Raw(S))
        => #inputValue(Encoded(#chars(S)))
      </k>
      <input> IN </input>
      <env> RHO </env>
      <functions> FS </functions>
      <result> V </result>
    </mpy>

endmodule
