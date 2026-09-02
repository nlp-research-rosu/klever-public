requires "spec.k"

module FRESH-FALSE-RESULT
  imports SPEC

  // Fresh audit mutation.  The satisfying input [1] really returns ["One"],
  // while this postcondition requires the returned heap object to be [].
  claim [one-does-not-return-empty]:
    <k>
      Call(Name("by_length"), (list(vCons(1, .ValSeq)), .Exprs))
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
      (?H |-> list(.ValSeq)) ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
