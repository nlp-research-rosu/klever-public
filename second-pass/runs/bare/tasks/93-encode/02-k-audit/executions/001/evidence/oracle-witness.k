requires "../../tmp/audit-work/93-encode/verification.k"

module AUDIT-WRONG-ORACLE
  imports VERIFICATION

  // This is a deliberately false interpretation of the three opaque
  // result-bearing functions from semantic.k.  It is not a candidate rule.
  // Its purpose is to show that the submitted abstract proof admits a model
  // in which encode("a") returns "X", even though both Python programs return
  // "C".
  rule swapCaseChar(_C) => "X"
  rule advancedVowel(C) => C
  rule encodedChar(_C) => "X"
endmodule

module AUDIT-WRONG-ORACLE-SPEC
  imports AUDIT-WRONG-ORACLE

  claim [false-entry-a]:
    <k> encodeProgram() ~> invoke("encode", pyStr("a")) => .K </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult => returned(pyStr("X")) </result>

  claim [false-loop-a]:
    <k> loopString("char", "a", encodeLoopBody()) => .K </k>
    <env>
      "char"    |-> pyStr("a")
      "message" |-> pyStr("a")
      "result"  |-> pyStr("")
    =>
      "char"    |-> pyStr(?C)
      "message" |-> pyStr("a")
      "result"  |-> pyStr("X")
    </env>
    <functions> .Map </functions>
    <result> noResult </result>
endmodule
