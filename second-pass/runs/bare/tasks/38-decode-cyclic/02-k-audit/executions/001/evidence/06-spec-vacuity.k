requires "../candidate-src/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // The unchanged loop circularity is required by the end-to-end execution.
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

  // Deliberately false: on the satisfying witness S="", execution returns
  // "", while this destination requires "!".
  claim [program-false-result]:
    <k> run(solutionProgram, S) => .K </k>
    <env> .Map => .Map </env>
    <result>
      noResult => pyStr(decodeFrom(S, 0, "") +String "!")
    </result>
endmodule
