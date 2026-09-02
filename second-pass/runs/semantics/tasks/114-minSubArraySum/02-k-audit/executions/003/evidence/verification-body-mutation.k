requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // A mathematical integer sequence is embedded as the read-only ValSeq used
  // by the Python semantics.  Restricting the input this way states that every
  // element of nums is an integer.
  syntax ValSeq ::= intVals(IntSeq)
  rule intVals(.IntSeq)                => .ValSeq
  rule intVals(iCons(I:Int, R:IntSeq)) => vCons(I, intVals(R))

  // Preserve the IntSeq witness while symbolically iterating its embedding.
  // These are exact instances of MPY-LIST's two iterator rules and avoid
  // losing injectivity information behind an opaque intVals(R) term.
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
    [priority(30)]
  rule <k> #iterNext(list(intVals(iCons(I:Int, R:IntSeq))))
        => #iterYield(I, list(intVals(R))) ... </k>
    [priority(30)]

  // The function reads nums[0] before the loop.  This is the corresponding
  // instance of MPY-SUBSCRIPT's valSeqAt rule on the symbolic embedding.
  rule valSeqAt(intVals(iCons(I:Int, _R:IntSeq)), 0) => I
    [simplification]

  // Kadane's invariant:
  //   current = the minimum sum of a non-empty subarray ending immediately
  //             before the unprocessed suffix;
  //   smallest = the minimum sum of every non-empty subarray seen so far.
  // For the next integer I, the subarrays ending at I are the singleton [I]
  // and extensions of previously-ending subarrays.  Integer addition is
  // monotone, so the minimum new ending sum is min(I, current + I).
  syntax Int ::= chooseSmaller(Int, Int) [function, total]
  rule chooseSmaller(A:Int, B:Int) => A
    requires A <Int B
  rule chooseSmaller(A:Int, B:Int) => B
    requires A >=Int B

  syntax Int ::= nextCurrent(Int, Int) [function, total]
  rule nextCurrent(I:Int, C:Int) => chooseSmaller(I, C +Int I)

  syntax Int ::= kadaneCurrent(IntSeq, Int) [function, total]
  rule kadaneCurrent(.IntSeq, C:Int) => C
  rule kadaneCurrent(iCons(I:Int, R:IntSeq), C:Int)
    => kadaneCurrent(R, nextCurrent(I, C))

  syntax Int ::= kadaneSmallest(IntSeq, Int, Int) [function, total]
  rule kadaneSmallest(.IntSeq, _C:Int, B:Int) => B
  rule kadaneSmallest(iCons(I:Int, R:IntSeq), C:Int, B:Int)
    => kadaneSmallest(
         R,
         nextCurrent(I, C),
         chooseSmaller(nextCurrent(I, C), B))

  // The contract is defined only on non-empty sequences, exactly as in the
  // HumanEval prompt.  The first element seeds both invariant components, and
  // the remaining suffix is folded by the recurrence above.
  syntax Int ::= minSubArraySumSpec(IntSeq) [function]
  rule minSubArraySumSpec(iCons(H:Int, T:IntSeq))
    => kadaneSmallest(T, H, H)

  syntax Int ::= lastFrom(IntSeq, Int) [function, total]
  rule lastFrom(.IntSeq, LAST:Int) => LAST
  rule lastFrom(iCons(I:Int, R:IntSeq), _LAST:Int)
    => lastFrom(R, I)

  // Exact constructor form emitted for the loop body by py2mpy.py.
  syntax Stmts ::= "kadaneBody" [macro]
  rule kadaneBody =>
       Assign(
         Name("current"),
         BinOp("-", Name("current"), Name("value")))
       If(
         Compare(Name("value"), CmpOp("<", Name("current"))),
         Assign(Name("current"), Name("value")) .Stmts,
         .Stmts)
       If(
         Compare(Name("current"), CmpOp("<", Name("smallest"))),
         Assign(Name("smallest"), Name("current")) .Stmts,
         .Stmts)
       .Stmts

  // Exact constructor form emitted for solution.py, factored into macros only
  // to keep the reachability claim and its final module scope readable.
  syntax Stmts ::= "minSubArraySumBody" [macro]
  rule minSubArraySumBody =>
       Expr(
         Str(
           "\n    Given an array of integers nums, find the minimum sum of any non-empty\n    sub-array of nums.\n    "))
       Assign(Name("smallest"), Subscript(Name("nums"), Int(0)))
       Assign(Name("current"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("nums"), kadaneBody)
       Return(Name("smallest"))
       .Stmts

  syntax Stmt ::= "minSubArraySumDef" [macro]
  rule minSubArraySumDef =>
       FuncDef(
         "minSubArraySum",
         Params("nums", .ParamNames),
         minSubArraySumBody)

  syntax Val ::= "minSubArraySumClosure" [macro]
  rule minSubArraySumClosure =>
       closureVal(
         ("nums", .ParamNames),
         minSubArraySumBody,
         0)
endmodule

// This module adds the loop theorem as a verified summary rule.  prove.sh first
// proves the identical reachability claim against VERIFICATION-BASE (where this
// rule is absent), then uses this module to prove the whole translated function.
module VERIFICATION
  imports VERIFICATION-BASE

  rule <k>
         #loop(
           list(intVals(iCons(I:Int, R:IntSeq))),
           Name("value"),
           kadaneBody)
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           (("nums" |-> INPUT:Val)
            ("smallest" |-> B:Int)
            ("current" |-> C:Int)
            ("value" |-> _OLD:Val))
             =>
           (("nums" |-> INPUT)
            ("smallest" |->
               kadaneSmallest(iCons(I, R), C, B))
            ("current" |->
               kadaneCurrent(iCons(I, R), C))
            ("value" |-> lastFrom(R, I))),
           parent(0))
         ...
       </scopes>
    [priority(30)]
endmodule
