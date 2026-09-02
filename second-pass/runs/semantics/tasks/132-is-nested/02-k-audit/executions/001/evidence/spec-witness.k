requires "verification.k"

module IS-NESTED-LOOP-WITNESS-SPEC
  imports IS-NESTED-VERIFICATION

  // Ground instance satisfying the generalized loop claim's complete precondition.
  claim [loop-empty-witness]:
    <k>
      #loop(str(bCodes(bNil)), Name("char"), scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4)))) .Stmts):Stmts
      ~> #endcall
      => false
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> 0
        "char" |-> str(.IntSeq)
        "string" |-> str(bCodes(bNil)),
        parent(0)) => .Map)
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module IS-NESTED-ENTRY-WITNESS-SPEC
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  // Ground instance satisfying the empty-input entry claim.
  claim [entry-empty-witness]:
    <k> Call(Name("is_nested"), str(bCodes(bNil))) => false </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Ground true instance satisfying the universal entry claim.
  claim [entry-nested-witness]:
    <k>
      Call(Name("is_nested"),
        str(bCodes(bOpen(bOpen(bClose(bClose(bNil)))))))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
