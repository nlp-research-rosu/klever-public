requires "semantic.k"

module SPEC
  imports SEMANTIC
  imports VERIFICATION

  // Universal functional-correctness claim: execution of the translated AST
  // agrees with the separate shortest-palindrome reference for every string.
  claim [functional-correctness]:
    <mpy>
      <k> #run(#solution, S) => .K </k>
      <program> #solution </program>
      <input> S </input>
      <ast-match> true </ast-match>
      <result> .K => strVal(#reference(S)) </result>
    </mpy>

  // The supplied helper is itself interpreted correctly for every string.
  claim [helper-correctness]:
    <mpy>
      <k> #runFunction("is_palindrome", #solution, S) => .K </k>
      <program> #solution </program>
      <input> S </input>
      <ast-match> true </ast-match>
      <result> .K => boolVal(#isPalindrome(S)) </result>
    </mpy>
endmodule

module CONCRETE-SPEC
  imports EXECUTION

  // End-to-end configuration claims for the examples in prompt.py.
  claim [empty]:
    <mpy>
      <k> #run(#solution, "") => .K </k>
      <program> #solution </program>
      <input> "" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("") </result>
    </mpy>

  claim [cat]:
    <mpy>
      <k> #run(#solution, "cat") => .K </k>
      <program> #solution </program>
      <input> "cat" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("catac") </result>
    </mpy>

  claim [cata]:
    <mpy>
      <k> #run(#solution, "cata") => .K </k>
      <program> #solution </program>
      <input> "cata" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("catac") </result>
    </mpy>

  // Additional cases cover immediate return and repeated-character recursion.
  claim [xyx]:
    <mpy>
      <k> #run(#solution, "xyx") => .K </k>
      <program> #solution </program>
      <input> "xyx" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("xyx") </result>
    </mpy>

  claim [abcd]:
    <mpy>
      <k> #run(#solution, "abcd") => .K </k>
      <program> #solution </program>
      <input> "abcd" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("abcdcba") </result>
    </mpy>

  claim [aabb]:
    <mpy>
      <k> #run(#solution, "aabb") => .K </k>
      <program> #solution </program>
      <input> "aabb" </input>
      <ast-match> true </ast-match>
      <result> .K => strVal("aabbaa") </result>
    </mpy>
endmodule
