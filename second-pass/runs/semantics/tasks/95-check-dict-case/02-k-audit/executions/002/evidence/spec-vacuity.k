requires "verification.k"

module SPEC-VACUITY
  imports CHECK-DICT-CASE-VERIFICATION

  // Fresh result mutation: flip the exact loop result. For the satisfying
  // empty-list state with SEEN=false, LOWER=true, UPPER=true, real execution
  // returns false while this mutated destination demands true.
  claim [loop-result-negated]:
    <k> #loop(list(KS:ValSeq), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
      => notBool checkDictCaseResult(KS, SEEN, LOWER, UPPER)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(
             "check_dict_case"
               |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "has_key"   |-> SEEN:Bool
             "all_lower" |-> LOWER:Bool
             "all_upper" |-> UPPER:Bool
             "dict"      |-> DICT:Val
             "key"       |-> OLDKEY:Val,
             parent(0))
      =>
      0 |-> scope(
             "check_dict_case"
               |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
