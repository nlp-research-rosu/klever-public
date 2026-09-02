requires "auditor-body-mutation.k"

module AUDITOR-BODY-MUTATION-SPEC
  imports AUDITOR-BODY-MUTATION

  // This should fail: the mutated body returns 0, while the real body returns 3.
  claim [auditor-body-sensitive]:
    <k>
      Call(
        Name("split_words"),
        str(
          iCons(97,
            iCons(98,
              iCons(99,
                iCons(100,
                  iCons(101,
                    iCons(102, .IntSeq))))))
        ),
        .Exprs
      )
      => 3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "split_words" |-> closureVal(
          ("txt", .ParamNames),
          auditorMutatedBody,
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
