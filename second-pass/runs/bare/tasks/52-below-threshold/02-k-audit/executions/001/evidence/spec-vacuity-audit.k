requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim [loop-invariant-for-vacuity]:
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
      <result> noResult => result(allBelow(XS, T)) </result>
    </bt>

  // Deliberately false result mutation: the real claim has
  // result(allBelow(XS,T)). For XS=nil, allBelow is true, not false.
  claim [false-result-mutation]:
    <bt>
      <k> boot => .K </k>
      <program> solutionProgram </program>
      <input> XS:IntSeq </input>
      <threshold> T:Int </threshold>
      <l> unbound => slot(VList(XS)) </l>
      <t> unbound => slot(VInt(T)) </t>
      <x> unbound => ?_FINAL_X:Slot </x>
      <result> noResult => result(false) </result>
    </bt>
endmodule
