requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Fresh false-result mutation. The precondition is unchanged, but this
  // claims every input returns None. Satisfying witness [1,2] actually returns
  // 2 in both Python implementations and the rebuilt concrete K semantics.
  claim
    <mpy>
      <k>
        Module(
          FuncDef("next_smallest", Params("lst"),
            Assign(Name("distinct"),
              Call(Name("sorted"), Call(Name("set"), Name("lst"))))
            Return(
              IfExp(
                Compare(Call(Name("len"), Name("distinct")),
                        CmpOp(">", Int(1))),
                Subscript(Name("distinct"), Int(1)),
                NoneVal))))
        => .K
      </k>
      <input> L:IntList </input>
      <distinct> none => pyList(uniqueSort(L)) </distinct>
      <result> noResult => none </result>
    </mpy>
    [label(false-all-none)]
endmodule
