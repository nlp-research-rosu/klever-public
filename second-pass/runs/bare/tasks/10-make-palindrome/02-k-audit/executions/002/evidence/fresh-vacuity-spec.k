requires "semantic.k"

module AUDIT-FRESH-VACUITY
  imports SEMANTIC
  imports VERIFICATION

  // Deliberately false: for the satisfying witness S = "", the real and
  // claimed reference result is "", not "!".
  claim [wrong-universal-result]:
    <mpy>
      <k> #run(#solution, S) => .K </k>
      <program> #solution </program>
      <input> S </input>
      <ast-match> true </ast-match>
      <result>
        .K => strVal(#reference(S) +String "!")
      </result>
    </mpy>
endmodule
