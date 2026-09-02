requires "verification.k"

module SPEC-REVIEWER-FALSE
  imports VERIFICATION

  // Reviewer-authored false result obligation. The entry state is satisfiable:
  // it calls the exact submitted body on the empty semantic string. The real
  // result is true, while this destination deliberately requires false.
  claim [empty-must-be-false]:
    <k>
      #loadAll(
        Module(
          FuncDef("is_palindrome", Params("text"),
            Return(
              Compare(
                Name("text"),
                CmpOp(
                  "==",
                  Subscript(
                    Name("text"),
                    Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
          Assign(
            Name("__result"),
            Call(Name("is_palindrome"), str(.IntSeq)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
          "is_palindrome" |->
            closureVal(
              ("text", .ParamNames),
              Return(
                Compare(
                  Name("text"),
                  CmpOp(
                    "==",
                    Subscript(
                      Name("text"),
                      Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))
              .Stmts,
              0)
          "__result" |-> false,
          parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
