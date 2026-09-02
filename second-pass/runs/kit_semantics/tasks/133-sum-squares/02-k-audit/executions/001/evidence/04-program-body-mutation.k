requires "reference-semantics/semantics/syntax.k"

module SOLUTION-PROGRAM
  imports MPY-SYNTAX

  // This nullary AST constant is checked mechanically against solution.mpy by
  // check_program_identity.py before compilation.
  syntax Module ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      Import("math")
      FuncDef("sum_squares", Params("lst"),
        Assign(Name("total"), Int(1))
        Assign(Name("number"), Int(0))
        Assign(Name("rounded"), Int(0))
        For(Name("number"), Name("lst"),
          Assign(
            Name("rounded"),
            Call(Attribute(Name("math"), "ceil"), Name("number")))
          AugAssign(
            Name("total"),
            "+",
            BinOp("*", Name("rounded"), Name("rounded"))))
        Return(Name("total"))))
endmodule
