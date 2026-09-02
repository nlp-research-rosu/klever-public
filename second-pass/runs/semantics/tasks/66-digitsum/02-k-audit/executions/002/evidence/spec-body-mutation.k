requires "verification-body-mutation.k"

module DIGIT-SUM-LOOP-SPEC
  imports DIGIT-SUM-VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(str(S:IntSeq), Name("char"), digitSumLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => A:Int +Int digitSumSpec(S)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      ( 1 |->
        scope(
          "s" |-> INPUT:Val
          "result" |-> A
          "char" |-> OLDCHAR:Val
          "code" |-> OLDCODE:Val,
          parent(0)
        )
      )
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule

module DIGIT-SUM-INITIALIZATION-SPEC
  imports DIGIT-SUM-VERIFICATION

  claim [initialization]:
    <k>
      Call(
        closureVal(("s", .ParamNames), digitSumBody, 0),
        (str(S:IntSeq), .Exprs)
      )
      =>
      #loop(str(S), Name("char"), digitSumLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      1 |->
        scope(
          "s" |-> str(S)
          "result" |-> 0
          "char" |-> str(.IntSeq)
          "code" |-> 0,
          parent(0)
        )
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List
      => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module DIGIT-SUM-ENTRY-SPEC
  imports DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA

  claim [entry-point]:
    <k>
      Call(
        closureVal(("s", .ParamNames), digitSumBody, 0),
        (str(S:IntSeq), .Exprs)
      )
      => digitSumSpec(S)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
