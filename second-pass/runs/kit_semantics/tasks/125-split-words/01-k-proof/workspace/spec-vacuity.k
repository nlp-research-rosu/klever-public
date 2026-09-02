requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: split_words("abcdef") returns 3, not 4.
  claim [false-count-result]:
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
      => 4
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "split_words" |-> closureVal(("txt", .ParamNames), splitWordsBody, 0),
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
