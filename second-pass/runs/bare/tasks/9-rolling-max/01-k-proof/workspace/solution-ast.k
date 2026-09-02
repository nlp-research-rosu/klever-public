requires "semantic.k"

module SOLUTION-AST
  imports MPY

  // Value-level operational harness used by proofs.  Run in semantic.k is
  // the corresponding concrete parser harness for command-line examples.
  syntax Program ::= OpRunList(Module, List)
  rule <k> OpRunList(M, XS)
        => M ~> Invoke("rolling_max", ListVal(XS)) ~> Cleanup ... </k>

  // Constructor-for-constructor transcription of solution.mpy.
  syntax Stmts ::= "ROLLING-LOOP" [macro]
  rule ROLLING-LOOP =>
    If(Name("first"),
      Assign(Name("maximum"), Name("number"))
      Assign(Name("first"), Bool(false)),
      If(Compare(Name("number"), CmpOp(">", Name("maximum"))),
        Assign(Name("maximum"), Name("number")),
        .Stmts))
    Expr(Call(Attribute(Name("result"), "append"), Name("maximum")))

  syntax Stmts ::= "ROLLING-BODY" [macro]
  rule ROLLING-BODY =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("first"), Bool(true))
    Assign(Name("maximum"), Int(0))
    For(Name("number"), Name("numbers"), ROLLING-LOOP)
    Return(Name("result"))

  syntax Module ::= "SOLUTION" [macro]
  rule SOLUTION => Module(
    ImportFrom("typing", "List", "Tuple")
    FuncDef("rolling_max", Params("numbers"), ROLLING-BODY))

  // Independent mathematical specification: emit the head, then scan the
  // tail while carrying the largest integer observed so far.
  syntax List ::= "#rollingMax" "(" List ")" [function]
                | "#scanMax" "(" Int "," List ")" [function]

  rule #rollingMax(.List) => .List
  rule #rollingMax(ListItem(I:Int) REST) => ListItem(I) #scanMax(I, REST)

  rule #scanMax(_, .List) => .List
  rule #scanMax(M, ListItem(I:Int) REST)
    => ListItem(I) #scanMax(I, REST)
    requires I >Int M
  rule #scanMax(M, ListItem(I:Int) REST)
    => ListItem(M) #scanMax(M, REST)
    requires notBool(I >Int M)
endmodule
