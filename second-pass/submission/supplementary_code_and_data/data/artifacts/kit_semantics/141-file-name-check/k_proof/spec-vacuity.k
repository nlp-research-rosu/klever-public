requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: "a.txt" satisfies this precondition, but returns Yes.
  claim [valid-txt-returns-no]:
    <k>
      Call(Name("file_name_check"), str(iCons(C:Int, REST:IntSeq)))
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
    requires cntSub(iCons(C, REST), strToCodes(".")) ==Int 1
     andBool strContains(
       iCons(C, .IntSeq),
       strToCodes("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".txt"))
     andBool decimalDigitCount(iCons(C, REST)) <=Int 3
endmodule
