requires "verification.k"

module BODY-SENSITIVITY-SPEC
  imports MPY-VERIFICATION

  // Operational-sensitivity mutation: append to reversed_result instead of
  // prepending. For s="ab", c="", this body returns ("ab", true), while the
  // unchanged target summary requires ("ab", false).
  claim
    <k>
      Call(
        closureVal(
          ("s", "c"),
          Assign(Name("result"), Str(""))
          Assign(Name("reversed_result"), Str(""))
          Assign(Name("character"), Str(""))
          For(
            Name("character"),
            Name("s"),
            If(
              Compare(Name("character"), CmpOp("not in", Name("c"))),
              AugAssign(Name("result"), "+", Name("character"))
              Assign(
                Name("reversed_result"),
                BinOp("+", Name("reversed_result"), Name("character"))),
              .Stmts))
          Return(
            TupleExpr(
              Name("result"),
              Compare(
                Name("result"),
                CmpOp("==", Name("reversed_result"))))),
          0),
        str(S:IntSeq),
        str(C:IntSeq))
      => tuple(
           vCons(
             str(keptAcc(S, C, .IntSeq)),
             vCons(
               keptAcc(S, C, .IntSeq)
                 ==K reversedKeptAcc(S, C, .IntSeq),
               .ValSeq)))
      ...
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
