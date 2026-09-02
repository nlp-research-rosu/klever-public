requires "semantic.k"

module SPEC-AUDIT
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

  claim [universal-correctness]: <py>
    <k>
      correctProgram() ~> invoke("correct_bracketing", SeqVal(BS))
      => .K
    </k>
    <functions> .Map => ?_UFM:Map </functions>
    <env> emptyStore() => ?_UENV:Store </env>
    <result> noResult() => result(BVal(bracketSeqSpec(BS, 0))) </result>
  </py>

  claim [example-single-open]: <py>
    <k> correctProgram() ~> invoke("correct_bracketing", SVal("<")) => .K </k>
    <functions> .Map => ?_FM1:Map </functions>
    <env> emptyStore() => ?_ENV1:Store </env>
    <result> noResult() => result(BVal(false)) </result>
  </py>

  claim [example-pair]: <py>
    <k> correctProgram() ~> invoke("correct_bracketing", SVal("<>")) => .K </k>
    <functions> .Map => ?_FM2:Map </functions>
    <env> emptyStore() => ?_ENV2:Store </env>
    <result> noResult() => result(BVal(true)) </result>
  </py>

  claim [example-nested]: <py>
    <k> correctProgram() ~> invoke("correct_bracketing", SVal("<<><>>")) => .K </k>
    <functions> .Map => ?_FM3:Map </functions>
    <env> emptyStore() => ?_ENV3:Store </env>
    <result> noResult() => result(BVal(true)) </result>
  </py>

  claim [example-negative-prefix]: <py>
    <k> correctProgram() ~> invoke("correct_bracketing", SVal("><<>")) => .K </k>
    <functions> .Map => ?_FM4:Map </functions>
    <env> emptyStore() => ?_ENV4:Store </env>
    <result> noResult() => result(BVal(false)) </result>
  </py>
endmodule
