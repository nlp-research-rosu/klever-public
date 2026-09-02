requires "verification.k"

module STAGE4-GROUND-WITNESS
  imports VERIFICATION

  claim [entry-witness-bca]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "decode_cyclic",
            Params("s"),
            decodeFunctionBody)))
      ~> Call(
           Name("decode_cyclic"),
           str(iCons(98, iCons(99, iCons(97, .IntSeq)))))
      => str(iCons(97, iCons(98, iCons(99, .IntSeq))))
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
