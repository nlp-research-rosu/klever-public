requires "verification.k"

module FILTER-SPEC-LOOP-ONLY
  imports FILTER-VERIFICATION

  claim [loop-target]:
    <k> #loop(list(strVals(SS:StrSeq)), Name("string"), filterLoopBody)
         ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        (.Map [ "strings" <- list(strVals(ORIG:StrSeq)) ]
              [ "substring" <- str(P:IntSeq) ]
              [ "result" <- ref(H:Int) ]
              [ "string" <- str(CUR:IntSeq) ])
        =>
        (.Map [ "strings" <- list(strVals(ORIG)) ]
              [ "substring" <- str(P) ]
              [ "result" <- ref(H) ]
              [ "string" <- str(lastCodes(CUR, SS)) ]),
        parent(0)) ...
    </scopes>
    <heap>
      ... H:Int |-> list(ACC:ValSeq
                         => filterAccStrings(ACC, P, SS)) ...
    </heap>
endmodule
