requires "verification.k"

module AUDIT-SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed function term is changed to return true. For disjoint inputs
  // "a" and "b", the original program/result obligation is false.
  claim [fresh-changed-body]:
    <k>
      #loadAll(Module(
        FuncDef("same_chars", Params("s0", "s1"),
          Return(Bool(true)))
        Assign(
          Name("result"),
          Call(
            Name("same_chars"),
            str(iCons(97, .IntSeq)),
            str(iCons(98, .IntSeq))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
        .Map
          [ "same_chars" <-
              closureVal(
                ("s0", "s1", .ParamNames),
                (Return(Bool(true)) .Stmts),
                0) ]
          [ "result" <- false ],
        parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
