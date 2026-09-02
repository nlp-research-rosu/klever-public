requires "mutation-verification.k"

module SPEC-BODY-MUTATION
  imports MUTATION-VERIFICATION

  // Expected failure: the mutated body returns 0 for "abcdef", not 3.
  claim [body-sensitive-count]:
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
      0  |-> scope(
               "split_words" |-> closureVal(
                 ("txt", .ParamNames),
                 mutatedSplitWordsBody,
                 0
               ),
               parent(-1)
             )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(
               iCons(97,
                 iCons(98,
                   iCons(99,
                     iCons(100,
                       iCons(101,
                         iCons(102, .IntSeq))))))
             ),
             .ValSeq
           )
         )
         1 |-> list(
           vCons(
             str(
               iCons(97,
                 iCons(98,
                   iCons(99,
                     iCons(100,
                       iCons(101,
                         iCons(102, .IntSeq))))))
             ),
             .ValSeq
           )
         )
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
