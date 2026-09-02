requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  claim [inner-loop-connection]:
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
             "numbers" |-> _NUMBERS:Val
             "items"   |-> _ITEMSREF:Val
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
endmodule
