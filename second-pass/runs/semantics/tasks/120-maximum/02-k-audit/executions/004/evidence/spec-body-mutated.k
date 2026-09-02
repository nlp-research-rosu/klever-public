requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports MAXIMUM-BODY-MUTATED

  claim
    <k>
      Call(Name("maximum"), list(VS:ValSeq), K:Int, .Exprs)
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "maximum" |-> closureVal(
                 ("arr", "k", .ParamNames),
                 mutatedMaximumBody,
                 0),
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
