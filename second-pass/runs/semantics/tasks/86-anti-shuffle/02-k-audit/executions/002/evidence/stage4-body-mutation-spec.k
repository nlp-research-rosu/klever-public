requires "verification-body-mutation.k"

module WORD-SPEC
  imports ANTI-SHUFFLE-BASE

  // The allocation-free word summary used by the main proof is exactly the
  // observable value produced by list(word), sorted(...), and "".join(...).
  claim [sort-word-summary]:
    <k>
      Call(
        Attribute(Str(""), "join"),
        Call(Name("sorted"), Call(Name("list"), str(W:IntSeq))))
      =>
      str(sortWord(W))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> H:Map => ?HFINAL:Map </heap>
    <heapLoc> N:Int => ?NFINAL:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (N in_keys(H))
     andBool notBool ((N +Int 1) in_keys(H))
endmodule

module ANTI-LOOP-SPEC
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  // Inductive loop invariant. Starting with prefix A and remaining words WS,
  // the loop leaves exactly A ++ emitWordSeq(WS).
  claim [anti-loop]:
    <k>
      #loop(wordsObj(WS:Words), Name("word"), antiLoopBody)
      ~> Name("result")
      =>
      str(seqConcat(A, emitWordSeq(WS)))
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "result" |-> str(A:IntSeq)
        "s"      |-> str(INPUT:IntSeq)
        "word"   |-> WORD0:Val,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SCFINAL:Map
    </scopes>
    <heap> H:Map => ?HFINAL:Map </heap>
    <heapLoc> N:Int => ?NFINAL:Int </heapLoc>
endmodule

module ANTI-SHUFFLE-SPEC
  imports ANTI-SHUFFLE-VERIFICATION

  // End-to-end functional correctness of the exact solution body for every
  // symbolic ASCII code sequence S accepted by the supplied string model.
  claim [anti-shuffle-correct]:
    <k>
      Call(
        closureVal(("s", .ParamNames), antiBody, 0),
        (str(S:IntSeq), .Exprs))
      =>
      antiShuffleSpec(S)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HFINAL:Map </heap>
    <heapLoc> 0 => ?NFINAL:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
