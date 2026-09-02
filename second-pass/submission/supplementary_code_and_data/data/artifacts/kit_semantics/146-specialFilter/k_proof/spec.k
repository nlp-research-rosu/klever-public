requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop circularity: from any loop head, count gains exactly the number of
  // qualifying integers in the unbounded remaining sequence.
  claim [filter-loop]:
    <k>
      #loop(list(INPUT:ValSeq), Name("num"), filterBody())
      ~> (Return(Name("count")) .Stmts)
      ~> #endcall
      ~> .K
      =>
      (Return(Name("count")) .Stmts)
      ~> #endcall
      ~> .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "specialFilter"
              |-> closureVal("nums", specialFilterStmts(), 0),
              parent(-1))
       1 |-> scope(
              "nums"  |-> list(ORIGINAL:ValSeq)
              "count" |-> (COUNT:Int => COUNT +Int specialCount(INPUT))
              "num"   |-> (OLDNUM:Val => ?FINALNUM:Val)
              "text"  |-> (str(OLDTEXT:IntSeq) => str(?FINALTEXT:IntSeq)),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(INPUT)

  // Required target: load the exact solution body and call it on every
  // arbitrary finite integer list represented by the supplied semantics.
  claim [special-filter]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            specialFilterStmts())))
      ~> Call(Name("specialFilter"), list(INPUT:ValSeq))
      => specialCount(INPUT)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "specialFilter"
                 |-> closureVal("nums", specialFilterStmts(), 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(INPUT)
endmodule
