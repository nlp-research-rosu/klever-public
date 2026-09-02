requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation. The concrete input [1,2] satisfies the original
  // entry domain, but the real and K executions return 2, not none.
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
      <input> cons(1, cons(2, nil)) </input>
      <distinct> none => pyList(uniqueSort(cons(1, cons(2, nil)))) </distinct>
      <result> noResult => none </result>
    </mpy>
    [label(false-always-none-on-one-two)]
endmodule
