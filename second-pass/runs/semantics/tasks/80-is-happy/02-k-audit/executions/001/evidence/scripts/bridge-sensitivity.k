requires "verification.k"

module BRIDGE-FIXED-CORRECT
  imports VERIFICATION-BASE

  claim
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
          [ "i" <- (0 => 1) ],
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

module BRIDGE-FIXED-FALSE
  imports VERIFICATION-BASE

  // False for "abc": fixed execution increments i from 0 to 1.
  claim
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

module BRIDGE-ENABLED-FALSE
  imports VERIFICATION

  // The proof-local bridge makes the false fixed-semantics conclusion close.
  claim
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
