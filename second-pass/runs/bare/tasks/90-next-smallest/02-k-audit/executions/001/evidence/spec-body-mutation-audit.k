requires "verification.k"

module SPEC-BODY-MUTATION-AUDIT
  imports VERIFICATION

  // Operational-sensitivity check: change the executed index from 1 to 0
  // while retaining the original second-smallest postcondition on [1,2].
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
                Subscript(Name("distinct"), Int(0)),
                NoneVal))))
        => .K
      </k>
      <input> cons(1, cons(2, nil)) </input>
      <distinct> none => pyList(uniqueSort(cons(1, cons(2, nil)))) </distinct>
      <result>
        noResult => secondSmallest(cons(1, cons(2, nil)))
      </result>
    </mpy>
    [label(index-body-sensitivity)]
endmodule
