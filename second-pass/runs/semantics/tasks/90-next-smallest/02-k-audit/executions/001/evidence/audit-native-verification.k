requires "verification.k"

module AUDIT-NATIVE-VERIFICATION
  imports NEXT-SMALLEST-VERIFICATION

  // A reviewer bridge from the inductive Ints carrier to the supplied
  // semantics' native .ValSeq/vCons representation.
  syntax ValSeq ::= nativeIntVals(Ints) [function, total]
  rule nativeIntVals(nilInts) => .ValSeq
  rule nativeIntVals(consInts(X:Int, XS:Ints))
    => vCons(X, nativeIntVals(XS))
endmodule

module AUDIT-NATIVE-WITH-LOOP-LEMMA
  imports AUDIT-NATIVE-VERIFICATION

  rule
    <k>
      #loop(list(nativeIntVals(INPUT:Ints)),
            Name("value"),
            nextSmallestLoopBody)
      ~> nextSmallestReturn
      ~> #endcall
    =>
      nsScan(INPUT, SMALLEST:Int, SECOND:Int, COUNT:Int)
      ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(("value" |-> OLD_VALUE:Int
                    "lst" |-> LST:Val
                    "smallest" |-> SMALLEST
                    "second" |-> SECOND
                    "count" |-> COUNT),
                   parent(0)))
    =>
      ((SC
        1 |-> scope(("value" |-> OLD_VALUE
                     "lst" |-> LST
                     "smallest" |-> SMALLEST
                     "second" |-> SECOND
                     "count" |-> COUNT),
                    parent(0))) [1 <- undef])
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) REST:List
    =>
      REST
    </stack>
    <ret> noRet </ret>
    <exc> EXC:Exc </exc>
    <exit-code> CODE:Int </exit-code>
    requires notBool (1 in_keys(SC))
    [priority(40)]
endmodule
