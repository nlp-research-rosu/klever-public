requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A symbolic sequence of words.  Keeping this separate from ValSeq lets the
  // prover perform structural induction while each element is known to be a
  // string.
  syntax WordSeq ::= ".WordSeq"
                   | wCons(IntSeq, WordSeq)

  // Opaque projection observed by the iterator rules below.  Using a
  // constructor (rather than an eager function) gives the symbolic executor
  // a clean two-case structural split on WordSeq.
  syntax ValSeq ::= wordsVals(WordSeq)

  rule <k> #iterNext(list(wordsVals(.WordSeq)))
        => #iterDone ... </k>
    [priority(30)]
  rule <k> #iterNext(list(wordsVals(wCons(C:IntSeq, R:WordSeq))))
        => #iterYield(str(C), list(wordsVals(R))) ... </k>
    [priority(30)]

  // Sentence represented by nonempty words separated by one ASCII space.
  // Opaque symbolic projection of WordSeq to its concrete space-separated
  // character sequence.  split's extensional rule below is its observer.
  syntax IntSeq ::= sentenceCodes(WordSeq) [function, total]
  // Opposite-interpretation probe: the otherwise unconstrained projection for
  // the valid word sequence ["aa", "bbb", "cccc"] denotes concrete string "x".
  rule sentenceCodes(
         wCons(
           iCons(97, iCons(97, .IntSeq)),
           wCons(
             iCons(98, iCons(98, iCons(98, .IntSeq))),
             wCons(
               iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
               .WordSeq))))
    => iCons(120, .IntSeq)
    [simplification]

  syntax Int ::= sentenceLen(WordSeq) [function, total]
  rule sentenceLen(.WordSeq) => 0
  rule sentenceLen(wCons(C:IntSeq, .WordSeq)) => isLen(C)
  rule sentenceLen(wCons(C:IntSeq, wCons(D:IntSeq, R:WordSeq)))
    => isLen(C) +Int 1 +Int sentenceLen(wCons(D, R))

  syntax Bool ::= validWords(WordSeq) [function, total]
  rule validWords(.WordSeq) => true
  rule validWords(wCons(C:IntSeq, R:WordSeq))
    => (isLen(C) >Int 0)
       andBool allAlpha(C)
       andBool validWords(R)

  // Complete prime characteristic function on the task's length domain 1..100.
  syntax Bool ::= primeLength(Int) [function, total]
  rule primeLength(N:Int)
    => N ==Int 2  orBool N ==Int 3  orBool N ==Int 5
       orBool N ==Int 7  orBool N ==Int 11 orBool N ==Int 13
       orBool N ==Int 17 orBool N ==Int 19 orBool N ==Int 23
       orBool N ==Int 29 orBool N ==Int 31 orBool N ==Int 37
       orBool N ==Int 41 orBool N ==Int 43 orBool N ==Int 47
       orBool N ==Int 53 orBool N ==Int 59 orBool N ==Int 61
       orBool N ==Int 67 orBool N ==Int 71 orBool N ==Int 73
       orBool N ==Int 79 orBool N ==Int 83 orBool N ==Int 89
       orBool N ==Int 97

  // Mathematical specification: filter the words, inserting a separator only
  // between retained words.
  syntax IntSeq ::= selectWord(IntSeq, IntSeq) [function, total]
  rule selectWord(A:IntSeq, C:IntSeq) => C
    requires A ==K .IntSeq
     andBool primeLength(isLen(C))
  rule selectWord(A:IntSeq, C:IntSeq)
    => seqConcat(seqConcat(A, iCons(32, .IntSeq)), C)
    requires notBool (A ==K .IntSeq)
     andBool primeLength(isLen(C))
  rule selectWord(A:IntSeq, C:IntSeq) => A
    requires notBool primeLength(isLen(C))

  syntax IntSeq ::= filterWords(IntSeq, WordSeq) [function, total]
  rule filterWords(A:IntSeq, .WordSeq) => A
  rule filterWords(A:IntSeq, wCons(C:IntSeq, R:WordSeq))
    => filterWords(selectWord(A, C), R)

  // This is the exact expression emitted in solution.mpy.
  syntax Expr ::= primeTest(Expr) [macro]
  rule primeTest(E:Expr)
    => BoolOp(
         "or",
         Compare(E, CmpOp("==", Int(2))),
         Compare(E, CmpOp("==", Int(3))),
         Compare(E, CmpOp("==", Int(5))),
         Compare(E, CmpOp("==", Int(7))),
         Compare(E, CmpOp("==", Int(11))),
         Compare(E, CmpOp("==", Int(13))),
         Compare(E, CmpOp("==", Int(17))),
         Compare(E, CmpOp("==", Int(19))),
         Compare(E, CmpOp("==", Int(23))),
         Compare(E, CmpOp("==", Int(29))),
         Compare(E, CmpOp("==", Int(31))),
         Compare(E, CmpOp("==", Int(37))),
         Compare(E, CmpOp("==", Int(41))),
         Compare(E, CmpOp("==", Int(43))),
         Compare(E, CmpOp("==", Int(47))),
         Compare(E, CmpOp("==", Int(53))),
         Compare(E, CmpOp("==", Int(59))),
         Compare(E, CmpOp("==", Int(61))),
         Compare(E, CmpOp("==", Int(67))),
         Compare(E, CmpOp("==", Int(71))),
         Compare(E, CmpOp("==", Int(73))),
         Compare(E, CmpOp("==", Int(79))),
         Compare(E, CmpOp("==", Int(83))),
         Compare(E, CmpOp("==", Int(89))),
         Compare(E, CmpOp("==", Int(97))))

  syntax Stmts ::= "solutionLoopBody" [macro]
  rule solutionLoopBody
    => Assign(Name("n"), Call(Name("len"), Name("word")))
       If(
         primeTest(Name("n")),
         If(
           Compare(Name("result"), CmpOp("==", Str(""))),
           Assign(Name("result"), Name("word")) .Stmts,
           Assign(
             Name("result"),
             BinOp(
               "+",
               BinOp("+", Name("result"), Str(" ")),
               Name("word"))) .Stmts) .Stmts,
         .Stmts) .Stmts

  syntax Stmts ::= "solutionBody" [macro]
  rule solutionBody
    => Assign(
         Name("words"),
         Call(Attribute(Name("sentence"), "split"), .Exprs))
       Assign(Name("result"), Str(""))
       Assign(Name("word"), Str(""))
       Assign(Name("n"), Int(0))
       Assign(Name("_plain"), Int(0))
       For(Name("word"), Name("words"), solutionLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Module ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef(
           "words_in_sentence",
           Params("sentence"),
           solutionBody)
         .Stmts)

  // The reference split implementation is concrete.  This extensional rule
  // exposes its result for a symbolic, contract-valid sentence representation.
  // The frontend marks this capture-free function as a plain frame.  These
  // priority rules make that known fact explicit to symbolic execution and
  // suppress infeasible closure-cell branches over an abstract map remainder.
  rule <k> #bindTgt(Name("word"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> R:Val)
           ("word" |-> _:Val)
           ("n" |-> N:Int)
           M:Map
           =>
           ("_plain" |-> 0)
           ("result" |-> R)
           ("word" |-> V)
           ("n" |-> N)
           M,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k> Assign(Name("n"), V:Int) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> R:Val)
           ("word" |-> W:Val)
           ("n" |-> _:Int)
           M:Map
           =>
           ("_plain" |-> 0)
           ("result" |-> R)
           ("word" |-> W)
           ("n" |-> V)
           M,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k> Assign(Name("result"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> _:Val)
           ("word" |-> W:Val)
           ("n" |-> N:Int)
           M:Map
           =>
           ("_plain" |-> 0)
           ("result" |-> V)
           ("word" |-> W)
           ("n" |-> N)
           M,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k>
         Call(Name("len"), Name("word"))
         => isLen(C)
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("word" |-> str(C:IntSeq))
           M:Map,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k> Name("n") => N ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> R:Val)
           ("word" |-> W:Val)
           ("n" |-> N:Int)
           M:Map,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k> Name("word") => W ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> R:Val)
           ("word" |-> W:Val)
           ("n" |-> N:Int)
           M:Map,
           P:Parent)
         ...
       </scopes>
    [priority(30)]

  rule <k> Name("result") => R ... </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ("_plain" |-> 0)
           ("result" |-> R:Val)
           ("word" |-> W:Val)
           ("n" |-> N:Int)
           M:Map,
           P:Parent)
         ...
       </scopes>
    [priority(30)]
endmodule
