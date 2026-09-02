requires "semantic.k"

module MUTATION-SPEC
  imports EXECUTION

  // Negative validation probe: the real result is "catac", so this claim must
  // fail.  prove.sh treats the expected non-zero exit as success of the probe.
  claim [wrong-cat-result]:
    <mpy>
      <k> #run(#solution, "cat") => .K </k>
      <program> #solution </program>
      <input> "cat" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("cat") </result>
    </mpy>
endmodule
