requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Named syntax for the exact translated submission and its loop body.  These
  // equations make the proof readable while still reducing to py2mpy constructors.
  syntax Stmts ::= "solutionLoopBody" [function]
  syntax AST ::= "solutionAST" [function]

  rule solutionLoopBody =>
    Assign(
      Name("count"),
      Int(0))
    If(Compare(Name("count"), CmpOp(">", Name("best_count"))),
      Assign(Name("best"), Name("word"))
      Assign(Name("best_count"), Name("count")),
      .Stmts)
    If(Compare(Name("count"), CmpOp("==", Name("best_count"))),
      If(Compare(Name("word"), CmpOp("<", Name("best"))),
        Assign(Name("best"), Name("word")),
        .Stmts),
      .Stmts)

  rule solutionAST =>
    Module(
      FuncDef("find_max", Params("words"),
        Assign(Name("best"), Str(""))
        Assign(Name("best_count"), UnaryOp("-", Int(1)))
        For(Name("word"), Name("words"), solutionLoopBody)
        Return(Name("best"))))

  // Independent executable contract: fold the input from left to right,
  // retaining the higher distinct-character count and breaking ties by String.<.
  syntax Candidate ::= "candidate" "(" String "," Int ")"
  syntax Candidate ::= "consider" "(" String "," Candidate ")" [function]
  syntax Candidate ::= "maxCandidate" "(" Words "," Candidate ")" [function]
  syntax String ::= "candidateWord" "(" Candidate ")" [function]
  syntax String ::= "findMaxSpec" "(" Words ")" [function]

  rule consider(W, candidate(_B, C))
    => candidate(W, distinctCount(W))
    requires distinctCount(W) >Int C
  rule consider(W, candidate(B, C))
    => candidate(W, C)
    requires distinctCount(W) <=Int C
     andBool distinctCount(W) ==Int C
     andBool W <String B
  rule consider(W, candidate(B, C))
    => candidate(B, C)
    requires distinctCount(W) <=Int C
     andBool (distinctCount(W) =/=Int C orBool notBool (W <String B))

  rule maxCandidate(nil, C) => C
  rule maxCandidate(cons(W, REST), C)
    => maxCandidate(REST, consider(W, C))

  rule candidateWord(candidate(W, _)) => W
  rule findMaxSpec(WORDS)
    => candidateWord(maxCandidate(WORDS, candidate("", -1)))
endmodule
