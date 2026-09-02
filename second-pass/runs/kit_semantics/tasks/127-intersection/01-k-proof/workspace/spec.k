requires "verification.k"

module SPEC
  imports VERIFICATION

  // Once a divisor has been seen, every remaining iteration preserves true.
  claim [divisor-loop-true]:
    <k>
      #while(Compare(Name("divisor"), CmpOp("<", Name("length"))),
             If(Compare(BinOp("%", Name("length"), Name("divisor")),
                        CmpOp("==", Int(0))),
                Assign(Name("has_divisor"), Bool(true)) .Stmts,
                .Stmts)
             Assign(Name("divisor"),
                    BinOp("+", Name("divisor"), Int(1)))
             .Stmts)
      => .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        "divisor"     |-> (D => N)
        "end"         |-> E
        "has_divisor" |-> true
        "interval1"   |-> IV1
        "interval2"   |-> IV2
        "length"      |-> N
        "start"       |-> S,
        PARENT)
      ...
    </scopes>
    <scopeLoc> NEXT </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HNEXT </heapLoc>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT </exit-code>
    requires D >=Int 2 andBool D <=Int N

  // If no divisor has yet been seen, scanning D .. N-1 returns the exact
  // recursive Boolean summary scanHasDivisor(false, N, D).
  claim [divisor-loop-false]:
    <k>
      #while(Compare(Name("divisor"), CmpOp("<", Name("length"))),
             If(Compare(BinOp("%", Name("length"), Name("divisor")),
                        CmpOp("==", Int(0))),
                Assign(Name("has_divisor"), Bool(true)) .Stmts,
                .Stmts)
             Assign(Name("divisor"),
                    BinOp("+", Name("divisor"), Int(1)))
             .Stmts)
      => .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        "divisor"     |-> (D => N)
        "end"         |-> E
        "has_divisor" |-> (false => scanHasDivisor(false, N, D))
        "interval1"   |-> IV1
        "interval2"   |-> IV2
        "length"      |-> N
        "start"       |-> S,
        PARENT)
      ...
    </scopes>
    <scopeLoc> NEXT </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HNEXT </heapLoc>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT </exit-code>
    requires D >=Int 2 andBool D <=Int N

  // Whole-program claim: exact translated definition, exact entry point, all
  // valid integer intervals, and a result characterized by proper divisors.
  claim [intersection-correct]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("intersection"),
              TupleExpr(Int(A0), Int(A1)),
              TupleExpr(Int(B0), Int(B1)))
      => primeResult(overlapLength(A0, A1, B0, B1))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A0 <=Int A1 andBool B0 <=Int B1
endmodule
