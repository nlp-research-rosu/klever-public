requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // The two inputs have the same character set, but the result is deliberately
  // mutated to false.  A discriminating proof must reject this claim.
  claim [false-postcondition]:
    <k>
      #loadAll(Module(
        FuncDef("same_chars", Params("s0", "s1"),
          Return(
            Compare(
              Call(Name("set"), Name("s0")),
              CmpOp("==", Call(Name("set"), Name("s1"))))))
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
                (Return(
                  Compare(
                    Call(Name("set"), Name("s0")),
                    CmpOp("==", Call(Name("set"), Name("s1")))))
                 .Stmts),
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
