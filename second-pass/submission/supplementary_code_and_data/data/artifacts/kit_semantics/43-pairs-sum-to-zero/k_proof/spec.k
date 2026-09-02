requires "verification.k"

module SPEC
  imports VERIFICATION

  // Program boundary: the exact translated function definition is loaded and
  // called with an unboxed semantic list.  Input domain: every element is Int.
  // Observable result: the returned Bool.  Other cells are unchanged.
  claim [loop-invariant]:
    <k>
      #loop(
        list(REM:ValSeq),
        Name("x"),
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
            .Stmts))
      ) => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "found" |-> (FOUND:Bool => FOUND orBool anyInverse(REM, FULL))
        "l"     |-> list(FULL:ValSeq)
        "x"     |-> (_X0:Val => ?XF:Val),
        parent(0))
      ...
    </scopes>
    requires allInts(FULL) andBool allInts(REM)

  claim [pairs-sum-to-zero]:
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
          Call(Name("pairs_sum_to_zero"), list(FULL:ValSeq)))
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
    requires allInts(FULL)
    ensures {?MODULE["$result"]}:>Bool ==Bool anyInverse(FULL, FULL)
endmodule
