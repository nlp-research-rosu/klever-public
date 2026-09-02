requires "connection.k"

module STAGE5-STRIP-FIXED-SPEC
  imports CONNECTION

  claim [space-with-observable-suffix]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("==", Str("")))
      ~> #notB
      => false
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(.IntSeq)
          "count"     |-> 0
          "at_start"  |-> true
          "pending_i" |-> false
          "c"         |-> str(iCons(32, .IntSeq)) ),
        parent(0))
      ...
    </scopes>

  claim [nonspace-with-observable-suffix]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("==", Str("")))
      ~> #notB
      => true
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(.IntSeq)
          "count"     |-> 0
          "at_start"  |-> true
          "pending_i" |-> false
          "c"         |-> str(iCons(120, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
endmodule
