requires "verification.k"

module AUDIT-FALSE-MUTATION
  imports VERIFICATION

  // Fresh A5 mutation: the real candidate body returns true for the
  // nonempty all-lower dictionary {"a": 1, "b2": 2}; this claim deliberately
  // changes only the result obligation to false.
  claim [all-lower-returns-false]:
    <k>
      #loadAll(Module(
        FuncDef("check_dict_case", Params("dict"), checkDictBody())
        Assign(
          Name("result"),
          Call(
            Name("check_dict_case"),
            dictV(
              vCons(
                str(iCons(97, .IntSeq)),
                vCons(str(iCons(98, iCons(50, .IntSeq))), .ValSeq)),
              vCons(1, vCons(2, .ValSeq)))))))
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
            closureVal(("dict", .ParamNames), checkDictBody(), 0)
          "result" |-> false,
          parent(-1))
        -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(str(iCons(98, iCons(50, .IntSeq))), .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
