requires "connection.k"

module CONNECTION-MUTATION-SPEC
  imports CONNECTION

  // Materially mutate strip() to upper(); for C=space the expected true result
  // is false, so fixed execution must reject this connection.
  claim [upper-is-not-strip]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "upper"), .Exprs),
        CmpOp("==", Str("")))
      =>
      true
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(ORIG:IntSeq)
          "count"     |-> N:Int
          "at_start"  |-> A:Bool
          "pending_i" |-> P:Bool
          "c"         |-> str(iCons(32, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
endmodule
