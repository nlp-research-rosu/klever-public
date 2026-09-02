requires "verification.k"

module IS-NESTED-LOOP-SPEC
  imports IS-NESTED-VERIFICATION

  claim [scan-loop]:
    <k>
      #loop(str(bCodes(BS:BSeq)), Name("char"), scanBody)
      ~> (Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts):Stmts
      ~> #endcall
      => scanState(I:Int, BS) ==Int 4
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
        "state" |-> I
        "char" |-> _CHAR:Val
        "string" |-> _INPUT:Val,
        parent(0)) => .Map)
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int 4
endmodule

module IS-NESTED-TOP-SPEC
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  claim [empty-input]:
    <k> Call(Name("is_nested"), str(bCodes(bNil))) => false </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [all-bracket-strings]:
    <k> Call(Name("is_nested"), str(bCodes(BS:BSeq))) => nested(BS) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
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
