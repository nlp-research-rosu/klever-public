requires "verification.k"

module FILTER-BY-PREFIX-LOOP-ONLY-SPEC
  imports VERIFICATION

  claim
    <k>
      #loop(
        stringList(REST:StrList),
        Name("string"),
        If(
          Call(Attribute(Name("string"), "startswith"), Name("prefix")),
          Expr(Call(Attribute(Name("result"), "append"), Name("string"))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "prefix" |-> str(PREFIX:IntSeq)
        "result" |-> ref(H:Int)
        "string" |-> CURRENT:Val
        "strings" |-> stringList(ORIGINAL:StrList),
        parent(0))
      =>
      SC
      L |-> scope(
        "prefix" |-> str(PREFIX)
        "result" |-> ref(H)
        "string" |-> ?FINALCURRENT:Val
        "strings" |-> stringList(ORIGINAL),
        parent(0))
    </scopes>
    <heap>
      H |-> list(
        ACC:ValSeq
        => valSeqConcat(ACC, prefixFilter(PREFIX, REST)))
    </heap>
endmodule
