requires "semantic.k"

module AUDIT-CLAIM-WITNESS
  imports EXECUTION

  claim [make-palindrome-cat]:
    <mpy>
      <k> #run(#solution, "cat") => .K </k>
      <program> #solution </program>
      <input> "cat" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("catac") </result>
    </mpy>

  claim [helper-cat]:
    <mpy>
      <k> #runFunction("is_palindrome", #solution, "cat") => .K </k>
      <program> #solution </program>
      <input> "cat" </input>
      <ast-match> true </ast-match>
      <result> .K => boolVal(false) </result>
    </mpy>

  claim [helper-abba]:
    <mpy>
      <k> #runFunction("is_palindrome", #solution, "abba") => .K </k>
      <program> #solution </program>
      <input> "abba" </input>
      <ast-match> true </ast-match>
      <result> .K => boolVal(true) </result>
    </mpy>
endmodule
