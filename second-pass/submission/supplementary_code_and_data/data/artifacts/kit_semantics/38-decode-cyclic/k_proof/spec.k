requires "verification.k"

module SPEC
  imports VERIFICATION

  // Phase 0: no buffered characters.
  claim [loop-empty]:
    <k> #loop(str(IS:IntSeq), Name("char"), decodeLoopBody) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope("decode_cyclic" |-> FUN:Val, parent(-1))
      L |-> scope(
        "s"      |-> str(SOURCE:IntSeq)
        "result" |-> (str(ACC:IntSeq)
                      => str(decodedResult(ACC, IS)))
        "group"  |-> (str(.IntSeq) => str(decodedTail(IS)))
        "char"   |-> (OLDCHAR:Val => finalLoopChar(IS, OLDCHAR)),
        parent(0))
    </scopes>
    <scopeLoc> NEXTLOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires L >=Int 1

  // Phase 1: one buffered character.
  claim [loop-one]:
    <k> #loop(str(IS:IntSeq), Name("char"), decodeLoopBody) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope("decode_cyclic" |-> FUN:Val, parent(-1))
      L |-> scope(
        "s"      |-> str(SOURCE:IntSeq)
        "result" |-> (str(ACC:IntSeq)
                      => str(decodedResult(
                           ACC,
                           iCons(A:Int, IS))))
        "group"  |-> (str(iCons(A, .IntSeq))
                      => str(decodedTail(iCons(A, IS))))
        "char"   |-> (OLDCHAR:Val => finalLoopChar(IS, OLDCHAR)),
        parent(0))
    </scopes>
    <scopeLoc> NEXTLOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires L >=Int 1

  // Phase 2: two buffered characters.
  claim [loop-two]:
    <k> #loop(str(IS:IntSeq), Name("char"), decodeLoopBody) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope("decode_cyclic" |-> FUN:Val, parent(-1))
      L |-> scope(
        "s"      |-> str(SOURCE:IntSeq)
        "result" |-> (str(ACC:IntSeq)
                      => str(decodedResult(
                           ACC,
                           iCons(A:Int, iCons(B:Int, IS)))))
        "group"  |-> (str(iCons(A, iCons(B, .IntSeq)))
                      => str(decodedTail(
                           iCons(A, iCons(B, IS)))))
        "char"   |-> (OLDCHAR:Val => finalLoopChar(IS, OLDCHAR)),
        parent(0))
    </scopes>
    <scopeLoc> NEXTLOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires L >=Int 1

  // Whole-program entry: load the exact definition, resolve its binding, and
  // execute its body under the supplied semantics.
  claim [decode-entry]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "decode_cyclic",
            Params("s"),
            decodeFunctionBody)))
      ~> Call(Name("decode_cyclic"), str(INPUT:IntSeq))
      => str(decodeCodes(INPUT))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "decode_cyclic" |-> ?FUN:Val, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
