requires "auditor-verification-body-mutant.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  claim [initial-body-step]:
    <k> oddCountLoopBody
         ~> #loopLbl(#loop(list(REST:ValSeq), Name("digits"), oddCountLoopBody))
         ~> (Return(Name("result")) .Stmts) ~> #endcall
      => #loop(list(REST), Name("digits"), oddCountLoopBody)
         ~> (Return(Name("result")) .Stmts) ~> #endcall </k>
    <env> 1 </env>
    <scopes>
        -1 |-> builtinsScope
        0  |-> scope(.Map [ "odd_count" <- closureVal("lst", oddCountBody, 0) ], parent(-1))
        1  |-> (scope(.Map
                       [ "lst"    <- list(ORIGINAL:ValSeq) ]
                       [ "result" <- ref(0) ]
                       [ "digits" <- str(CS:IntSeq) ],
                     parent(0))
                => scope(.Map
                           [ "lst"        <- list(ORIGINAL) ]
                           [ "result"     <- ref(0) ]
                           [ "digits"     <- str(CS) ]
                           [ "count"      <- oddDigitCount(CS) ]
                           [ "count_text" <- str(strToCodes(Int2String(oddDigitCount(CS)))) ],
                         parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(ACC:ValSeq
                 => valSeqConcat(
                      ACC,
                      vCons(str(oddCountMessage(oddDigitCount(CS))), .ValSeq)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitString(str(CS))

  // Fixed-semantics connection theorem for VERIFICATION's exact bridge.
  claim [body-step]:
    <k> oddCountLoopBody
         ~> #loopLbl(#loop(list(REST:ValSeq), Name("digits"), oddCountLoopBody))
         ~> (Return(Name("result")) .Stmts) ~> #endcall
      => #loop(list(REST), Name("digits"), oddCountLoopBody)
         ~> (Return(Name("result")) .Stmts) ~> #endcall </k>
    <env> 1 </env>
    <scopes>
        -1 |-> builtinsScope
        0  |-> scope(.Map [ "odd_count" <- closureVal("lst", oddCountBody, 0) ], parent(-1))
        1  |-> scope(.Map
                      [ "lst"        <- list(ORIGINAL:ValSeq) ]
                      [ "result"     <- ref(0) ]
                      [ "digits"     <- str(CS:IntSeq) ]
                      [ "count"      <- (OLD_COUNT:Val => oddDigitCount(CS)) ]
                      [ "count_text" <- (OLD_TEXT:Val => str(strToCodes(Int2String(oddDigitCount(CS))))) ],
                    parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(ACC:ValSeq
                 => valSeqConcat(
                      ACC,
                      vCons(str(oddCountMessage(oddDigitCount(CS))), .ValSeq)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitString(str(CS))
endmodule
