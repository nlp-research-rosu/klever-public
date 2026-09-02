requires "verification.k"

module MAX-FILL-SPEC
  imports MAX-FILL-VERIFICATION

  // Fixed-semantics auxiliary circularity for sum(row).
  claim [sum-loop]:
    <k> #sumAcc(list(VS:ValSeq), A:Int)
          => A +Int rowSum(VS) ... </k>
    requires allBinary(VS)

  // Program-loop circularity. The body is the exact AST emitted in solution.mpy.
  claim [grid-loop]:
    <k> #loop(
          list(GS:ValSeq),
          Name("row"),
          AugAssign(
            Name("total"),
            "+",
            BinOp(
              "//",
              BinOp(
                "-",
                BinOp("+", Call(Name("sum"), Name("row")), Name("capacity")),
                Int(1)),
              Name("capacity"))))
          => .K
          ... </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
            "capacity" |-> C:Int
            "grid"     |-> _ORIGINAL_GRID:Val
            "total"    |-> (S:Int => S +Int gridCost(GS, C))
            "row"      |-> (PREV:Val => finalRow(GS, PREV))
            .Map,
            parent(0))
      0 |-> scope(GLOBALS:Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    requires C >Int 0
      andBool allRows(GS)
      andBool notBool ("sum" in_keys(GLOBALS))

  // Exact invocation theorem: normal lookup selects the exact closure body,
  // arguments are evaluated and bound by MPY-CALL, and return/pop execute.
  claim [max-fill]:
    <k> Call(Name("max_fill"), list(GS:ValSeq), C:Int)
          => gridCost(GS, C) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "max_fill" |->
          closureVal(
            ("grid", "capacity"),
            Assign(Name("total"), Int(0))
            Assign(Name("row"), Int(0))
            For(
              Name("row"),
              Name("grid"),
              AugAssign(
                Name("total"),
                "+",
                BinOp(
                  "//",
                  BinOp(
                    "-",
                    BinOp(
                      "+",
                      Call(Name("sum"), Name("row")),
                      Name("capacity")),
                    Int(1)),
                  Name("capacity"))))
            Return(Name("total")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires C >Int 0 andBool allRows(GS)
endmodule
