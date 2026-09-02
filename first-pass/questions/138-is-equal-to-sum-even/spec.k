requires "verification.k"

module IS-EQUAL-TO-SUM-EVEN-SPEC
  imports IS-EQUAL-TO-SUM-EVEN-VERIFICATION

  claim
    <k>
      FuncDef("is_equal_to_sum_even", Params("n"),
        Return(BoolOp("and",
          Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
          Compare(Name("n"), CmpOp(">=", Int(8))))))
      Assign(Name("result"), Call(Name("is_equal_to_sum_even"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_equal_to_sum_even" <- ?_:Val ]
                       [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool (pyMod(N, 2) ==Int 0) andBool (N >=Int 8)
    [all-path]
endmodule
