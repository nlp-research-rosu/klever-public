requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Satisfiable witness: the input is the empty integer list. The real
  // program returns false; this mutation deliberately demands true.
  claim [empty-list-wrong-result]:
    <k>
      #loadAll(Module(
        FuncDef("pairs_sum_to_zero", Params("l"),
          Assign(Name("found"), Bool(false))
          Assign(Name("x"), Int(0))
          For(Name("x"), Name("l"),
            If(Compare(Name("x"), CmpOp("==", Int(0))),
              If(Compare(
                Call(Attribute(Name("l"), "count"), Int(0)),
                CmpOp(">", Int(1))),
                Assign(Name("found"), Bool(true)),
                .Stmts),
              If(Compare(
                Call(Attribute(Name("l"), "count"),
                     UnaryOp("-", Name("x"))),
                CmpOp(">", Int(0))),
                Assign(Name("found"), Bool(true)),
                .Stmts)))
          Return(Name("found"))
        )
        Assign(
          Name("$result"),
          Call(Name("pairs_sum_to_zero"), list(.ValSeq)))
      ))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope((.Map => ?MODULE:Map), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures {?MODULE["$result"]}:>Bool ==Bool true
endmodule
