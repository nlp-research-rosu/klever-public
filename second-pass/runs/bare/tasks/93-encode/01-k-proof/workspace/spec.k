requires "verification.k"
requires "concrete.k"

module SPEC
  imports VERIFICATION

  // Loop invariant: starting with accumulator R, executing the translated
  // loop body over S appends exactly the reference encoding of S.
  claim [encode-loop-correct]:
    <k> loopString("char", S, encodeLoopBody()) => .K </k>
    <env>
      "char"    |-> pyStr(C)
      "message" |-> pyStr(M)
      "result"  |-> pyStr(R)
    =>
      "char"    |-> pyStr(?C)
      "message" |-> pyStr(M)
      "result"  |-> pyStr(R +String encodeSpec(S))
    </env>
    <functions> FS </functions>
    <result> RES </result>

endmodule

module CONCRETE-SPEC
  imports CONCRETE
  imports VERIFICATION

  // The prompt's examples are retained as concrete end-to-end theorems.
  claim [example-test]:
    <k> encodeProgram() ~> invoke("encode", pyStr("test")) => .K </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult => returned(pyStr("TGST")) </result>

  claim [example-message]:
    <k> encodeProgram() ~> invoke("encode", pyStr("This is a message")) => .K </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult => returned(pyStr("tHKS KS C MGSSCGG")) </result>

  // Covers every allowed upper- and lower-case English letter, plus the
  // whitespace behavior exhibited by the prompt.
  claim [ascii-domain]:
    <k> encodeProgram()
      ~> invoke(
           "encode",
           pyStr("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "))
      => .K
    </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult
      => returned(pyStr("CBCDGFGHKJKLMNQPQRSTWVWXYZcbcdgfghkjklmnqpqrstwvwxyz "))
    </result>
endmodule
