requires "verification-base.k"

module STAGE5-STRIP-OPPOSITE-SPEC
  imports VERIFICATION-BASE

  // Deliberately false: stripping a one-space string is empty, so equality is
  // true and the observable #notB suffix must produce false, not true.
  claim [opposite-space-interpretation]:
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
          "c"         |-> str(iCons(32, .IntSeq)) ),
        parent(0))
      ...
    </scopes>
endmodule
