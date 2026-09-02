requires "verification.k"

module SPEC-CLAIM-EXAMPLE-THREE
  imports VERIFICATION

  claim
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
    <input> VList(1, 2, 3) </input>
    <result> .K => VList(1, 2, 3) </result>
endmodule
