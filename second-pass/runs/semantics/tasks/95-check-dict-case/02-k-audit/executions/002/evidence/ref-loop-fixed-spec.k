requires "verification-no-bridges.k"

module REF-LOOP-FIXED-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // Ground instance of the candidate loop claim's own precondition. The fixed
  // semantics dereferences ref(0) to the string "a", so the real suffix returns
  // true.
  claim [loop-ref-to-string]:
    <k> #loop(list(vCons(ref(0), .ValSeq)),
              Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(
             "check_dict_case"
               |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "has_key"   |-> false
             "all_lower" |-> true
             "all_upper" |-> true
             "dict"      |-> dictV(vCons(ref(0), .ValSeq),
                                    vCons(0, .ValSeq))
             "key"       |-> noneV,
             parent(0))
      =>
      0 |-> scope(
             "check_dict_case"
               |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> 0 |-> str(iCons(97, .IntSeq)) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
