requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real execution returns "ccc", not "bb".
  claim [false-concrete-result]:
      <k> longestProgram => .K </k>
      <args> listVal(strVal("a"), strVal("bb"), strVal("ccc")) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => strVal("bb") </out>
endmodule
