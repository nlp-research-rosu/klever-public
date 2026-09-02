requires "verification.k"

module XOR-BODY-SENSITIVITY
  imports XOR-VERIFICATION

  // Exact submitted program term except the final unequal-bit literal is
  // mutated from "1" to "0". For inputs "0" and "1", the original expected
  // result "1" must therefore be rejected.
  claim [mutated-body-rejects-original-result]:
    <k>
      Module(
        FuncDef("string_xor", Params("a", "b"),
          If(Compare(Name("a"), CmpOp("==", Str(""))),
            Return(Str("")),
            .Stmts)
          If(Compare(Name("b"), CmpOp("==", Str(""))),
            Return(Str("")),
            .Stmts)
          If(Compare(
            Subscript(Name("a"), Int(0)),
            CmpOp("==", Subscript(Name("b"), Int(0)))),
            Return(
              BinOp(
                "+",
                Str("0"),
                Call(
                  Name("string_xor"),
                  Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
                  Subscript(Name("b"), Slice(Int(1), NoBound, NoBound))))),
            .Stmts)
          Return(
            BinOp(
              "+",
              Str("0"),
              Call(
                Name("string_xor"),
                Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
                Subscript(Name("b"), Slice(Int(1), NoBound, NoBound)))))))
      => returned(str(cons(true, empty))) ... </k>
    <args>
      Args(str(segment(1, seed(0))), str(segment(1, seed(1))))
    </args>
endmodule
