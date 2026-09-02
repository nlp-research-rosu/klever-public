requires "audit-connection-verification.k"

module AUDIT-FIXED-DISPATCH-SPEC
  imports AUDIT-CONNECTION-VERIFICATION

  claim [plus-int-domain]:
    <k> applyBin("+", I1:Int, I2:Int) => I1 +Int I2 </k>
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

  claim [min-int-domain]:
    <k>
      applyBuiltin("min", I1:Int, I2:Int, .Vals)
      => minInt(I1, I2)
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
endmodule
