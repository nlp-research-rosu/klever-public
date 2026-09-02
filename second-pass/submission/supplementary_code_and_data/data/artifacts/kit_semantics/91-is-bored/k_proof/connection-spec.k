requires "connection.k"

module CONNECTION-SPEC
  imports CONNECTION

  claim [strip-eq-ws]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("==", Str("")))
      =>
      true
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(ORIG:IntSeq)
          "count"     |-> N:Int
          "at_start"  |-> A:Bool
          "pending_i" |-> P:Bool
          "c"         |-> str(iCons(C:Int, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
    requires isWSC(C)

  claim [strip-eq-nonws]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("==", Str("")))
      =>
      false
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(ORIG:IntSeq)
          "count"     |-> N:Int
          "at_start"  |-> A:Bool
          "pending_i" |-> P:Bool
          "c"         |-> str(iCons(C:Int, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
    requires notBool isWSC(C)

  claim [strip-ne-ws]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("!=", Str("")))
      =>
      false
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(ORIG:IntSeq)
          "count"     |-> N:Int
          "at_start"  |-> A:Bool
          "pending_i" |-> P:Bool
          "c"         |-> str(iCons(C:Int, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
    requires isWSC(C)

  claim [strip-ne-nonws]:
    <k>
      Compare(
        Call(Attribute(Name("c"), "strip"), .Exprs),
        CmpOp("!=", Str("")))
      =>
      true
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ( "S"         |-> str(ORIG:IntSeq)
          "count"     |-> N:Int
          "at_start"  |-> A:Bool
          "pending_i" |-> P:Bool
          "c"         |-> str(iCons(C:Int, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
    requires notBool isWSC(C)
endmodule
