requires "verification.k"

module SPEC
  imports VERIFICATION

  // A coinductive invariant over arbitrary current accumulator values.  The
  // folds carry symbolic islower/isupper results across the next loop cutpoint
  // instead of attempting a second, unrelated induction over string codes.
  claim [loop]:
    <k>
      #loop(list(KS:ValSeq), Name("key"), checkDictLoopBody())
      ~> Return(checkDictReturn()) .Stmts ~> #endcall
      =>
      Return(checkDictReturn()) .Stmts ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope("check_dict_case" |-> FUNCTION:Val, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "dict" |-> DICT:Val
        "all_lower" |-> (AL:Bool => foldLowerKeys(AL, KS))
        "all_upper" |-> (AU:Bool => foldUpperKeys(AU, KS))
        "seen_key" |-> (SEEN:Bool => SEEN orBool hasAnyKey(KS))
        "key" |-> (_OLDKEY:Val => ?FINALKEY:Val)
        "is_string" |-> (_OLDISSTRING:Bool => ?FINALISSTRING:Bool),
        parent(0))
    </scopes>
    requires L >=Int 1
     andBool notBool hasRefVS(KS)

  // Full entry-point theorem.  The actual translated body is loaded, looked
  // up by its public name, called with an arbitrary symbolic dictV, and its
  // return is assigned to result.
  claim [target]:
    <k>
      #loadAll(Module(
        FuncDef("check_dict_case", Params("dict"),
          Assign(Name("all_lower"), Bool(true))
          Assign(Name("all_upper"), Bool(true))
          Assign(Name("seen_key"), Bool(false))
          Assign(Name("key"), NoneVal)
          Assign(Name("is_string"), Bool(false))
          For(Name("key"), Call(Attribute(Name("dict"), "keys"), .Exprs),
            Assign(Name("seen_key"), Bool(true))
            Assign(
              Name("is_string"),
              BoolOp(
                "and",
                BoolOp("or", Name("all_lower"), Name("all_upper")),
                Call(Name("isinstance"), Name("key"), Name("str"))))
            Assign(
              Name("all_lower"),
              BoolOp(
                "and",
                Name("all_lower"),
                Name("is_string"),
                Call(Attribute(Name("key"), "islower"), .Exprs)))
            Assign(
              Name("all_upper"),
              BoolOp(
                "and",
                Name("all_upper"),
                Name("is_string"),
                Call(Attribute(Name("key"), "isupper"), .Exprs))))
          Return(
            BoolOp(
              "and",
              Name("seen_key"),
              BoolOp("or", Name("all_lower"), Name("all_upper")))))
        Assign(
          Name("result"),
          Call(
            Name("check_dict_case"),
            dictV(KS:ValSeq, VALUES:ValSeq)))))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope)
      =>
      ( 0 |-> scope(
          "check_dict_case" |->
            closureVal(
              ("dict", .ParamNames),
              Assign(Name("all_lower"), Bool(true))
              Assign(Name("all_upper"), Bool(true))
              Assign(Name("seen_key"), Bool(false))
              Assign(Name("key"), NoneVal)
              Assign(Name("is_string"), Bool(false))
              For(Name("key"), Call(Attribute(Name("dict"), "keys"), .Exprs),
                Assign(Name("seen_key"), Bool(true))
                Assign(
                  Name("is_string"),
                  BoolOp(
                    "and",
                    BoolOp("or", Name("all_lower"), Name("all_upper")),
                    Call(Name("isinstance"), Name("key"), Name("str"))))
                Assign(
                  Name("all_lower"),
                  BoolOp(
                    "and",
                    Name("all_lower"),
                    Name("is_string"),
                    Call(Attribute(Name("key"), "islower"), .Exprs)))
                Assign(
                  Name("all_upper"),
                  BoolOp(
                    "and",
                    Name("all_upper"),
                    Name("is_string"),
                    Call(Attribute(Name("key"), "isupper"), .Exprs))))
              Return(
                BoolOp(
                  "and",
                  Name("seen_key"),
                  BoolOp("or", Name("all_lower"), Name("all_upper")))),
              0)
          "result" |-> checkCaseSummary(true, true, false, KS),
          parent(-1))
        -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(KS) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool hasRefVS(KS)
endmodule
