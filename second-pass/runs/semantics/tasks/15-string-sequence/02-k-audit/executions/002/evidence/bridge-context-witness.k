requires "verification.k"

// The candidate bridge constrains only the local n binding and admits arbitrary
// outer scopes.  Here the module scope shadows Python's str with len.  Fixed
// semantics reaches applyBuiltin("len", 1, .Vals) and sticks; the candidate
// bridge skips that lookup/call and fabricates the normal "0 1" result.

module BRIDGE-CONTEXT-WITH
  imports VERIFICATION

  claim <k> sequenceBody ~> #endcall
           => str(sequenceCodes(1)) </k>
        <env> 1 => 0 </env>
        <scopes>
          (1 |-> scope("n" |-> 1, parent(0))
           0 |-> scope("str" |-> builtinV("len"), parent(-1))
           -1 |-> builtinsScope)
          => (1 |-> scope("n" |-> 1, parent(0))
              0 |-> scope("str" |-> builtinV("len"), parent(-1))
              -1 |-> builtinsScope) [1 <- undef]
        </scopes>
        <scopeLoc> 2 => 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule

module BRIDGE-CONTEXT-BASE
  imports VERIFICATION-BASE

  claim <k> sequenceBody ~> #endcall
           => str(sequenceCodes(1)) </k>
        <env> 1 => 0 </env>
        <scopes>
          (1 |-> scope("n" |-> 1, parent(0))
           0 |-> scope("str" |-> builtinV("len"), parent(-1))
           -1 |-> builtinsScope)
          => (1 |-> scope("n" |-> 1, parent(0))
              0 |-> scope("str" |-> builtinV("len"), parent(-1))
              -1 |-> builtinsScope) [1 <- undef]
        </scopes>
        <scopeLoc> 2 => 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule
