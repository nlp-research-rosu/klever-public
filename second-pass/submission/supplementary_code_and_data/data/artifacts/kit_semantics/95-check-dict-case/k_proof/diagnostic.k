requires "verification.k"

module DIAGNOSTIC
  imports VERIFICATION

  claim [base]:
    <k>
      #loop(list(.ValSeq), Name("key"), checkDictLoopBody())
      ~> Return(checkDictReturn()) ~> #endcall
      =>
      Return(checkDictReturn()) ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope("check_dict_case" |-> FUNCTION:Val, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "dict" |-> DICT:Val
        "all_lower" |-> AL:Bool
        "all_upper" |-> AU:Bool
        "seen_key" |-> SEEN:Bool
        "key" |-> (_OLDKEY:Val => ?FINALKEY:Val)
        "is_string" |-> (_OLDISSTRING:Bool => ?FINALISSTRING:Bool),
        parent(0))
    </scopes>
    requires L >=Int 1

  claim [one]:
    <k>
      #loop(list(vCons(V:Val, .ValSeq)), Name("key"), checkDictLoopBody())
      ~> Return(checkDictReturn()) ~> #endcall
      =>
      Return(checkDictReturn()) ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope("check_dict_case" |-> FUNCTION:Val, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "dict" |-> DICT:Val
        "all_lower" |-> (AL:Bool => AL andBool lowerKey(V))
        "all_upper" |-> (AU:Bool => AU andBool upperKey(V))
        "seen_key" |-> (SEEN:Bool => true)
        "key" |-> (_OLDKEY:Val => ?FINALKEY:Val)
        "is_string" |-> (_OLDISSTRING:Bool => ?FINALISSTRING:Bool),
        parent(0))
    </scopes>
    requires L >=Int 1
     andBool notBool isRefV(V)

  claim [one-tt]:
    <k>
      #loop(list(vCons(V:Val, .ValSeq)), Name("key"), checkDictLoopBody())
      ~> Return(checkDictReturn()) ~> #endcall
      =>
      Return(checkDictReturn()) ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope("check_dict_case" |-> FUNCTION:Val, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "dict" |-> DICT:Val
        "all_lower" |-> (true => lowerKey(V))
        "all_upper" |-> (true => upperKey(V))
        "seen_key" |-> (_SEEN:Bool => true)
        "key" |-> (_OLDKEY:Val => ?FINALKEY:Val)
        "is_string" |-> (_OLDISSTRING:Bool => ?FINALISSTRING:Bool),
        parent(0))
    </scopes>
    requires L >=Int 1
     andBool notBool isRefV(V)

  claim [one-ff]:
    <k>
      #loop(list(vCons(V:Val, .ValSeq)), Name("key"), checkDictLoopBody())
      ~> Return(checkDictReturn()) ~> #endcall
      =>
      Return(checkDictReturn()) ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope("check_dict_case" |-> FUNCTION:Val, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "dict" |-> DICT:Val
        "all_lower" |-> false
        "all_upper" |-> false
        "seen_key" |-> (_SEEN:Bool => true)
        "key" |-> (_OLDKEY:Val => ?FINALKEY:Val)
        "is_string" |-> (_OLDISSTRING:Bool => ?FINALISSTRING:Bool),
        parent(0))
    </scopes>
    requires L >=Int 1
     andBool notBool isRefV(V)
endmodule
