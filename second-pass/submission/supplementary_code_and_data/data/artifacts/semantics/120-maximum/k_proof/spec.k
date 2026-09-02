requires "verification.k"

module MAXIMUM-SPEC
  imports MAXIMUM-VERIFICATION

  // The k = 0 branch is essential: sorted(arr)[-0:] would incorrectly return
  // the entire array.
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

  // For 0 < k <= len(arr), the returned heap object is exactly the suffix of
  // length k of the supplied ascending sorted permutation.
  claim
    <k>
      Call(Name("maximum"), list(VS:ValSeq), K:Int, .Exprs)
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "maximum" |-> closureVal(("arr", "k", .ParamNames), maximumBody, 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => (0 |-> list(sortVS(VS)))
         (1 |-> list(
           buildVS(
             sortVS(VS),
             0 -Int K +Int vsLen(VS),
             vsLen(VS),
             1)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 0 <Int K andBool K <=Int vsLen(VS)
endmodule
