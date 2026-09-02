requires "verification.k"

module AUDIT-EMPTY-SPEC
  imports GET-ROW-VERIFICATION

  claim [empty]:
    <k>
      Call(Name("get_row"), list(.ValSeq), X:Int, .Exprs)
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("get_row" |-> getRowClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(.ValSeq)
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
