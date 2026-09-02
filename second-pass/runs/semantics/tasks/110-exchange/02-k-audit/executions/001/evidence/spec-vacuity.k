requires "verification.k"

module EXCHANGE-SPEC-VACUITY
  imports EXCHANGE-VERIFICATION

  // Induction invariant for the first loop.
  claim [odd-loop]:
    <k>
      #loop(list(intVals(iCons(I:Int, IS:IntSeq))),
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
      #loop(list(intVals(iCons(I:Int, IS:IntSeq))),
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
  // Fresh false mutation: force the universal result to "NO". This is false,
  // for example, for the satisfying nonempty input ([2], [1]), where odd=0
  // and even=0 and both Python implementations return "YES".
  claim [exchange-wrong-always-no]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(intVals(iCons(A:Int, AS:IntSeq)))
           , list(intVals(iCons(B:Int, BS:IntSeq)))
           , .Exprs))
      =>
      str(iCons(78, iCons(79, .IntSeq)))
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
