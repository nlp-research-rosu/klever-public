requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: return str(x) without shifting it.
  claim [mutated-body]:
    <k>
      Call(Name("circular_shift"), (12, 1, .Exprs))
      => circularShiftResult(12, 1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
              "circular_shift" |->
                closureVal(
                  ("x", "shift", .ParamNames),
                  Assign(
                    Name("s"),
                    Call(Name("str"), (Name("x"), .Exprs)))
                  Return(Name("s"))
                  .Stmts,
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
