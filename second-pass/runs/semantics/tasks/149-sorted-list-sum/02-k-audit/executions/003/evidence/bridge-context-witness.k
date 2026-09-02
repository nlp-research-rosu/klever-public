requires "reference-semantics/semantics.k"

module BRIDGE-CONTEXT-WITNESS
  imports MPY

  // The one-element loop must both append "aa" and leave word == "aa".
  // The arbitrary-CONT candidate bridge instead skips the target binding,
  // so it cannot establish this fixed-semantics result.
  claim
    <k>
      #loop(
        list(vCons(str(iCons(97, iCons(97, .IntSeq))), .ValSeq)),
        Name("word"),
        If(
          Compare(
            BinOp("%", Call(Name("len"), Name("word")), Int(2)),
            CmpOp("==", Int(0))),
          Expr(
            Call(
              Attribute(Name("even_words"), "append"),
              Name("word"))),
          .Stmts))
      ~> Name("word")
    =>
      str(iCons(97, iCons(97, .IntSeq)))
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
             "lst" |-> list(vCons(str(iCons(97, iCons(97, .IntSeq))), .ValSeq))
             "even_words" |-> ref(0),
             parent(0))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
             "lst" |-> list(vCons(str(iCons(97, iCons(97, .IntSeq))), .ValSeq))
             "even_words" |-> ref(0)
             "word" |-> str(iCons(97, iCons(97, .IntSeq))),
             parent(0))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
    =>
      0 |-> list(vCons(str(iCons(97, iCons(97, .IntSeq))), .ValSeq))
    </heap>
endmodule
