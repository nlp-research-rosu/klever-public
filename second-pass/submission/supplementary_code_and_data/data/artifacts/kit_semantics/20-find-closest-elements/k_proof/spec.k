requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [inner-loop]:
    <k>
      #loop(list(REST:ValSeq), Name("item2"), innerBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "find_closest_elements"
               |-> closureVal(
                     ("numbers", .ParamNames),
                     findBody,
                     0),
             parent(-1))
      1 |-> scope(
             "numbers" |-> NUMBERS:Val
             "items"   |-> ITEMSREF:Val
             "item1"   |-> ITEM1:Val
             "item2"   |-> (OLD2:Val => lastItem(REST, OLD2))
             "closest" |->
               ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq)))
                 =>
                 tuple(
                   vCons(
                     innerFirst(ITEM1, REST, A, B),
                     vCons(
                       innerSecond(ITEM1, REST, A, B),
                       .ValSeq))) ),
             parent(0))
    </scopes>
    requires ITEM1
       ==K tuple(
             vCons(
               itemIndex(ITEM1),
               vCons(itemFloat(ITEM1), .ValSeq)))
     andBool allFloatItems(REST)

  claim [outer-loop]:
    <k>
      #loop(list(REST:ValSeq), Name("item1"), outerBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "find_closest_elements"
               |-> closureVal(
                     ("numbers", .ParamNames),
                     findBody,
                     0),
             parent(-1))
      1 |-> scope(
             "numbers" |-> NUMBERS:Val
             "items"   |-> ref(H:Int)
             "item1"   |-> (OLD1:Val => ?FINAL1:Val)
             "item2"   |-> (OLD2:Val => ?FINAL2:Val)
             "closest" |->
               ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq)))
                 =>
                 tuple(
                   vCons(
                     outerFirst(REST, ALL:ValSeq, A, B),
                     vCons(
                       outerSecond(REST, ALL, A, B),
                       .ValSeq))) ),
             parent(0))
    </scopes>
    <heap> H |-> list(ALL) ... </heap>
    requires allFloatItems(REST)
     andBool allFloatItems(ALL)

  claim [find-closest]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("find_closest_elements"),
           (list(vCons(F0:Float, vCons(F1:Float, REST:ValSeq))), .Exprs))
      =>
      tuple(
        vCons(
          outerFirst(
            enumVS(vCons(F0, vCons(F1, REST)), 0),
            enumVS(vCons(F0, vCons(F1, REST)), 0),
            orderedFirst(F0, F1),
            orderedSecond(F0, F1)),
          vCons(
            outerSecond(
              enumVS(vCons(F0, vCons(F1, REST)), 0),
              enumVS(vCons(F0, vCons(F1, REST)), 0),
              orderedFirst(F0, F1),
              orderedSecond(F0, F1)),
            .ValSeq)))
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
      0 |-> list(enumVS(vCons(F0, vCons(F1, REST)), 0))
      1 |-> list(enumVS(vCons(F0, vCons(F1, REST)), 0))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatVS(REST)
endmodule
