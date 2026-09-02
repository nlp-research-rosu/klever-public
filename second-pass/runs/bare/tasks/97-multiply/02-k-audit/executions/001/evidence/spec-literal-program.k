requires "verification.k"

module AUDIT-LITERAL-PROGRAM-SPEC
  imports VERIFICATION

  // Reviewer-authored pinning check: the complete constructor term below is
  // byte-for-byte the AST represented by submitted solution.mpy, with neither
  // multiplyProgram nor multiplyBody used in the entry or destination.
  claim
    <task>
      <k>
        Module(
          FuncDef("multiply", Params("a", "b"),
            If(Compare(Name("a"), CmpOp("<", Int(0))),
              Assign(Name("a"), UnaryOp("-", Name("a"))),
              .Stmts)
            If(Compare(Name("b"), CmpOp("<", Int(0))),
              Assign(Name("b"), UnaryOp("-", Name("b"))),
              .Stmts)
            Return(
              BinOp(
                "*",
                BinOp("%", Name("a"), Int(10)),
                BinOp("%", Name("b"), Int(10))))))
        ~> #invoke("multiply", A, B)
        => .K
      </k>
      <env> .Map => ("a" |-> absInt(A)) ("b" |-> absInt(B)) </env>
      <functions>
        .Map =>
          "multiply" |->
            function("a", "b",
              If(Compare(Name("a"), CmpOp("<", Int(0))),
                Assign(Name("a"), UnaryOp("-", Name("a"))),
                .Stmts)
              If(Compare(Name("b"), CmpOp("<", Int(0))),
                Assign(Name("b"), UnaryOp("-", Name("b"))),
                .Stmts)
              Return(
                BinOp(
                  "*",
                  BinOp("%", Name("a"), Int(10)),
                  BinOp("%", Name("b"), Int(10)))))
      </functions>
      <result>
        noResult => unitDigit(A) *Int unitDigit(B)
      </result>
    </task>
endmodule
