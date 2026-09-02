requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the empty dictionary must return false, but this
  // mutation asks the exact loaded program to bind result to true.
  claim [empty-returns-true]:
    <k>
      #loadAll(Module(
        FuncDef("check_dict_case", Params("dict"), checkDictBody())
        Assign(
          Name("result"),
          Call(
            Name("check_dict_case"),
            dictV(.ValSeq, .ValSeq)))))
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
              checkDictBody(),
              0)
          "result" |-> true,
          parent(-1))
        -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
