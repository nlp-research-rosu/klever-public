requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The exact body is materially changed to `return False`, while the
  // expected result for equal-character inputs remains true.
  claim [changed-body]:
    <k>
      #loadAll(Module(
        FuncDef("same_chars", Params("s0", "s1"),
          Return(Bool(false)))
        Assign(
          Name("result"),
          Call(
            Name("same_chars"),
            str(iCons(97, .IntSeq)),
            str(iCons(97, iCons(97, .IntSeq)))))))
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
                (Return(Bool(false)) .Stmts),
                0) ]
          [ "result" <- true ],
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
