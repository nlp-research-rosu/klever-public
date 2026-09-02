requires "verification.k"

module SPEC
  imports VERIFICATION

  // At a loop head, trace is a finite valid trace from start through n, and
  // odds contains exactly the odd trace elements before the current n.
  // The RHS existentially describes the finite trace present if the loop
  // terminates; it does not assert that a terminal trace exists for every n.
  claim [collatz-loop]:
    <k>
      #while(
        Compare(Name("n"), CmpOp(">", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
          Expr(Call(Attribute(Name("odds"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))))
        Expr(Call(Attribute(Name("trace"), "append"), Name("n"))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "n"     |-> (N:Int => 1)
        "odds"  |-> ref(HO:Int)
        "start" |-> S:Int
        "trace" |-> ref(HT:Int),
        parent(0))
      ...
    </scopes>
    <heap>
      HO |-> list(A:ValSeq => ?AF:ValSeq)
      HT |-> list(T:ValSeq => ?TF:ValSeq)
    </heap>
    requires N >Int 0
     andBool validCollatzTrace(T)
     andBool notBool (T ==K .ValSeq)
     andBool traceFirstInt(T) ==Int S
     andBool traceLastInt(T) ==Int N
     andBool A ==K oddWithoutLast(T)
    ensures validCollatzTrace(?TF)
     andBool traceFirstInt(?TF) ==Int S
     andBool traceLastInt(?TF) ==Int 1
     andBool ?AF ==K oddWithoutLast(?TF)

  // Exact target invocation: define the translated function in module scope,
  // resolve that binding, bind N to parameter n, and execute the real body.
  // The existential trace is an internal finite execution witness.
  claim [get-odd-collatz]:
    <k>
      FuncDef("get_odd_collatz", Params("n"),
        Assign(Name("odds"), ListExpr(.Exprs))
        Assign(Name("start"), Name("n"))
        Assign(Name("trace"), ListExpr(Name("start")))
        While(Compare(Name("n"), CmpOp(">", Int(1))),
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
            Expr(Call(Attribute(Name("odds"), "append"), Name("n")))
            Assign(
              Name("n"),
              BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))))
          Expr(Call(Attribute(Name("trace"), "append"), Name("n"))))
        Expr(Call(Attribute(Name("odds"), "append"), Int(1)))
        Expr(Call(Attribute(Name("odds"), "sort"), .Exprs))
        Return(Name("odds")))
      ~> Call(Name("get_odd_collatz"), (N:Int, .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "get_odd_collatz" |->
          closureVal(
            "n",
            Assign(Name("odds"), ListExpr(.Exprs))
            Assign(Name("start"), Name("n"))
            Assign(Name("trace"), ListExpr(Name("start")))
            While(Compare(Name("n"), CmpOp(">", Int(1))),
              If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
                Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
                Expr(Call(Attribute(Name("odds"), "append"), Name("n")))
                Assign(
                  Name("n"),
                  BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))))
              Expr(Call(Attribute(Name("trace"), "append"), Name("n"))))
            Expr(Call(Attribute(Name("odds"), "append"), Int(1)))
            Expr(Call(Attribute(Name("odds"), "sort"), .Exprs))
            Return(Name("odds")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        sortVS(
          valSeqConcat(
            oddWithoutLast(?TF),
            vCons(1, .ValSeq))))
      1 |-> list(?TF:ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0
    ensures validCollatzTrace(?TF)
     andBool traceFirstInt(?TF) ==Int N
     andBool traceLastInt(?TF) ==Int 1
endmodule
