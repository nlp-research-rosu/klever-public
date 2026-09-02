requires "verification.k"

module REVIEWER-GROUND-WITNESSES
  imports VERIFICATION

  claim [balanced-integer]:
    <k>
      Call(Name("will_it_fly"), (list(vCons(3, .ValSeq)), 5, .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("will_it_fly" |-> willItFlyClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(3, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [unbalanced-integer]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(vCons(1, vCons(2, .ValSeq))), 5, .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("will_it_fly" |-> willItFlyClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(2, vCons(1, .ValSeq))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [balanced-float]:
    <k>
      Call(Name("will_it_fly"), (list(vCons(1.5, .ValSeq)), 2.0, .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("will_it_fly" |-> willItFlyClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1.5, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [any-unbalanced-short-circuit]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(vCons(1.0, vCons(2.0, .ValSeq))), 5, .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("will_it_fly" |-> willItFlyClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(2.0, vCons(1.0, .ValSeq))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
