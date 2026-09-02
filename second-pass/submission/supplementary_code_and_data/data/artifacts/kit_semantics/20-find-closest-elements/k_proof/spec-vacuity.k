requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result-shape]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("find_closest_elements"),
           (list(vCons(F0:Float, vCons(F1:Float, .ValSeq))), .Exprs))
      =>
      tuple(
        vCons(
          orderedFirst(F0, F1),
          vCons(
            orderedSecond(F0, F1),
            vCons(noneV, .ValSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        =>
        0 |-> scope(
               "find_closest_elements"
                 |-> closureVal(
                       ("numbers", .ParamNames),
                       findBody,
                       0),
               parent(-1)) )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               tuple(vCons(0, vCons(F0, .ValSeq))),
               vCons(
                 tuple(vCons(1, vCons(F1, .ValSeq))),
                 .ValSeq)))
      1 |-> list(
             vCons(
               tuple(vCons(0, vCons(F0, .ValSeq))),
               vCons(
                 tuple(vCons(1, vCons(F1, .ValSeq))),
                 .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
