requires "semantic.k"

module UNICODE-WITNESS
  imports EXECUTION

  // Python indexes and reverses Unicode code points.  This generated K
  // semantics instead slices/reverses the UTF-8 bytes used by K String.
  // The real candidate and trusted canonical both return "a🙂b🙂a".
  claim [python-codepoint-result]:
    <mpy>
      <k> #run(#solution, "a🙂b") => .K </k>
      <program> #solution </program>
      <input> "a🙂b" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("a🙂b🙂a") </result>
    </mpy>
endmodule
