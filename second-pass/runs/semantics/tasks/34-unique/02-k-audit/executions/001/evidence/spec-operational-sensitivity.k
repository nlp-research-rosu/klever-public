requires "verification.k"

module UNIQUE-OPERATIONAL-SENSITIVITY
  imports UNIQUE-VERIFICATION

  // Body mutation: append every item, omitting the submitted membership guard.
  // On [1, 1] this mutated loop produces [1, 1], so the submitted loop summary
  // (which demands [1]) must no longer hold.
  claim [mutated-loop-rejected]:
    <k>
      #loop(
        list(vCons(1, vCons(1, .ValSeq))),
        Name("item"),
        Expr(
          Call(
            Attribute(Name("result"), "append"),
            Name("item"), .Exprs))
        .Stmts)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        .Map
          [ "l" <- list(vCons(1, vCons(1, .ValSeq))) ]
          [ "result" <- ref(0) ]
          [ "item" <- 99 => 1 ],
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
