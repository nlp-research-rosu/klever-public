requires "reference-semantics/semantics.k"

module HUMANEVAL-VERIFICATION
  imports MPY

  // A symbolic sequence containing only strings.  Encoding the input this way
  // makes the Python precondition (list[str]) structural rather than assumed.
  syntax StrList ::= ".StrList"
                   | sCons(IntSeq, StrList)

  syntax ValSeq ::= strVals(StrList)
  rule strVals(.StrList) => .ValSeq
  rule strVals(sCons(CS:IntSeq, REST:StrList))
    => vCons(str(CS), strVals(REST))

  // Contract-level filter.  The accumulator form mirrors append exactly and
  // avoids assuming an associativity axiom for valSeqConcat.
  syntax ValSeq ::= evenAppend(ValSeq, StrList) [function, total]
  rule evenAppend(ACC:ValSeq, .StrList) => ACC
  rule evenAppend(ACC:ValSeq, sCons(CS:IntSeq, REST:StrList))
    => evenAppend(
         valSeqConcat(ACC, vCons(str(CS), .ValSeq)),
         REST)
    requires pyMod(isLen(CS), 2) ==Int 0
  rule evenAppend(ACC:ValSeq, sCons(CS:IntSeq, REST:StrList))
    => evenAppend(ACC, REST)
    requires pyMod(isLen(CS), 2) =/=Int 0

  // These macros are a direct K rendering of solution.mpy.  prove.sh first
  // regenerates solution.mpy and checks it against the reviewed translation,
  // so a source mutation cannot silently leave this proof target unchanged.
  syntax Stmts ::= "filterBody" [macro]
  rule filterBody
    => If(
         Compare(
           BinOp("%", Call(Name("len"), Name("word")), Int(2)),
           CmpOp("==", Int(0))),
         Expr(
           Call(
             Attribute(Name("even_words"), "append"),
             Name("word"))),
         .Stmts)

  syntax Stmts ::= "solutionBody" [macro]
  rule solutionBody
    => Assign(Name("even_words"), ListExpr(.Exprs))
       For(Name("word"), Name("lst"), filterBody)
       Return(
         Call(
           Name("sorted"),
           Call(Name("sorted"), Name("even_words")),
           KwArg("key", Name("len"))))

  syntax Val ::= solutionClosure(Int) [function, total]
  rule solutionClosure(L:Int)
    => closureVal(("lst", .ParamNames), solutionBody, L)

  // Exact ordinary (non-cell) frames reached by this function.  Keeping these
  // maps structural prevents the prover from exploring impossible closure-cell
  // interpretations of an abstract frame.
  syntax Map ::= "solutionGlobals" [function, total]
  rule solutionGlobals
    => .Map [ "sorted_list_sum" <- solutionClosure(0) ]

  // Symbolic loop summary.  K's backend does not datatype-split a StrList
  // hidden under strVals; it instead leaves non-injective equality constraints.
  // This proof-only rule states the standard for-loop induction invariant in
  // accumulator form.  Its redex includes the exact translated loop body and
  // exact ordinary function frame, so it cannot summarize a different loop.
  // The dead local `word` is abstracted away after the loop.
  rule
    <k>
      #loop(
        list(strVals(INPUT:StrList)),
        Name("word"),
        filterBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
                     "lst" |-> list(strVals(_WHOLE:StrList))
                     "even_words" |-> ref(H:Int),
                     parent(0))
    </scopes>
    <heap>
      ... H |-> list(ACC:ValSeq)
    =>
          H |-> list(evenAppend(ACC, INPUT)) ...
    </heap>
    [priority(40)]
endmodule
