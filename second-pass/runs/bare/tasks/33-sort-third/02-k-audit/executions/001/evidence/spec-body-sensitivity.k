requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Deliberate body mutation: return the untouched parameter instead of result.
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
          Return(Name("l"))))
      => .K
    </k>
    <input> VList(5, 6, 3, 4, 8, 9, 2) </input>
    <result> .K => VList(2, 6, 3, 4, 8, 9, 5) </result>
endmodule
