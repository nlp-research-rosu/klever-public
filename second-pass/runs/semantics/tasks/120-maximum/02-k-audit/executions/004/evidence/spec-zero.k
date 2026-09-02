requires "verification.k"

module MAXIMUM-SPEC-ZERO
  imports MAXIMUM-VERIFICATION

  claim
    <k>
      Call(Name("maximum"), list(VS:ValSeq), 0, .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "maximum" |-> closureVal(("arr", "k", .ParamNames), maximumBody, 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
