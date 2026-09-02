requires "reference-semantics/semantics.k"

module HELPER-FIXED-COLLISION
  imports MPY

  claim
    <k>
      #applyK(toCall(closureVal(
        ("string", .ParamNames),
        Return(Compare(Name("string"),
          CmpOp("==", Subscript(Name("string"),
            Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts,
        0)),
        (str(iCons(99, iCons(97, iCons(116, .IntSeq)))), .Vals))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope("sentinel" |-> 42, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 0 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
