requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation.  The precondition is realized by the normal
  // one-element input ["a"], whose actual result is "a", not "wrong".
  claim [false-result]:
    <mpy>
      <k> solutionAST => .K </k>
      <words> cons("a", nil) </words>
      <best> "" => ?FINALBEST:String </best>
      <bestCount> -1 => ?FINALCOUNT:Int </bestCount>
      <word> "" => ?FINALWORD:String </word>
      <count> 0 => ?LASTCOUNT:Int </count>
      <result> noResult => result(strVal("wrong")) </result>
    </mpy>
endmodule
