requires "verification.k"

module UNICODE-INTSEQ-SPEC
  imports VERIFICATION

  // U+00E9 followed by ".txt": non-Latin first code, hence "No".
  claim [unicode-first-letter]:
    <k>
      Call(
        Name("file_name_check"),
        str(iCons(233,
          iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))))
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

  // ASCII "a", four fullwidth digits U+FF11..U+FF14, then ".txt":
  // the prompt counts only ASCII '0'..'9', hence "Yes".
  claim [unicode-nonascii-digits]:
    <k>
      Call(
        Name("file_name_check"),
        str(iCons(97,
          iCons(65297, iCons(65298, iCons(65299, iCons(65300,
          iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))))))))
      =>
      str(strToCodes("Yes"))
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
