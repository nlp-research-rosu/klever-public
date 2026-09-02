requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTIC

  // These constructor constants are an exact transcription of solution.mpy.
  syntax Exprs ::= "solutionPrimes" [function]
  rule solutionPrimes =>
       Int(4), Int(3), Int(5), Int(7), Int(11), Int(13), Int(17), Int(19),
       Int(23), Int(29), Int(31), Int(37), Int(41), Int(43), Int(47),
       Int(53), Int(59), Int(61), Int(67), Int(71), Int(73), Int(79),
       Int(83), Int(89), Int(97)

  syntax Stmts ::= "solutionLoopBody" [function]
  rule solutionLoopBody =>
       If(Compare(Call(Name("len"), Name("word")),
                  CmpOp("in", ListExpr(solutionPrimes))),
          If(Compare(Name("result"), CmpOp("==", Str(""))),
             Assign(Name("result"), Name("word")),
             Assign(Name("result"),
                    BinOp("+", BinOp("+", Name("result"), Str(" ")),
                          Name("word")))),
          .Stmts)

  syntax Stmts ::= "solutionBody" [function]
  rule solutionBody =>
       Assign(Name("result"), Str(""))
       Assign(Name("word"), Str(""))
       For(Name("word"),
           Call(Attribute(Name("sentence"), "split"), Str(" ")),
           solutionLoopBody)
       Return(Name("result"))

  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
       Module(FuncDef("words_in_sentence", Params("sentence"), solutionBody))

  // An independent contract copy of the finite prime characterization.  It
  // is deliberately distinct from solutionPrimes, which transcribes the
  // implementation AST.  Since the whole sentence is at most 100 characters,
  // these are exactly all possible prime word lengths.
  syntax Exprs ::= "contractPrimes" [function]
  rule contractPrimes =>
       Int(2), Int(3), Int(5), Int(7), Int(11), Int(13), Int(17), Int(19),
       Int(23), Int(29), Int(31), Int(37), Int(41), Int(43), Int(47),
       Int(53), Int(59), Int(61), Int(67), Int(71), Int(73), Int(79),
       Int(83), Int(89), Int(97)

  syntax Bool ::= "primeLength" "(" Int ")" [function, total]
  rule primeLength(N) => memberInt(N, contractPrimes)

  syntax String ::= "appendSelected" "(" String "," String ")" [function, total]
  rule appendSelected(A, W) =>
       conditionalAppend(primeLength(lengthString(W)), A, W)

  syntax String ::= "selectedWords" "(" WordSeq "," String ")" [function, total]
  rule selectedWords(WNil, A) => A
  rule selectedWords(WCons(W, WS), A) =>
       selectedWords(WS, appendSelected(A, W))

  // A denotational account of the loop's store transformation.  It is
  // separate from the small-step rules in semantic.k and is used as the
  // invariant's target.
  syntax Map ::= "loopEnv" "(" WordSeq "," Map ")" [function]
  syntax Map ::= "wordEnv" "(" WordSeq "," Map ")" [function, total]
  rule wordEnv(WNil, RHO) => RHO
  rule wordEnv(WCons(W, WS), "word" |-> Str(_OLD) RHO) =>
       wordEnv(WS, "word" |-> Str(W) RHO)
    requires notBool ("word" in_keys(RHO))
  rule loopEnv(WS, "result" |-> Str(A) RHO) =>
       "result" |-> Str(selectedWords(WS, A)) wordEnv(WS, RHO)
    requires notBool ("result" in_keys(RHO))

  syntax KItem ::= "finishProgram"
  rule <k> finishProgram => .K ... </k>
       <functions> _ => .Map </functions>
       <env> _ => .Map </env>

  // Utilities for stating the input model (nonempty, space-free words).
  syntax Bool ::= "wellFormedWords" "(" WordSeq ")" [function]
  rule wellFormedWords(WNil) => true
  rule wellFormedWords(WCons(W, WS)) =>
       (lengthString(W) >Int 0 andBool findString(W, " ", 0) ==Int -1)
       andBool wellFormedWords(WS)

  syntax String ::= "renderWords" "(" WordSeq ")" [function]
  rule renderWords(WNil) => ""
  rule renderWords(WCons(W, WNil)) => W
  rule renderWords(WCons(W, WCons(W2, WS))) =>
       W +String " " +String renderWords(WCons(W2, WS))
endmodule
