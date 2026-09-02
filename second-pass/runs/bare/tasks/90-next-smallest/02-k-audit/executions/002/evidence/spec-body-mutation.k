requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: the submitted body indexes 1; this deliberately
  // changes the executed program term to index 0 while retaining the original
  // result obligation. Witness L = cons(1, cons(2, nil)) returns 1, not 2.
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
      <input> L:IntList </input>
      <distinct> none => pyList(uniqueSort(L)) </distinct>
      <result> noResult => secondSmallest(L) </result>
    </mpy>
    [label(body-change-should-not-prove)]
endmodule
