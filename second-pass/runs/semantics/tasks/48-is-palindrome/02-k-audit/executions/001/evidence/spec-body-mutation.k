requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "is_palindrome",
            Params("text"),
            Return(
              Compare(
                Name("text"),
                CmpOp(
                  "!=",
                  Subscript(
                    Name("text"),
                    Slice(
                      NoBound,
                      NoBound,
                      UnaryOp("-", Int(1)))))))
            .Stmts)))
      ~> Call(Name("is_palindrome"), str(IS:IntSeq))
    =>
      palindrome(IS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "is_palindrome" |->
          closureVal(
            "text",
            Return(
              Compare(
                Name("text"),
                CmpOp(
                  "!=",
                  Subscript(
                    Name("text"),
                    Slice(
                      NoBound,
                      NoBound,
                      UnaryOp("-", Int(1)))))))
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
