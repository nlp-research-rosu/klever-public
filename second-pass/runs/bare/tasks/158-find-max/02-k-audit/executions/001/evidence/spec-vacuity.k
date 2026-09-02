requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation. The satisfying input ["a"] makes the real
  // submitted program return "a"; this deliberately demands the false "".
  claim [false-ground-result]:
    <mpy>
      <k> solutionAST => .K </k>
      <words> cons("a", nil) </words>
      <best> "" => ?FINALBEST:String </best>
      <bestCount> -1 => ?FINALCOUNT:Int </bestCount>
      <word> "" => ?FINALWORD:String </word>
      <count> 0 => ?LASTCOUNT:Int </count>
      <result> noResult => result(strVal("")) </result>
    </mpy>
endmodule
