requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop invariant.  If the suffix XS remains to be scanned, the
  // eventual answer is exactly the mathematical predicate on that suffix.
  claim [loop-invariant]:
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

  claim [below-threshold-correct]:
    <bt>
      <k> boot => .K </k>
      <program> solutionProgram </program>
      <input> XS:IntSeq </input>
      <threshold> T:Int </threshold>
      <l> unbound => slot(VList(XS)) </l>
      <t> unbound => slot(VInt(T)) </t>
      <x> unbound => ?_FINAL_X:Slot </x>
      <result> noResult => result(allBelow(XS, T)) </result>
    </bt>
endmodule
