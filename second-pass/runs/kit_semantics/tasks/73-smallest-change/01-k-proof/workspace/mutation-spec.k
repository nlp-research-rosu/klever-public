requires "mutation.k"

module MUTATION-SPEC
  imports MUTATION

  // This is the general loop theorem with only the body mutated.  It is
  // expected to fail under fixed execution.
  claim [skip-index-mutation]:
    <k>
      #while(
        Compare(
          Name("i"),
          CmpOp(
            "<",
            BinOp(
              "//",
              Call(Name("len"), Name("arr")),
              Int(2)))),
        mutantLoopBody)
      ~> (Return(Name("changes")) .Stmts):Stmts
      ~> #endcall
      => C +Int mismatchCount(VS, I, halfLen(VS))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> fixedBuiltins
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", mutantBody, 0),
             parent(-1))
      1 |-> scope(
             "arr" |-> list(VS:ValSeq)
             "changes" |-> C:Int
             "i" |-> I:Int,
             parent(0))
      =>
      -1 |-> fixedBuiltins
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", mutantBody, 0),
             parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allInts(VS)
      andBool 0 <=Int I
endmodule
