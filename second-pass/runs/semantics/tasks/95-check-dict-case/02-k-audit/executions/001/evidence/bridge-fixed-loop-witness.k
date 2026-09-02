requires "bridge-audit-base.k"

module BRIDGE-FIXED-LOOP-WITNESS
  imports BRIDGE-AUDIT-BASE

  // Ground instance of the candidate loop claim's precondition.  With fixed
  // semantics, ref(7) is dereferenced to "a", so the function returns true.
  claim [fixed-loop-ref-key]:
    <k> #loop(list(vCons(ref(7), .ValSeq)),
              Name("key"),
              auditLoopBody())
         ~> (Return(auditResultExpr()) .Stmts)
         ~> #endcall
      =>
         true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), auditBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
               "has_key"   |-> false
               "all_lower" |-> true
               "all_upper" |-> true
               "dict"      |-> dictV(vCons(ref(7), .ValSeq), vCons(0, .ValSeq))
               "key"       |-> noneV,
               parent(0))
      =>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), auditBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> 7 |-> str(iCons(97, .IntSeq)) </heap>
    <heapLoc> 8 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
