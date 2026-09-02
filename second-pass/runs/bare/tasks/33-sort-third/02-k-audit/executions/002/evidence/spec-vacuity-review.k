requires "verification.k"

module SPEC-VACUITY-REVIEW
  imports VERIFICATION

  // Fresh reviewer mutation: the program and satisfiable input are unchanged,
  // but the required returned list is deliberately the unsorted input.
  claim [false-result]:
    <k>
      Module(
        FuncDef("sort_third", Params("l"),
          Assign(Name("result"),
            Subscript(Name("l"), Slice(NoBound, NoBound, NoBound)))
          Assign(
            Subscript(Name("result"), Slice(NoBound, NoBound, Int(3))),
            Call(Name("sorted"),
              Subscript(Name("result"), Slice(NoBound, NoBound, Int(3)))))
          Return(Name("result"))))
      => .K
    </k>
    <input> VList(5, 6, 3, 4, 8, 9, 2) </input>
    <result> .K => VList(5, 6, 3, 4, 8, 9, 2) </result>
endmodule
