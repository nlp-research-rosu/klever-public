requires "verification.k"

module BRIDGE-EXTENDED-LOOP-WITNESS
  imports CHECK-DICT-CASE-VERIFICATION

  // Same ground loop state as bridge-fixed-loop-witness.k.  The candidate
  // priority-30 isinstance splitter returns false for ref(7), so the candidate
  // theory proves the opposite final result.
  claim [extended-loop-ref-key]:
    <k> #loop(list(vCons(ref(7), .ValSeq)),
              Name("key"),
              checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
      =>
         false
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
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
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
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
