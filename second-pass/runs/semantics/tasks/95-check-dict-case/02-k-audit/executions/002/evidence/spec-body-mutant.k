requires "verification-body-mutant.k"

module CHECK-DICT-CASE-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // The entry point, parameter binding, flag initialization, d.keys(), and
  // For setup reach the generalized loop state over exactly the dict key list.
  claim [entry-reaches-loop]:
    <k> #loadAll(checkDictCaseModule())
         ~> Call(Name("check_dict_case"),
                 (dictV(KS:ValSeq, VS:ValSeq), .Exprs))
        =>
         #loop(list(KS), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
               "dict"      |-> dictV(KS, VS)
               "has_key"   |-> false
               "all_lower" |-> true
               "all_upper" |-> true
               "key"       |-> noneV,
               parent(0))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map => 0 |-> list(KS) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack>
      .List => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Inductive loop theorem. OLDKEY generalizes the loop target binding, while
  // the exact local map makes this a decidable non-closure frame.
  claim [loop-and-return]:
    <k> #loop(list(KS:ValSeq), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
        =>
         checkDictCaseResult(KS, SEEN, LOWER, UPPER)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
               "has_key"   |-> SEEN:Bool
               "all_lower" |-> LOWER:Bool
               "all_upper" |-> UPPER:Bool
               "dict"      |-> DICT:Val
               "key"       |-> OLDKEY:Val,
               parent(0))
      =>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
