requires "witness-fixed.k"

module AUDIT-WITNESS-FIXED-TRUE-SPEC
  imports AUDIT-WITNESS-FIXED

  claim
    <k>
      #loop(
        list(vCons(str(iCons(97, iCons(97, .IntSeq))), .ValSeq)),
        Name("word"),
        filterBody)
      ~> Name("word")
    =>
      str(iCons(97, iCons(97, .IntSeq))) ~> .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      1  |-> (scope(
                     "lst" |-> list(vCons(
                                      str(iCons(97, iCons(97, .IntSeq))),
                                      .ValSeq))
                     "even_words" |-> ref(0),
                     parent(0))
              =>
              scope(
                 "lst" |-> list(vCons(
                                  str(iCons(97, iCons(97, .IntSeq))),
                                  .ValSeq))
                 "even_words" |-> ref(0)
                 "word" |-> str(iCons(97, iCons(97, .IntSeq))),
                 parent(0)))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
    =>
      0 |-> list(vCons(
                   str(iCons(97, iCons(97, .IntSeq))),
                   .ValSeq))
    </heap>
endmodule
