requires "verification.k"

module CHECK-DICT-CASE-SPEC-VACUITY
  imports CHECK-DICT-CASE-VERIFICATION

  // Deliberately false mutation: negate the result-constraining loop summary.
  // Ground counterexample:
  //   KS=.ValSeq, SEEN=true, LOWER=true, UPPER=false,
  //   DICT=dictV(.ValSeq,.ValSeq), OLDKEY=noneV, HEAP=.Map, NEXTHEAP=0.
  // The real execution returns true; this destination requires false.
  claim [false-loop-result]:
    <k> #loop(list(KS:ValSeq), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
        =>
         notBool checkDictCaseResult(KS, SEEN, LOWER, UPPER)
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
