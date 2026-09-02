requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inner insertion loop as an independent local-state theorem.  The framed
  // continuation is arbitrary and is preserved.
  claim [anti-shuffle-inner-loop]:
    <k>
      #loop(str(IS:IntSeq), Name("old_char"), antiInnerBody())
      ~> antiPostInsert()
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      1 |-> scope(
             ("s" |-> str(ORIGINAL:IntSeq))
             ("result" |-> str(R:IntSeq))
             ("word" |-> str(WORD:IntSeq))
             ("char" |-> str(iCons(C:Int, .IntSeq)))
             ("new_word" |-> str(A:IntSeq))
             ("inserted" |-> B:Bool)
             ("old_char" |-> str(OLD:IntSeq)),
             parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      1 |-> scope(
             ("s" |-> str(ORIGINAL:IntSeq))
             ("result" |-> str(R:IntSeq))
             ("word" |-> str(insertGo(IS, C, A, B)))
             ("char" |-> str(iCons(C:Int, .IntSeq)))
             ("new_word" |-> str(insertGo(IS, C, A, B)))
             ("inserted" |-> true)
             ("old_char" |-> str(?FINALOLD:IntSeq)),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Outer character loop.  The relation in the postcondition is also the
  // invariant threaded through the inner-loop claim above.
  claim [anti-shuffle-outer-loop]:
    <k>
      #loop(str(S:IntSeq), Name("char"), antiOuterBody())
      ~> antiTail()
      ~> #endcall
      => str(antiGo(S, R, W))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      1 |-> scope(
             ("s" |-> str(ORIGINAL:IntSeq))
             ("result" |-> str(R:IntSeq))
             ("word" |-> str(W:IntSeq))
             ("char" |-> str(CURRENT:IntSeq))
             ("new_word" |-> str(NEW:IntSeq))
             ("inserted" |-> INSERTED:Bool)
             ("old_char" |-> str(OLD:IntSeq)),
             parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Whole-program claim: load the exact translated definition, resolve its
  // public name, execute the real body, and constrain the returned string.
  claim [anti-shuffle]:
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("anti_shuffle"), str(INPUT:IntSeq), .Exprs)
      => str(antiGo(INPUT, .IntSeq, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
