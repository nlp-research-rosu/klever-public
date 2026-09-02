requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Deliberately false: for the satisfying input S = "", actual result is
  // "", while this destination requires "!".
  claim [program-correct-false]:
    <k> run(solutionProgram, S) => .K </k>
    <env> .Map => .Map </env>
    <result>
      noResult => pyStr(decodeFrom(S, 0, "") +String "!")
    </result>
endmodule
