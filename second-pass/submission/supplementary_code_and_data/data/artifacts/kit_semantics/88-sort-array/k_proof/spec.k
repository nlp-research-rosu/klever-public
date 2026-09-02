requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [empty]:
    <k> Call(Name("sort_array"), ref(0)) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sort_array" |->
          closureVal(
            "array",
            If(
              UnaryOp("not", Name("array")),
              Return(Call(Name("sorted"), Name("array"))) .Stmts,
              .Stmts)
            Return(
              Call(
                Name("sorted"),
                Name("array"),
                KwArg(
                  "reverse",
                  Compare(
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      (0 |-> list(.ValSeq))
      =>
      (0 |-> list(.ValSeq)
       1 |-> list(.ValSeq))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [nonempty]:
    <k> Call(Name("sort_array"), ref(0)) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sort_array" |->
          closureVal(
            "array",
            If(
              UnaryOp("not", Name("array")),
              Return(Call(Name("sorted"), Name("array"))) .Stmts,
              .Stmts)
            Return(
              Call(
                Name("sorted"),
                Name("array"),
                KwArg(
                  "reverse",
                  Compare(
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      (0 |-> list(intVals(iCons(F:Int, IS:IntSeq))))
      =>
      (0 |-> list(intVals(iCons(F, IS)))
       1 |-> list(
         condRev(
           sortVS(intVals(iCons(F, IS))),
           pyMod(F +Int L, 2) ==Int 0)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires F >=Int 0
      andBool nonNegative(IS)
      andBool valSeqAt(
        vCons(F, intVals(IS)),
        vsLen(intVals(IS))) ==K L:Int
endmodule
