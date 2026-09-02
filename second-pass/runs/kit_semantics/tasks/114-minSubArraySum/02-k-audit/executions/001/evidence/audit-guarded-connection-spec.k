requires "audit-connection-verification.k"

module AUDIT-GUARDED-CONNECTION-SPEC
  imports AUDIT-CONNECTION-VERIFICATION

  claim [plus-val-guard]:
    <k>
      applyBin("+", I:Int, V:Val)
      => I +Int {V}:>Int
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(V)

  claim [min-val-guard]:
    <k>
      applyBuiltin("min", V:Val, I:Int, .Vals)
      => minInt({V}:>Int, I)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(V)
endmodule
