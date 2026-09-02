requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  syntax Program ::= "Verify" "(" PString ")"
                   | "VerifyDrop" "(" PString ")"

  rule <k> Verify(S) => call("fix_spaces", pyStr(S)) </k>
       <funs> .Funs => solutionFuns </funs>
  rule <k> VerifyDrop(S) => call("_drop_spaces", pyStr(S)) </k>
       <funs> .Funs => solutionFuns </funs>

  // This is the exact constructor tree emitted in solution.mpy.  Keeping it
  // here as data lets the claims call the ordinary interpreter on symbolic
  // arguments; there is no special semantic rule for fix_spaces.
  syntax Funs ::= "solutionFuns" [function]
  rule solutionFuns => collect(
    FuncDef("_drop_spaces", Params("text"),
      If(Compare(Name("text"), CmpOp("==", Str(""))),
        Return(Str("")),
        .Stmts)
      If(Compare(Subscript(Name("text"), Int(0)), CmpOp("==", Str(" "))),
        Return(Call(Name("_drop_spaces"),
          Subscript(Name("text"), Slice(Int(1), NoBound, NoBound)))),
        .Stmts)
      Return(Call(Name("fix_spaces"), Name("text"))))
    FuncDef("fix_spaces", Params("text"),
      If(Compare(Name("text"), CmpOp("==", Str(""))),
        Return(Str("")),
        .Stmts)
      If(Compare(Subscript(Name("text"), Int(0)), CmpOp("==", Str(" "))),
        If(Compare(Call(Name("len"), Name("text")), CmpOp(">", Int(2))),
          If(Compare(
              Subscript(Name("text"), Slice(Int(0), Int(3), NoBound)),
              CmpOp("==", Str("   "))),
            Return(BinOp("+", Str("-"),
              Call(Name("_drop_spaces"),
                Subscript(Name("text"), Slice(Int(3), NoBound, NoBound))))),
            .Stmts),
          .Stmts)
        Return(BinOp("+", Str("_"),
          Call(Name("fix_spaces"),
            Subscript(Name("text"), Slice(Int(1), NoBound, NoBound))))),
        .Stmts)
      Return(BinOp("+", Subscript(Name("text"), Int(0)),
        Call(Name("fix_spaces"),
          Subscript(Name("text"), Slice(Int(1), NoBound, NoBound))))))
  )

  // Independent structural statement of the prompt's contract.  Runs of one
  // or two spaces become underscores; a run beginning with at least three
  // spaces emits one hyphen and dropRef consumes the remainder of that run.
  syntax PString ::= fixRef(PString) [function]
  rule fixRef(.PString) => .PString
  rule fixRef(ch(C) REST) => ch(C) fixRef(REST)
  rule fixRef(sp .PString) => ch("_") .PString
  rule fixRef(sp ch(C) REST) => ch("_") ch(C) fixRef(REST)
  rule fixRef(sp sp .PString) => ch("_") ch("_") .PString
  rule fixRef(sp sp ch(C) REST) => ch("_") ch("_") ch(C) fixRef(REST)
  rule fixRef(sp sp sp REST) => ch("-") dropRef(REST)

  syntax PString ::= dropRef(PString) [function]
  rule dropRef(.PString) => .PString
  rule dropRef(sp REST) => dropRef(REST)
  rule dropRef(ch(C) REST) => ch(C) fixRef(REST)
endmodule
