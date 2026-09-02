requires "semantic.k"

module AUDIT-UNICODE-WITNESS
  imports EXECUTION

  // Python regards U+00E9 as a one-code-point palindrome and returns it
  // unchanged. This checks the fixed K rules on a proper source-level value.
  claim [python-expected-e-acute]:
    <mpy>
      <k> #run(#solution, "\u00e9") => .K </k>
      <program> #solution </program>
      <input> "\u00e9" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("\u00e9") </result>
    </mpy>

  claim [python-expected-lambda]:
    <mpy>
      <k> #run(#solution, "\u03bb") => .K </k>
      <program> #solution </program>
      <input> "\u03bb" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("\u03bb") </result>
    </mpy>

  claim [python-expected-lambda-han]:
    <mpy>
      <k> #run(#solution, "\u03bb\u6f22") => .K </k>
      <program> #solution </program>
      <input> "\u03bb\u6f22" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("\u03bb\u6f22\u03bb") </result>
    </mpy>

  claim [python-expected-smiley]:
    <mpy>
      <k> #run(#solution, "\U0001f642") => .K </k>
      <program> #solution </program>
      <input> "\U0001f642" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("\U0001f642") </result>
    </mpy>
endmodule
