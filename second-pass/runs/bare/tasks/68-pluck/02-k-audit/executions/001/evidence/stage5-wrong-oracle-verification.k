requires "semantic.k"

module WRONG-ORACLE-VERIFICATION
  imports SEMANTIC

  // Opposite interpretation witness: semantic.k leaves minEvenArray wholly
  // unconstrained, so K accepts this deliberately false completion too.
  rule minEvenArray(_ID, _OFFSET, _LENGTH) => VList(.Ints)

  // Exact constructor form generated in the submitted solution.mpy.
  syntax Stmts ::= "witnessPluckBody" [function, total]
  syntax Program ::= "witnessSolutionProgram" [function, total]
  syntax Map ::= "witnessSolutionFunctions" [function, total]

  rule witnessPluckBody =>
    Return(Call(
      Name("min"),
      ListComp(
        ListExpr(Name("value"), Name("index")),
        CompFor(
          TupleExpr(Name("index"), Name("value")),
          Call(Name("enumerate"), Name("arr")),
          Compare(
            BinOp("%", Name("value"), Int(2)),
            CmpOp("==", Int(0))))),
      KwArg("default", ListExpr(.Exprs))))

  rule witnessSolutionProgram =>
    Module(FuncDef("pluck", Params("arr"), witnessPluckBody))

  rule witnessSolutionFunctions =>
    "pluck" |-> fun(Params("arr"), witnessPluckBody)
endmodule
