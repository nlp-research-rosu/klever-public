requires "verification.k"

module SPEC-MUTATION
  imports VERIFICATION-BASE

  // Deliberately false mutation of SPEC-CONNECTION.poly-loop-empty.
  // The empty loop preserves A, not addF(A, 1.0).
  claim [wrong-poly-result]:
    <k>
      #loop(list(numVals(.NumSeq)), Name("coeff"), polyStep)
      => .K ...
    </k>
    <env> L </env>
    <scopes>
      BASE:Map
      (L |-> scope(
        .Map
          [ "xs" <- XSV:Val ]
          [ "value" <- (A:Float => addF(A, 1.0)) ]
          [ "power" <- P:Float ]
          [ "x" <- X:Float ]
          [ "coeff" <- C:Val ],
        PAR:Parent))
    </scopes>
    <scopeLoc> SL </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack> REST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool L in_keys(BASE)
endmodule
