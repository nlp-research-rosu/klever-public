requires "reference-semantics/semantics.k"

module FILTER-VERIFICATION
  imports MPY

  // A typed symbolic sequence: every element denotes a Python string.
  syntax StrSeq ::= ".StrSeq"
                  | ssCons(IntSeq, StrSeq)

  // strVals is a proof-side representation constructor.  The iterator bridge
  // below exposes exactly the same head/tail behavior as vCons(str(...), ...).
  syntax ValSeq ::= strVals(StrSeq)
  rule strVals(.StrSeq) => .ValSeq
  rule strVals(ssCons(S:IntSeq, SS:StrSeq))
    => vCons(str(S), strVals(SS))

  syntax KItem ::= #strIterNext(StrSeq)
  rule <k> #iterNext(list(strVals(SS:StrSeq)))
        => #strIterNext(SS) ... </k>
    [priority(40)]
  rule <k> #strIterNext(.StrSeq) => #iterDone ... </k>
  rule <k> #strIterNext(ssCons(S:IntSeq, SS:StrSeq))
        => #iterYield(str(S), list(strVals(SS))) ... </k>

  // Split symbolic string containment while retaining the reference function.
  syntax KItem ::= #strContainsBool(IntSeq, IntSeq)
  rule <k> Compare(str(P:IntSeq), CmpOp("in", str(S:IntSeq)))
        => #strContainsBool(P, S) ... </k>
    [priority(40)]
  rule <k> #strContainsBool(P:IntSeq, S:IntSeq) => true ... </k>
    requires strContains(P, S) ==Bool true
  rule <k> #strContainsBool(P:IntSeq, S:IntSeq) => false ... </k>
    requires strContains(P, S) ==Bool false

  // Mathematical contract in accumulator form: inspect each string once,
  // append it exactly when it contains P, and otherwise leave ACC unchanged.
  syntax ValSeq ::= filterAccStrings(ValSeq, IntSeq, StrSeq) [function, total]
  rule filterAccStrings(ACC:ValSeq, _:IntSeq, .StrSeq) => ACC
  rule filterAccStrings(ACC:ValSeq, P:IntSeq,
                        ssCons(S:IntSeq, SS:StrSeq))
    => filterAccStrings(valSeqConcat(ACC, vCons(str(S), .ValSeq)), P, SS)
    requires strContains(P, S) ==Bool true
    [simplification]
  rule filterAccStrings(ACC:ValSeq, P:IntSeq,
                        ssCons(S:IntSeq, SS:StrSeq))
    => filterAccStrings(ACC, P, SS)
    requires strContains(P, S) ==Bool false
    [simplification]

  syntax ValSeq ::= filterStrings(IntSeq, StrSeq) [function, total]
  rule filterStrings(P:IntSeq, SS:StrSeq)
    => filterAccStrings(.ValSeq, P, SS)

  syntax IntSeq ::= lastCodes(IntSeq, StrSeq) [function, total]
  rule lastCodes(S:IntSeq, .StrSeq) => S
  rule lastCodes(_:IntSeq, ssCons(S:IntSeq, SS:StrSeq))
    => lastCodes(S, SS)

  // These macros are the exact translated function body in solution.mpy.
  syntax Stmts ::= "filterLoopBody" [macro]
  rule filterLoopBody
    => If(Compare(Name("substring"), CmpOp("in", Name("string"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("string"))) .Stmts,
          .Stmts)

  syntax Stmts ::= "filterBody" [macro]
  rule filterBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("string"), Name("strings"), filterLoopBody)
       Return(Name("result"))

  syntax Module ::= "filterProgram" [macro]
  rule filterProgram
    => Module(ImportFrom("typing", "List")
              FuncDef("filter_by_substring", Params("strings", "substring"),
                      filterBody))
endmodule
