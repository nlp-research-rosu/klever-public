requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the even Int/Int median adds 1 to the numerator.
  // Satisfying witness [1, 3] has the real result 2.0, not 2.5.
  claim [wrong-even-int-result]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divII(I1:Int +Int I2:Int +Int 1, 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K I1
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K I2
     andBool notBool (HL in_keys(HP))
endmodule
