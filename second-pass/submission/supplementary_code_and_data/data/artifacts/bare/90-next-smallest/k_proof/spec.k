requires "verification.k"

module SPEC
  imports VERIFICATION

  // For every finite list of mathematical integers, executing the translated
  // implementation terminates with the declarative second-smallest result.
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
      <result> noResult => secondSmallest(L) </result>
    </mpy>
    [label(next-smallest-correct)]
endmodule
