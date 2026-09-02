requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A reusable spelling of the exact solution.mpy term, used only by the
  // negative proof probe.  The positive universal theorem spells it out.
  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("do_algebra", Params("operator", "operand"),
        Assign(
          Name("expression"),
          Call(Name("str"), Subscript(Name("operand"), Int(0))))
        For(TupleExpr(Name("oprt"), Name("oprn")), Call(
          Name("zip"),
          Name("operator"),
          Subscript(Name("operand"), Slice(Int(1), NoBound, NoBound))),
          AugAssign(
            Name("expression"),
            "+",
            BinOp("+", Name("oprt"),
                  Call(Name("str"), Name("oprn")))))
        Return(Call(Name("eval"), Name("expression")))))

  // The postcondition names the independently visible mathematical result.
  // pyEval is the precedence evaluator defined by the semantics; expected is
  // deliberately kept in the verification layer so specifications never
  // mention an implementation cell or continuation.
  syntax Int ::= expected ( Ops , Ints ) [function]
  rule expected(OS, IS) => pyEval(OS, IS)

  // A one-step proof harness keeps concrete evaluator claims as reachability
  // claims (rather than backend-unsupported bare functional claims).
  syntax KItem ::= "check" "(" Int ")" | "checked" "(" Int ")"
  rule check(I) => checked(I)

  syntax Bool ::= validOps ( Ops ) [function, total]
  rule validOps(.Ops) => true
  rule validOps(Op(O, OS)) => validOperator(O) andBool validOps(OS)

  syntax Bool ::= validOperator ( String ) [function, total]
  rule validOperator("+") => true
  rule validOperator("-") => true
  rule validOperator("*") => true
  rule validOperator("//") => true
  rule validOperator("**") => true
  rule validOperator(O) => false
    requires O =/=String "+"
     andBool O =/=String "-"
     andBool O =/=String "*"
     andBool O =/=String "//"
     andBool O =/=String "**"

  syntax Bool ::= nonNegative ( Ints ) [function, total]
  rule nonNegative(.Ints) => true
  rule nonNegative(Num(I, IS))
    => (I >=Int 0) andBool nonNegative(IS)
endmodule
