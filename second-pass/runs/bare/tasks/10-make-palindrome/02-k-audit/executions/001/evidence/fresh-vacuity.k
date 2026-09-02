requires "semantic.k"

module AUDIT-VACUITY
  imports SEMANTIC
  imports VERIFICATION

  // Fresh reviewer mutation.  "cat" satisfies the original entry state, but
  // the claimed result adds one character to the original postcondition:
  // #reference("cat") is "catac", not "catacx".
  claim [wrong-functional-result]:
    <mpy>
      <k> #run(#solution, "cat") => .K </k>
      <program> #solution </program>
      <input> "cat" </input>
      <ast-match> true </ast-match>
      <result>
        .K => strVal(#reference("cat") +String "x")
      </result>
    </mpy>
endmodule
