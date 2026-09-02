requires "reference-semantics/semantics.k"

module BRANCH-WITNESS-FIXED
  imports MPY

  claim [path1-false-forces-first-then]:
    <k>
      #branch(
        false,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts) ~> #endcall
      =>
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) ~> #endcall
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "$proofPath" |-> 1
        "txt" |-> str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [path2-true-forces-first-else]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts) ~> #endcall
      =>
        #endcall
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "$proofPath" |-> 2
        "txt" |-> str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [path3-true-forces-first-else]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
        .Stmts) ~> #endcall
      =>
        #endcall
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "$proofPath" |-> 3
        "txt" |-> str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [path2-false-forces-second-then]:
    <k>
      #branch(
        false,
        Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
        .Stmts) ~> #endcall
      =>
        Return(Call(Attribute(Name("txt"), "split"), Str(","))) ~> #endcall
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "$proofPath" |-> 2
        "txt" |-> str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [path3-true-forces-second-else]:
    <k>
      #branch(
        true,
        Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
        .Stmts) ~> #endcall
      =>
        #endcall
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "$proofPath" |-> 3
        "txt" |-> str(iCons(97, iCons(44, iCons(98, .IntSeq)))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
