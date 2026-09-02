requires "verification.k"

module ADEQUACY-GROUND-SPEC
  imports VERIFICATION

  claim [true-witness-precondition]:
    <k>
      validScan(
        iCons(47,
          iCons(53,
            iCons(47,
              iCons(53,
                iCons(47,
                  iCons(49, .IntSeq)))))),
        0, 1, 0, 0, 0)
      => true
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [true-witness-result]:
    <k>
      scanResult(
        iCons(49,
          iCons(47,
            iCons(53,
              iCons(47,
                iCons(53,
                  iCons(47,
                    iCons(49, .IntSeq))))))),
        0, 0, 0, 0, 0)
      => true
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [false-witness-result]:
    <k>
      scanResult(
        iCons(49,
          iCons(47,
            iCons(54,
              iCons(47,
                iCons(50,
                  iCons(47,
                    iCons(49, .IntSeq))))))),
        0, 0, 0, 0, 0)
      => false
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
