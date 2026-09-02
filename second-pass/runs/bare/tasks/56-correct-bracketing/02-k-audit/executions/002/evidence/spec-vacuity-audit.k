requires "semantic.k"

module SPEC-VACUITY-AUDIT
  imports MPY

  claim [loop-zero]: <py>
    <k>
      forBracketSeq(BS, "bracket", targetLoopBody()) ~> targetTail() ~> functionBoundary()
      => .K
    </k>
    <functions> _FM0:Map => ?_FM:Map </functions>
    <env> bind("depth", IVal(0), _REST0:Store) => ?_FINALENV:Store </env>
    <result> noResult() => result(BVal(bracketSeqSpec(BS, 0))) </result>
  </py>

  claim [loop-positive]: <py>
    <k>
      forBracketSeq(BS, "bracket", targetLoopBody()) ~> targetTail() ~> functionBoundary()
      => .K
    </k>
    <functions> _FMP:Map => ?_FM:Map </functions>
    <env> bind("depth", IVal(D), _RESTP:Store) => ?_FINALENV:Store </env>
    <result>
      noResult() => result(BVal(bracketSeqSpec(BS, D)))
    </result>
  </py>
    requires D >Int 0

  // Deliberately false result mutation: the original universal result was
  // bracketSeqSpec(BS, 0). This demands false for every BS. The satisfying
  // witness BS=noBrackets() corresponds to input "", whose real result is true.
  claim [false-universal-result]: <py>
    <k>
      correctProgram() ~> invoke("correct_bracketing", SeqVal(BS))
      => .K
    </k>
    <functions> .Map => ?_UFM:Map </functions>
    <env> emptyStore() => ?_UENV:Store </env>
    <result> noResult() => result(BVal(false)) </result>
  </py>
endmodule
