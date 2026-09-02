requires "verification.k"

module SPEC-VACUITY-LOOP
  imports VERIFICATION

  // Deliberately false at XS = nil, INPUT = nil, T = 0, x = unbound:
  // execution returns true, while this destination requires false.
  claim [false-loop-invariant]:
    <bt>
      <k>
        loop(Name("x"), XS:IntSeq,
          If(Compare(Name("x"), CmpOp(">=", Name("t"))),
            Return(Bool(false)),
            .Stmts))
        ~> exec(Return(Bool(true)) .Stmts)
        => .K
      </k>
      <program> solutionProgram </program>
      <input> INPUT:IntSeq </input>
      <threshold> T:Int </threshold>
      <l> slot(VList(INPUT)) </l>
      <t> slot(VInt(T)) </t>
      <x> _INITIAL_X:Slot => ?_FINAL_LOOP_X:Slot </x>
      <result>
        noResult => result(notBool allBelow(XS, T))
      </result>
    </bt>
endmodule
