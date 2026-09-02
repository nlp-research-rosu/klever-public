requires "verification-bridge-mutant.k"

module SPEC-BRIDGE-MUTANT
  imports VERIFICATION-BRIDGE-MUTANT

  claim
    <k> (
      #loop(
        str(.IntSeq),
        Name("char"),
        removeVowelsLoopBody)
      =>
      .K
    ) ... </k>
    <env> CALLEE:Int </env>
    <scopes> (
      CALLEE |-> scope(
        "text" |-> str(TEXT:IntSeq)
        "result" |-> str(ACC:IntSeq)
        "char" |-> CHAR:Val,
        parent(0))
      OUTER:Map
      =>
      CALLEE |-> scope(
        "text" |-> str(TEXT)
        "result" |-> str(ACC)
        "char" |-> CHAR,
        parent(0))
      OUTER
    ) </scopes>

  claim
    <k> (
      #loop(
        str(iCons(C:Int, REST:IntSeq)),
        Name("char"),
        removeVowelsLoopBody)
      =>
      .K
    ) ... </k>
    <env> CALLEE:Int </env>
    <scopes> (
      CALLEE |-> scope(
        "text" |-> str(TEXT:IntSeq)
        "result" |-> str(ACC:IntSeq)
        "char" |-> CHAR:Val,
        parent(0))
      OUTER:Map
      =>
      CALLEE |-> scope(
        "text" |-> str(TEXT)
        "result" |-> str(removeVowelCodesAcc(ACC, REST))
        "char" |-> ?FINALCHAR:Val,
        parent(0))
      OUTER
    ) </scopes>
    requires isVowelCode(C)

  claim
    <k> (
      #loop(
        str(iCons(C:Int, REST:IntSeq)),
        Name("char"),
        removeVowelsLoopBody)
      =>
      .K
    ) ... </k>
    <env> CALLEE:Int </env>
    <scopes> (
      CALLEE |-> scope(
        "text" |-> str(TEXT:IntSeq)
        "result" |-> str(ACC:IntSeq)
        "char" |-> CHAR:Val,
        parent(0))
      OUTER:Map
      =>
      CALLEE |-> scope(
        "text" |-> str(TEXT)
        "result" |-> str(
          removeVowelCodesAcc(
            seqConcat(ACC, iCons(C, .IntSeq)),
            REST))
        "char" |-> ?FINALCHAR:Val,
        parent(0))
      OUTER
    ) </scopes>
    requires notBool isVowelCode(C)

  claim
    <k>
      #loadAll(removeVowelsProgram)
      ~> Call(Name("remove_vowels"), str(CODES:IntSeq))
      =>
      str(removeVowelCodes(CODES))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "remove_vowels" |->
          closureVal(("text", .ParamNames), removeVowelsBody, 0),
        parent(-1))
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
