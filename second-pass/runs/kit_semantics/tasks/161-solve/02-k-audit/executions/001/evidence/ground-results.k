requires "/tmp/audit-work/161-solve/scratch/verification.k"

module GROUND-RESULTS
  imports VERIFICATION

  claim [empty]:
    <k> solveResult(.IntSeq) => str(.IntSeq) </k>
    <env> ENV1:Int </env>
    <scopes> SCOPES1:Map </scopes>
    <scopeLoc> SCOPELOC1:Int </scopeLoc>
    <heap> HEAP1:Map </heap>
    <heapLoc> HEAPLOC1:Int </heapLoc>
    <stack> STACK1:List </stack>
    <ret> RET1:RetState </ret>
    <exc> EXC1:Exc </exc>
    <exit-code> EXIT1:Int </exit-code>

  claim [letter-and-digit]:
    <k>
      solveResult(iCons(97, iCons(49, .IntSeq)))
      =>
      str(iCons(65, iCons(49, .IntSeq)))
    </k>
    <env> ENV2:Int </env>
    <scopes> SCOPES2:Map </scopes>
    <scopeLoc> SCOPELOC2:Int </scopeLoc>
    <heap> HEAP2:Map </heap>
    <heapLoc> HEAPLOC2:Int </heapLoc>
    <stack> STACK2:List </stack>
    <ret> RET2:RetState </ret>
    <exc> EXC2:Exc </exc>
    <exit-code> EXIT2:Int </exit-code>

  claim [no-letters]:
    <k>
      solveResult(iCons(49, iCons(35, iCons(50, .IntSeq))))
      =>
      str(iCons(50, iCons(35, iCons(49, .IntSeq))))
    </k>
    <env> ENV3:Int </env>
    <scopes> SCOPES3:Map </scopes>
    <scopeLoc> SCOPELOC3:Int </scopeLoc>
    <heap> HEAP3:Map </heap>
    <heapLoc> HEAPLOC3:Int </heapLoc>
    <stack> STACK3:List </stack>
    <ret> RET3:RetState </ret>
    <exc> EXC3:Exc </exc>
    <exit-code> EXIT3:Int </exit-code>

  claim [ascii-case-boundaries]:
    <k>
      solveResult(iCons(65, iCons(122, iCons(90, iCons(97, .IntSeq)))))
      =>
      str(iCons(97, iCons(90, iCons(122, iCons(65, .IntSeq)))))
    </k>
    <env> ENV4:Int </env>
    <scopes> SCOPES4:Map </scopes>
    <scopeLoc> SCOPELOC4:Int </scopeLoc>
    <heap> HEAP4:Map </heap>
    <heapLoc> HEAPLOC4:Int </heapLoc>
    <stack> STACK4:List </stack>
    <ret> RET4:RetState </ret>
    <exc> EXC4:Exc </exc>
    <exit-code> EXIT4:Int </exit-code>

  // The supplied model treats 233 as nonalphabetic; this records the exact
  // formal result without claiming it is CPython's Unicode result.
  claim [unicode-model-boundary]:
    <k>
      solveResult(iCons(233, iCons(49, .IntSeq)))
      =>
      str(iCons(49, iCons(233, .IntSeq)))
    </k>
    <env> ENV5:Int </env>
    <scopes> SCOPES5:Map </scopes>
    <scopeLoc> SCOPELOC5:Int </scopeLoc>
    <heap> HEAP5:Map </heap>
    <heapLoc> HEAPLOC5:Int </heapLoc>
    <stack> STACK5:List </stack>
    <ret> RET5:RetState </ret>
    <exc> EXC5:Exc </exc>
    <exit-code> EXIT5:Int </exit-code>
endmodule
