requires "verification.k"

module AUDIT-WITNESS
  imports VERIFICATION

  // Ground witness for the prompt's second example.  The postcondition uses
  // explicit ValSeq values rather than the candidate's summary symbols.
  claim [example-5-6-3-4]:
    <k>
      #loadAll(Module(FuncDef("sort_even", Params("l"), sortEvenBody)))
      ~> Call(
           Name("sort_even"),
           list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ( 0 |-> list(vCons(3, vCons(6, vCons(5, vCons(4, .ValSeq)))))
        1 |-> list(vCons(5, vCons(3, .ValSeq)))
        2 |-> list(vCons(3, vCons(5, .ValSeq))) )
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
