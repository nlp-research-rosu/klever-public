requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result mutation: the real result for satisfying input 5 is
  // [1, 5], so requiring [1, 7] must leave an unmet result obligation.
  claim [false-five-result]:
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 5 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 7 :: .Ints)) </result>
    </python>
endmodule
