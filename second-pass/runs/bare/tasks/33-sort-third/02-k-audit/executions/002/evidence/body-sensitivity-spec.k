requires "verification.k"

module BODY-SENSITIVITY
  imports VERIFICATION

  // Reviewer mutation: remove the slice-sorting assignment from the term
  // actually executed by the claim, but retain the original expected result.
  claim [body-mutated]:
    <k>
      Module(
        FuncDef("sort_third", Params("l"),
          Assign(Name("result"),
            Subscript(Name("l"), Slice(NoBound, NoBound, NoBound)))
          Return(Name("result"))))
      => .K
    </k>
    <input> VList(5, 6, 3, 4, 8, 9, 2) </input>
    <result> .K => VList(2, 6, 3, 4, 8, 9, 5) </result>
endmodule
