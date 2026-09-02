requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim
    <k>
      solutionModule =>
      Module(
        FuncDef("fruit_distribution", Params("s", "n"),
          Assign(Name("fruits"), Call(Attribute(Name("s"), "split"), .Exprs))
          Return(
            BinOp(
              "-",
              BinOp(
                "-",
                Name("n"),
                Call(Name("int"), Subscript(Name("fruits"), Int(0)), .Exprs)),
              Call(Name("int"), Subscript(Name("fruits"), Int(3)), .Exprs)))))
    </k>
endmodule
