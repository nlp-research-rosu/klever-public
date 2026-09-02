requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant: the actual loop returns a digit sequence satisfying the
  // guarded base-2 recurrence from its current integer and accumulator.
  claim [binary-loop]:
    <k>
      #while(
        Compare(Name("decimal"), CmpOp("!=", Int(0))),
        Assign(
          Name("binary"),
          BinOp(
            "+",
            Call(
              Name("chr"),
              BinOp(
                "+",
                Int(48),
                BinOp("%", Name("decimal"), Int(2)))),
            Name("binary")))
        Assign(
          Name("decimal"),
          BinOp("//", Name("decimal"), Int(2))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0  |-> scope(
        "decimal_to_binary" |-> FUNCTION:Val,
        parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
        "binary"  |-> (str(ACC:IntSeq) => str(?OUT:IntSeq))
        "decimal" |-> (N:Int => 0),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    ensures binRel(N, ACC, ?OUT)

  // Exact invocation of the translated function body under its real binding.
  // The complete result code sequence is constrained by decimalResultRel.
  claim [decimal-to-binary]:
    <k>
      Call(
        Name("decimal_to_binary"),
        (N:Int, .Exprs))
      => str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "decimal_to_binary" |->
          closureVal(
            ("decimal", .ParamNames),
            Assign(Name("binary"), Str("db"))
            If(
              Compare(Name("decimal"), CmpOp("==", Int(0))),
              Assign(
                Name("binary"),
                BinOp("+", Str("0"), Name("binary"))),
              .Stmts)
            While(
              Compare(Name("decimal"), CmpOp("!=", Int(0))),
              Assign(
                Name("binary"),
                BinOp(
                  "+",
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      Int(48),
                      BinOp("%", Name("decimal"), Int(2)))),
                  Name("binary")))
              Assign(
                Name("decimal"),
                BinOp("//", Name("decimal"), Int(2))))
            Return(
              BinOp(
                "+",
                Str("db"),
                Name("binary"))),
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
    requires N >=Int 0
    ensures decimalResultRel(N, ?CODES)
endmodule
