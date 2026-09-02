module VERIFICATION
  imports MPY

  // A mathematical, accumulator-based definition of stable prefix filtering.
  // It is independent of environments, statements, and all control machinery.
  syntax StrList ::= filterAcc(StrList, String, StrList) [function]
                   | filterByPrefix(StrList, String) [function]

  rule filterByPrefix(INPUT, PREFIX) => filterAcc(INPUT, PREFIX, nil)
  rule filterAcc(nil, _, ACC) => ACC
  rule filterAcc(cons(S, REST), PREFIX, ACC) =>
    filterAcc(REST, PREFIX, appendOne(ACC, S))
    requires startsWith(S, PREFIX) ==Bool true [simplification]
  rule filterAcc(cons(S, REST), PREFIX, ACC) =>
    filterAcc(REST, PREFIX, ACC)
    requires startsWith(S, PREFIX) ==Bool false [simplification]

  // Canonical syntax trees used by the proof.  solutionProgram is exactly the
  // term emitted in solution.mpy (SHA-256 7d10644743b0d635231400e73ff58c5755e17dd09b7a73f64b79fd8fa0a12269,
  // checked by prove.sh); loopBody is its for-loop body.
  syntax Stmts ::= loopBody() [function]
  syntax Module ::= solutionProgram() [function]

  rule loopBody() =>
    Expr(Call(Attribute(Name("result"), "append"), Name("string"))) .Stmts

  rule solutionProgram() =>
    Module(
      ImportFrom("typing", "List", .Strings)
      FuncDef("filter_by_prefix", Params("strings", "prefix", .Strings),
        Assign(Name("result"), ListExpr())
        For(Name("string"), Name("strings"), loopBody())
        Return(Name("result"))))
endmodule
