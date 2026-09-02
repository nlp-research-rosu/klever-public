requires "body-mutation-verification.k"

module X-OR-Y-BODY-SENSITIVITY
  imports X-OR-Y-BODY-MUT-VERIFICATION

  // Reachable original-program loop-head witness after testing divisor 2:
  // n=9, next D=3, old divisor=2, x=1, y=2. The mutated body returns 1,
  // while the original summary obligation requires 2.
  claim
    <k>
      #loop(rangeObj(3, 9, 1), Name("divisor"), xOrYLoopBodyMutated)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (2 => scanLast(9, 3, 2))
        "n" |-> 9
        "x" |-> 1
        "y" |-> 2,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(primeSelect(9, 3, 1, 2)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(body_sensitivity)]
endmodule
