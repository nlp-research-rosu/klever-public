requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE

  // Exact AST fragments generated from solution.py.  These are names for
  // syntax trees; they do not replace any operational step.
  syntax Stmts ::= "charLoopBody" [function, total]
                 | "afterCharLoop" [function, total]
                 | "selectWordsBody" [function, total]

  // Mathematical specification: scan the remaining character codes while
  // carrying the current word, its consonant count, and the selected words.
  syntax ValSeq ::= selectScan(IntSeq, Int, IntSeq, Int, ValSeq)
                    [function, total]
                  | scanAccum(IntSeq, Int, IntSeq, Int, ValSeq)
                    [function, total]
                  | flushSelected(ValSeq, IntSeq, Int, Int)
                    [function, total]

  syntax IntSeq ::= wordAfter(IntSeq, IntSeq) [function, total]
                  | charAfter(IntSeq, IntSeq) [function, total]
  syntax Int ::= countAfter(IntSeq, Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule charLoopBody =>
    If(Compare(Name("ch"), CmpOp("==", Str(" "))),
      If(BoolOp("and",
           Compare(Name("count"), CmpOp("==", Name("n"))),
           Compare(Name("word"), CmpOp("!=", Str("")))),
        Expr(Call(Attribute(Name("result"), "append"), Name("word")))
        .Stmts,
        .Stmts)
      Assign(Name("word"), Str(""))
      Assign(Name("count"), Int(0))
      .Stmts,
      Assign(Name("word"), BinOp("+", Name("word"), Name("ch")))
      If(Compare(Name("ch"), CmpOp("not in", Str("aeiouAEIOU"))),
        Assign(Name("count"),
          BinOp("+", Name("count"), Int(1)))
        .Stmts,
        .Stmts)
      .Stmts)
    .Stmts

  rule afterCharLoop =>
    If(BoolOp("and",
         Compare(Name("count"), CmpOp("==", Name("n"))),
         Compare(Name("word"), CmpOp("!=", Str("")))),
      Expr(Call(Attribute(Name("result"), "append"), Name("word")))
      .Stmts,
      .Stmts)
    Return(Name("result"))
    .Stmts

  rule selectWordsBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("word"), Str(""))
    Assign(Name("count"), Int(0))
    Assign(Name("ch"), Str(""))
    For(Name("ch"), Name("s"), charLoopBody)
    afterCharLoop

  // Flush never selects an empty token, including when n == 0.
  rule flushSelected(A:ValSeq, _WORD:IntSeq, COUNT:Int, N:Int) => A
    requires COUNT =/=Int N
    [simplification]
  rule flushSelected(A:ValSeq, .IntSeq, COUNT:Int, N:Int) => A
    requires COUNT ==Int N
    [simplification]
  rule flushSelected(A:ValSeq, WORD:IntSeq, COUNT:Int, N:Int)
    => valSeqConcat(A, vCons(str(WORD), .ValSeq))
    requires COUNT ==Int N andBool notBool (WORD ==K .IntSeq)
    [simplification]

  rule selectScan(S:IntSeq, N:Int, WORD:IntSeq, COUNT:Int, A:ValSeq)
    => flushSelected(
         scanAccum(S, N, WORD, COUNT, A),
         wordAfter(S, WORD),
         countAfter(S, COUNT),
         N)
    [simplification]

  // A space ends the current word.  Empty runs never create words.
  rule scanAccum(.IntSeq, _N:Int, _WORD:IntSeq, _COUNT:Int, A:ValSeq)
    => A
    [simplification]
  rule scanAccum(iCons(C:Int, R:IntSeq), N:Int, _WORD:IntSeq,
                 COUNT:Int, A:ValSeq)
    => scanAccum(R, N, .IntSeq, 0, A)
    requires C ==Int 32 andBool COUNT =/=Int N
    [simplification]
  rule scanAccum(iCons(C:Int, R:IntSeq), N:Int, .IntSeq,
                 COUNT:Int, A:ValSeq)
    => scanAccum(R, N, .IntSeq, 0, A)
    requires C ==Int 32 andBool COUNT ==Int N
    [simplification]
  rule scanAccum(iCons(C:Int, R:IntSeq), N:Int,
                 WORD:IntSeq, COUNT:Int, A:ValSeq)
    => scanAccum(
         R, N, .IntSeq, 0,
         valSeqConcat(
           A, vCons(str(WORD), .ValSeq)))
    requires C ==Int 32 andBool COUNT ==Int N
      andBool notBool (WORD ==K .IntSeq)
    [simplification]

  // Every non-space code extends the current word.  Membership in the exact
  // vowel literal used by solution.py determines whether the count changes.
  rule scanAccum(iCons(C:Int, R:IntSeq), N:Int, WORD:IntSeq,
                 COUNT:Int, A:ValSeq)
    => scanAccum(
         R, N, seqConcat(WORD, iCons(C, .IntSeq)), COUNT, A)
    requires C =/=Int 32
      andBool strContains(
        iCons(C, .IntSeq), strToCodes("aeiouAEIOU"))
    [simplification]
  rule scanAccum(iCons(C:Int, R:IntSeq), N:Int, WORD:IntSeq,
                 COUNT:Int, A:ValSeq)
    => scanAccum(
         R, N, seqConcat(WORD, iCons(C, .IntSeq)),
         COUNT +Int 1, A)
    requires C =/=Int 32
      andBool notBool strContains(
        iCons(C, .IntSeq), strToCodes("aeiouAEIOU"))
    [simplification]

  // Final loop-local values.  They are specified separately so the loop
  // circularity describes exactly the state that the fixed semantics reaches.
  rule wordAfter(.IntSeq, WORD:IntSeq) => WORD
    [simplification]
  rule wordAfter(iCons(C:Int, R:IntSeq), _WORD:IntSeq)
    => wordAfter(R, .IntSeq)
    requires C ==Int 32
    [simplification]
  rule wordAfter(iCons(C:Int, R:IntSeq), WORD:IntSeq)
    => wordAfter(R, seqConcat(WORD, iCons(C, .IntSeq)))
    requires C =/=Int 32
    [simplification]

  rule countAfter(.IntSeq, COUNT:Int) => COUNT
    [simplification]
  rule countAfter(iCons(C:Int, R:IntSeq), _COUNT:Int)
    => countAfter(R, 0)
    requires C ==Int 32
    [simplification]
  rule countAfter(iCons(C:Int, R:IntSeq), COUNT:Int)
    => countAfter(R, COUNT)
    requires C =/=Int 32
      andBool strContains(
        iCons(C, .IntSeq), strToCodes("aeiouAEIOU"))
    [simplification]
  rule countAfter(iCons(C:Int, R:IntSeq), COUNT:Int)
    => countAfter(R, COUNT +Int 1)
    requires C =/=Int 32
      andBool notBool strContains(
        iCons(C, .IntSeq), strToCodes("aeiouAEIOU"))
    [simplification]

  rule charAfter(.IntSeq, OLD:IntSeq) => OLD
    [simplification]
  rule charAfter(iCons(C:Int, R:IntSeq), _OLD:IntSeq)
    => charAfter(R, iCons(C, .IntSeq))
    [simplification]

endmodule
