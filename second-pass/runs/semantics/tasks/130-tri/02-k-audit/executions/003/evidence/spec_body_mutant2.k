requires "/tmp/audit-work/130-tri-audit/verification-body-mutant2.k"

module TRI-LOOP-SPEC
  imports TRI-VERIFICATION

  // Loop invariant: before iteration I, result is the prefix through I-1,
  // and a/b are precisely the preceding two contract values.
  claim
    <k> #while(TriLoopCond, TriLoopBody) ~> KREST:K => KREST </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        .Map
          [ "n"      <- I:Int +Int R:Int -Int 1 ]
          [ "result" <- ref(H:Int) ]
          [ "a"      <- triAt(I:Int -Int 2) ]
          [ "b"      <- triAt(I -Int 1) ]
          [ "value"  <- triAt(I -Int 1) ]
          [ "i"      <- I ],
        parent(0))
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        .Map
          [ "n"      <- I +Int R -Int 1 ]
          [ "result" <- ref(H) ]
          [ "a"      <- ?AFINAL:Int ]
          [ "b"      <- ?BFINAL:Int ]
          [ "value"  <- ?VFINAL:Int ]
          [ "i"      <- ?FINAL:Int ],
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      H |-> list(VS:ValSeq)
      =>
      H |-> list(?OUT:ValSeq)
    </heap>
    <heapLoc> H +Int 1 </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2
     andBool R >=Int 0
     andBool prefixIndex(VS) <=Int I -Int 1
     andBool prefixIndex(VS) >=Int I -Int 1
    ensures ?FINAL <=Int I +Int R
     andBool ?FINAL >=Int I +Int R
     andBool prefixIndex(?OUT) <=Int I +Int R -Int 1
     andBool prefixIndex(?OUT) >=Int I +Int R -Int 1
endmodule

module TRI-CORRECT-SPEC
  imports TRI-LOOP-SPEC

  // The exact translated body, called with an arbitrary contract input,
  // returns a heap list containing the mathematical prefix through n.
  claim
    <k> Call(closureVal(("n", .ParamNames), TriFunctionBody, 0),
             Int(N:Int), .Exprs)
      =>
         ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(?RESULT:ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    ensures prefixIndex(?RESULT) <=Int N
     andBool prefixIndex(?RESULT) >=Int N
endmodule
