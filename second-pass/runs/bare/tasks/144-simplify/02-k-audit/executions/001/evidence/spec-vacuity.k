requires "../source/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: 1/5 * 5/1 is exactly 1, so the real result is true.
  claim [false-result]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify", strVal("1/5"), strVal("5/1"))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult => result(boolVal(false)) </result>
    </simplify>
endmodule
