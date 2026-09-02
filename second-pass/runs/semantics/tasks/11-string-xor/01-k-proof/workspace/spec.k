requires "verification.k"

module STRING-XOR-SPEC
  imports STRING-XOR-VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(zipObjS(A:IntSeq, B:IntSeq), stringXorTarget,
            stringXorLoopBody) ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(("a" |-> str(ORIGA:IntSeq))
                    ("b" |-> str(ORIGB:IntSeq))
                    ("result" |-> str(P:IntSeq))
                    ("x" |-> str(X:IntSeq))
                    ("y" |-> str(Y:IntSeq)),
                    PAR:Parent)) SC:Map
      =>
      (L |-> scope(("a" |-> str(ORIGA))
                    ("b" |-> str(ORIGB))
                    ("result" |-> str(xorAcc(P, A, B)))
                    ("x" |-> str(xorLastX(A, B, X)))
                    ("y" |-> str(xorLastY(A, B, Y))),
                    PAR)) SC
    </scopes>
    requires notBool (L in_keys(SC))
     andBool binaryCodes(A)
     andBool binaryCodes(B)

  claim [solution-correct]:
    <k>
      #loadAll(stringXorModule)
      ~> Call(Name("string_xor"), str(A:IntSeq), str(B:IntSeq))
      => str(xorAcc(.IntSeq, A, B))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))) (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("string_xor" |-> stringXorClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires binaryCodes(A) andBool binaryCodes(B)
endmodule
