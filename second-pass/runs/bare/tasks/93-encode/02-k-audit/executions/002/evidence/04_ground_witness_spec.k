requires "verification.k"
requires "concrete.k"

module GROUND-WITNESS-SPEC
  imports CONCRETE
  imports VERIFICATION

  claim [loop-a-witness]:
    <k> loopString("char", "a", encodeLoopBody()) => .K </k>
    <env>
      "char"    |-> pyStr("x")
      "message" |-> pyStr("a")
      "result"  |-> pyStr("")
    =>
      "char"    |-> pyStr("c")
      "message" |-> pyStr("a")
      "result"  |-> pyStr("C")
    </env>
    <functions> .Map </functions>
    <result> noResult </result>
endmodule
