requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant/circularity: ACC is exactly the already-decoded prefix,
  // and decodeFrom specifies the remaining work from index I.
  claim [loop-correct]:
    <k>
      whileLoop(decodeTest, decodeBody) ~> exec(decodeReturn)
      => .K
    </k>
    <env>
      "s" |-> pyStr(S)
      "i" |-> pyInt(I)
      "result" |-> pyStr(ACC)
      => .Map
    </env>
    <result>
      noResult => pyStr(decodeFrom(S, I, ACC))
    </result>
    requires 0 <=Int I andBool I <=Int lengthString(S)

  // End-to-end theorem for every input string.
  claim [program-correct]:
    <k> run(solutionProgram, S) => .K </k>
    <env> .Map => .Map </env>
    <result> noResult => pyStr(decodeFrom(S, 0, "")) </result>
endmodule
