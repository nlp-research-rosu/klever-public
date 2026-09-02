requires "verification.k"

module FIB-SPEC-VACUITY
  imports FIB-VERIFICATION

  // The result of the remaining loop is the mathematical fold fibRun.
  claim [fib-loop]:
    <k>
      #loop(
        rangeObj(I:Int, N:Int, 1),
        Name("_"),
        Assign(
          TupleExpr(Name("a"), Name("b")),
          TupleExpr(Name("b"), BinOp("+", Name("a"), Name("b")))))
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (REST:Map
       L |-> scope(
         ("n" |-> N
          "a" |-> A:Int
          "b" |-> B:Int
          "_" |-> OLD_INDEX:Int),
         parent(0)))
      =>
      (REST
       L |-> scope(
         ("n" |-> N
          "a" |-> fibRun(A, B, I, N)
          "b" |-> ?FINAL_B:Int
          "_" |-> ?FINAL_INDEX:Int),
         parent(0)))
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXIT:Int </exit-code>
    [circularity]

  // For every natural-number input, running the translated function returns
  // the mathematical Fibonacci value.
  claim [fib-all-natural]:
    <k>
      #loadAll(fibProgram) ~> Call(Name("fib"), Int(N:Int))
      =>
      fibSpec(N) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("fib" |-> fibClosure, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [depends(FIB-SPEC-VACUITY.fib-loop)]
endmodule
