requires "04_witness_extension.k"

module SEARCH-BRIDGE-CONTEXT-WITNESS
  imports SEARCH-WITNESS-EXTENSION

  // The bridge accepts an arbitrary continuation and does not preserve the
  // loop's writes to count/value/item. For conceptual input [1], this closure
  // should return count=1 after the real loop, but the bridge skips the loop
  // and leaves the pre-loop count=99.
  claim
    <k> Call(Name("observe"), list(oneSeq), .Exprs) => 99 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "observe" |-> closureVal(
               "lst", .ParamNames,
               Assign(Name("result"), UnaryOp("-", Int(1)))
               Assign(Name("count"), Int(99))
               For(Name("value"), Name("lst"), #outerBody)
               Return(Name("count")) .Stmts,
               0),
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
