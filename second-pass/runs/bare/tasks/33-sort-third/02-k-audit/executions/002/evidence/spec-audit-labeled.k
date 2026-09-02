requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  claim [audit-universal]:
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
    <input> VList(IS:Ints) </input>
    <result> .K => contractResult(IS) </result>

  claim [audit-example-2]:
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
    <result> .K => VList(2, 6, 3, 4, 8, 9, 5) </result>

  claim [audit-example-1]:
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
