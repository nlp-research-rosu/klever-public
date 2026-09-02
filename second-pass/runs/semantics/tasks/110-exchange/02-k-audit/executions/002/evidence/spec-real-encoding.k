requires "verification-real-encoding.k"

module EXCHANGE-SPEC-REAL
  imports EXCHANGE-VERIFICATION-REAL

  // Induction invariant for the first loop.
  claim [odd-loop]:
    <k>
      #loop(list(vCons(I:Int, intSeqVals(IS:IntSeq))),
            Name("number"), ODD-BODY) ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ( "lst1"  |-> LST1:Val
          "lst2"  |-> LST2:Val
          "odd"   |-> O:Int
          "even"  |-> E:Int
          "number" |-> N:Int ),
        P:Parent)
      =>
      SC
      L |-> scope(
        ( "lst1"  |-> LST1
          "lst2"  |-> LST2
          "odd"   |-> oddAcc(O, iCons(I, IS))
          "even"  |-> E
          "number" |-> ?ODDLAST:Int ),
        P)
    </scopes>
    requires notBool L in_keys(SC)

  // The analogous invariant for the second loop.
  claim [even-loop]:
    <k>
      #loop(list(vCons(I:Int, intSeqVals(IS:IntSeq))),
            Name("number"), EVEN-BODY) ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ( "lst1"  |-> LST1:Val
          "lst2"  |-> LST2:Val
          "odd"   |-> O:Int
          "even"  |-> E:Int
          "number" |-> N:Int ),
        P:Parent)
      =>
      SC
      L |-> scope(
        ( "lst1"  |-> LST1
          "lst2"  |-> LST2
          "odd"   |-> O
          "even"  |-> evenAcc(E, iCons(I, IS))
          "number" |-> ?EVENLAST:Int ),
        P)
    </scopes>
    requires notBool L in_keys(SC)

  // End-to-end functional correctness for all non-empty integer lists, the
  // input domain promised by prompt.py.
  claim [exchange-correct]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(intSeqVals(iCons(A:Int, AS:IntSeq)))
           , list(intSeqVals(iCons(B:Int, BS:IntSeq)))
           , .Exprs))
      =>
      exchangeResult(
        iCons(A, AS),
        iCons(B, BS))
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
