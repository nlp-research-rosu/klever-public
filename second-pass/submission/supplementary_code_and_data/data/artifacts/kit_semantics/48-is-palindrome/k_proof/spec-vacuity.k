requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the empty string is a palindrome, but the destination
  // below requires the observed result to be false.
  claim [empty-is-not-palindrome]:
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
