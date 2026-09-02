requires "verification.k"

module SPEC
  imports VERIFICATION

  // Call the exact solution closure through ordinary Python name lookup.
  claim [iscube-entry]:
    <k>
      Call(Name("iscube"), Int(INPUT:Int))
      =>
      isCubeInt(INPUT)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
