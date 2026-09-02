requires "reference-semantics/semantics.k"

module VERIFICATION-NOBRIDGES
  imports MPY

  syntax IntSeq ::= decimalCodes(Int)
                  | fruitSentenceCodes(Int, Int)

  syntax Module ::= "solutionModule" [function, total]
  rule solutionModule =>
    Module(
      FuncDef("fruit_distribution", Params("s", "n"),
        Assign(
          Name("fruits"),
          Call(Attribute(Name("s"), "split"), .Exprs))
        Return(
          BinOp(
            "-",
            BinOp(
              "-",
              Name("n"),
              Call(
                Name("int"),
                Subscript(Name("fruits"), Int(0)), .Exprs)),
            Call(
              Name("int"),
              Subscript(Name("fruits"), Int(3)), .Exprs)))))
endmodule
