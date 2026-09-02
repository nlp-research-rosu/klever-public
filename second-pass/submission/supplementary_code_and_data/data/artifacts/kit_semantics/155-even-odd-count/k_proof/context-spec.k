requires "verification-with-lemma.k"

module CONTEXT-SPEC
  imports VERIFICATION-WITH-LEMMA

  // The loop bridge must preserve an arbitrary caller continuation. Here the
  // function result is discarded by Expr and a following expression yields 7.
  claim [caller-continuation]:
    <k> Expr(Call(Name("even_odd_count"), Int(12))) ~> Int(7)
        => 7
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
