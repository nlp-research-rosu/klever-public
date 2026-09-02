requires "verification.k"

// Intended input "abc", with the same valid global/builtin/local frames as the
// entry theorem. Fixed execution increments local i to 1 before reaching #pop.
module BRIDGE-STATE-BASE
  imports VERIFICATION-BASE

  claim [fixed-cannot-preserve-i]:
    <k>
      While(happyLoopCondition, happyLoopBody)
      ~> (Return(Bool(true)) .Stmts)
      ~> #endcall
    =>
      #pop
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "s" <- str(iCons(97, iCons(98, iCons(99, .IntSeq)))) ]
          [ "i" <- 0 ],
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(true) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// The proof-local priority rule preserves i=0 while manufacturing the same
// result, so the otherwise false complete-state conclusion becomes provable.
module BRIDGE-STATE-EXTENDED
  imports VERIFICATION

  claim [bridge-preserves-i-falsely]:
    <k>
      While(happyLoopCondition, happyLoopBody)
      ~> (Return(Bool(true)) .Stmts)
      ~> #endcall
    =>
      #pop
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "s" <- str(iCons(97, iCons(98, iCons(99, .IntSeq)))) ]
          [ "i" <- 0 ],
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(true) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
