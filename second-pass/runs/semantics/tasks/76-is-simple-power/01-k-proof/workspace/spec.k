requires "verification.k"

module SIMPLE-POWER-SPEC
  imports SIMPLE-POWER-VERIFICATION

  // Inductive invariant: at the head of the repeated-division loop, the
  // remaining computation returns simplePower of the current x and n.
  claim [loop-correct]:
    <k> #while(powerCondition, powerLoopBody)
         ~> (Return(powerResult) .Stmts) ~> #endcall
      => positivePowerLoop(X, N)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      BASE:Map
      1 |-> scope(.Map [ "x" <- X ] [ "n" <- N ], _P:Parent)
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
  requires N >Int 1

  // The following four end-to-end claims partition all integer arguments.
  // Each starts from the supplied MPY namespaces, loads the exact generated
  // solution module, calls its entry point, and observes the returned Boolean.
  claim [function-one]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(1), Int(N))
      => simplePower(1, N)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

  claim [function-below-one]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(X), Int(N))
      => simplePower(X, N)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
  requires X <Int 1

  claim [function-degenerate-base]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(X), Int(N))
      => simplePower(X, N)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
  requires X >Int 1 andBool N <=Int 1

  claim [function-positive-domain]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(X), Int(N))
      => simplePower(X, N)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
  requires X >Int 1 andBool N >Int 1
endmodule
