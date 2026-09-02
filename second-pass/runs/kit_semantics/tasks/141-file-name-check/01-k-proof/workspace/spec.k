requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [empty-name]:
    <k>
      Call(Name("file_name_check"), str(.IntSeq))
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

  claim [bad-dot-count]:
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
    requires cntSub(iCons(C, REST), strToCodes(".")) =/=Int 1

  claim [bad-initial]:
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
     andBool notBool strContains(
       iCons(C, .IntSeq),
       strToCodes("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))

  claim [bad-extension]:
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
     andBool notBool allowedFileExtension(iCons(C, REST))

  claim [too-many-digits-txt]:
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
     andBool decimalDigitCount(iCons(C, REST)) >Int 3

  claim [too-many-digits-exe]:
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
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".txt"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".exe"))
     andBool decimalDigitCount(iCons(C, REST)) >Int 3

  claim [too-many-digits-dll]:
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
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".txt"))
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".exe"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".dll"))
     andBool decimalDigitCount(iCons(C, REST)) >Int 3

  claim [valid-name-txt]:
    <k>
      Call(Name("file_name_check"), str(iCons(C:Int, REST:IntSeq)))
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
    requires cntSub(iCons(C, REST), strToCodes(".")) ==Int 1
     andBool strContains(
       iCons(C, .IntSeq),
       strToCodes("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".txt"))
     andBool decimalDigitCount(iCons(C, REST)) <=Int 3

  claim [valid-name-exe]:
    <k>
      Call(Name("file_name_check"), str(iCons(C:Int, REST:IntSeq)))
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
    requires cntSub(iCons(C, REST), strToCodes(".")) ==Int 1
     andBool strContains(
       iCons(C, .IntSeq),
       strToCodes("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".txt"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".exe"))
     andBool decimalDigitCount(iCons(C, REST)) <=Int 3

  claim [valid-name-dll]:
    <k>
      Call(Name("file_name_check"), str(iCons(C:Int, REST:IntSeq)))
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
    requires cntSub(iCons(C, REST), strToCodes(".")) ==Int 1
     andBool strContains(
       iCons(C, .IntSeq),
       strToCodes("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".txt"))
     andBool notBool fileExtensionIs(
       iCons(C, REST), strToCodes(".exe"))
     andBool fileExtensionIs(iCons(C, REST), strToCodes(".dll"))
     andBool decimalDigitCount(iCons(C, REST)) <=Int 3
endmodule
