requires "bridge-definition.k"

module SPEC-ACTUAL-STRING-ATTEMPT
  imports BRIDGE-DEFINITION

  // The candidate's two submitted circularities are retained unchanged.
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

  // This is the missing real-string theorem: it invokes the submitted body
  // with SVal(String), using an injective constructor renderer for [<>]*.
  claim [actual-string-universal]: <py>
    <k>
      correctProgram()
      ~> invoke(
           "correct_bracketing",
           SVal(bracketSeqString(BS)))
      => .K
    </k>
    <functions> .Map => ?_UFM:Map </functions>
    <env> emptyStore() => ?_UENV:Store </env>
    <result> noResult() => result(BVal(bracketSeqSpec(BS, 0))) </result>
  </py>
endmodule
