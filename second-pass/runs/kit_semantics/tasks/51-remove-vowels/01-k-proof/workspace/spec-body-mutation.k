requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changed implementation: always return the empty string.
  // The original postcondition must reject it for the consonant input "b".
  claim [changed-body-rejected]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "remove_vowels",
            Params("text"),
            Return(Str("")) .Stmts)
          .Stmts))
      ~> Call(
           Name("remove_vowels"),
           (str(iCons(98, .IntSeq)), .Exprs))
      => str(removeVowelsFrom(iCons(98, .IntSeq), .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        .Map
        => .Map [
             "remove_vowels"
             <- closureVal(
                  "text",
                  Return(Str("")) .Stmts,
                  0)
           ],
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
