requires "verification.k"

module SPEC-FRESH-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: "a.txt" is in the valid-name-txt domain and the
  // real program returns "Yes"; this deliberately demands the opposite result.
  claim [ground-valid-txt-returns-no]:
    <k>
      Call(Name("file_name_check"), str(strToCodes("a.txt")))
      =>
      str(strToCodes("No"))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "file_name_check" |->
          closureVal(
            ("file_name", .ParamNames),
            fileNameCheckBody,
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
