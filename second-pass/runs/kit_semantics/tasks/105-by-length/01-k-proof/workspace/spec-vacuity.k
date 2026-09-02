requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: append an extra "Wrong" element to every result.
  claim [false-by-length]:
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
      (?H
        |-> list(
              valSeqConcat(
                byLengthVS(VS),
                vCons(str(strToCodes("Wrong")), .ValSeq))))
      ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
