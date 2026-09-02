requires "verification.k"

module X-OR-Y-LOOP-SPEC
  imports X-OR-Y-VERIFICATION

  // Inductive loop invariant.  The recursive non-divisor case advances both
  // the Python range iterator and primeSelect, allowing this claim to close
  // by circularity.
  claim
    <k>
      #loop(rangeObj(D:Int, N:Int, 1), Name("divisor"), xOrYLoopBody)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BS:Scope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (OLD:Int => scanLast(N, D, OLD))
        "n" |-> N:Int
        "x" |-> X:Val
        "y" |-> Y:Val,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(primeSelect(N, D, X:Val, Y:Val)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
      andBool D >=Int 2
    [label(loop_correct)]
endmodule

module X-OR-Y-MAIN-SPEC
  imports X-OR-Y-SUMMARY

  // Universal functional correctness for every integer n and arbitrary
  // Python values x and y, from the reference semantics' initial state.
  claim
    <k> #xOrY(N:Int, X:Val, Y:Val) => primeSelect(N, 2, X, Y) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_correct)]
endmodule
