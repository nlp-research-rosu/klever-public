requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  // Rejection 1: anything other than exactly one dot.
  claim [audit-reject-dot-count]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) =/=Int 1

  // Rejection 2: one dot, but not enough room for a nonempty base and suffix.
  claim [audit-reject-short]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) <Int 5

  // Rejection 3: the first character is not an ASCII Latin letter.
  claim [audit-reject-first]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) >=Int 5
     andBool notBool latinCode(headCode(CS))

  // Rejection 4: all earlier checks pass, but the extension is unsupported.
  claim [audit-reject-suffix]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) >=Int 5
     andBool latinCode(headCode(CS))
     andBool notBool allowedSuffix(CS)

  // Rejection 5: all structural checks pass, but there are over three digits.
  claim [audit-reject-digits]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) >=Int 5
     andBool latinCode(headCode(CS))
     andBool allowedSuffix(CS)
     andBool digitCount(CS) >Int 3

  // Acceptance: every condition in the natural-language contract holds.
  claim [audit-accept]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(89, iCons(101, iCons(115, .IntSeq)))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) >=Int 5
     andBool latinCode(headCode(CS))
     andBool allowedSuffix(CS)
     andBool digitCount(CS) <=Int 3
endmodule
