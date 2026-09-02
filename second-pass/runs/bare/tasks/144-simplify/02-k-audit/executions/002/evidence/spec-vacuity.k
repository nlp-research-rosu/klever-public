requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the submitted program returns true for this input.
  claim [false-result-mutation]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify", strVal("1/5"), strVal("5/1"))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult => result(boolVal(false)) </result>
    </simplify>
endmodule
