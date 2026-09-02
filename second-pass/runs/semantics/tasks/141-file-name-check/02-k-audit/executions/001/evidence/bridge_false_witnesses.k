requires "verification.k"

module BRIDGE-FALSE-WITNESSES
  imports VERIFICATION

  // "a.txt" really returns Yes.  Interpreting charCount("a.txt", '.') as 0
  // makes the count bridge take the first rejection branch.
  claim [count-a-txt-wrongly-rejected]:
    <k>
      runFileNameCheck(iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))))
      => str(iCons(78, iCons(111, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires charCount(
      iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))),
      46) ==Int 0

  // Keeping the dot count correct but interpreting the first code as '0'
  // makes the head projection bridge reject the same real input.
  claim [head-a-txt-wrongly-rejected]:
    <k>
      runFileNameCheck(iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))))
      => str(iCons(78, iCons(111, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires charCount(
      iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))),
      46) ==Int 1
      andBool isLen(
        iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))))
        >=Int 5
      andBool headCode(
        iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq))))))
        ==Int 48

  // "a.pdf" really returns No.  With correct dot/head/digit observations but
  // suffixIs(..., txt) set true, the slice/equality bridge set accepts it.
  claim [suffix-a-pdf-wrongly-accepted]:
    <k>
      runFileNameCheck(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
      => str(iCons(89, iCons(101, iCons(115, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires charCount(
      iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))),
      46) ==Int 1
      andBool headCode(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
        ==Int 97
      andBool suffixIs(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))),
        0)
      andBool digitCount(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
        ==Int 0
endmodule
