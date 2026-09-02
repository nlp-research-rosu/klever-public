requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [collect-loop]:
    <k>
      #loop(list(VS:ValSeq), Name("value"), collectLoopBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("arr" |-> list(WHOLE:ValSeq)
         "digit" |-> D:Int
         "name" |-> N:Val
         "result" |-> ref(H:Int)
         "value" |-> (OLD:Val => ?FINAL:Val)),
        parent(0))
      ...
    </scopes>
    <heap>
      ...
      H |-> (list(ACC:ValSeq) => list(collectAcc(VS, D, N, ACC)))
      ...
    </heap>
    requires allInts(VS)

  claim [by-length]:
    <k>
      Call(Name("by_length"), (list(VS:ValSeq), .Exprs))
      => ref(?H:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("collect_digit"
           |-> closureVal(
                 ("arr", "digit", "name", .ParamNames),
                 collectDigitBody,
                 0)
         "by_length"
           |-> closureVal(("arr", .ParamNames), byLengthBody, 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (?H |-> list(byLengthVS(VS))) ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
