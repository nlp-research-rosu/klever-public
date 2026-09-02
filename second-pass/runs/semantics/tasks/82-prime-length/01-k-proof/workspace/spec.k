requires "verification.k"

// Inductive loop theorem.  The setup witness below captures the live N and D
// at the exact While statement; the supplied While -> #while rule reaches
// this theorem's LHS.
module LOOP-SPEC
  imports VERIFICATION

  claim [divisor-loop]:
    <k>
      #while(
        Compare(Name("divisor"), CmpOp("<", Name("n"))),
        primeLoopBody)
      ~> Return(Bool(true))
      ~> .Stmts
      ~> #endcall
      =>
      noDivisorsFrom(N:Int, D:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> scope(BUILTINS:Map, root)
       1 |-> scope(
         "divisor" |-> D
         "n" |-> N
         "string" |-> _S:Val,
         parent(0)))
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> scope(BUILTINS, root))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 2
endmodule

module SPEC
  imports VERIFICATION

  // Lengths zero and one return False before entering the divisor loop.
  claim [prime-length-small]:
    <k>
      #applyK(
        toCall(primeLengthClosure),
        (str(CS:IntSeq), .Vals))
      =>
      false
    </k>
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
    requires isLen(CS) >=Int 0
     andBool isLen(CS) <Int 2

  // For every length at least two, setup reaches the loop theorem's LHS with
  // N = len(string) and D = 2.  Together with divisor-loop, this yields
  // noDivisorsFrom(N,2), the definition of primality on this domain.
  claim [prime-length-setup]:
    <k>
      #applyK(
        toCall(primeLengthClosure),
        (str(CS:IntSeq), .Vals))
      =>
      #primeLoopEntry(isLen(CS), 2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      .Map
    </scopes>
    <scopeLoc> 1 => 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(CS) >=Int 2
endmodule
