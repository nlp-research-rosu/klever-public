requires "verification-body-mutant.k"

module SPEC
  imports VERIFICATION

  // Loop invariant: the remaining loop updates result with precisely the
  // mathematical decode, while ch has Python's usual final loop-variable value.
  claim [decode-loop]:
    <k>
      #loop(str(CS:IntSeq), Name("ch"), decodeStep)
      ~> KONT:K
    =>
      KONT
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(ORIGINAL:IntSeq)
        "result" |-> str(ACC:IntSeq)
        "ch" |-> CH:Val,
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> builtinsScope
    =>
      1 |-> scope(
        "s" |-> str(ORIGINAL)
        "result" |-> str(decodeAcc(ACC, CS))
        "ch" |-> loopLast(CH, CS),
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires lowerCodes(CS)

  // The actual translated closure computes decodeCodes for every lowercase
  // encoded string, from the ordinary module/builtins environment.
  claim [decode-shift]:
    <k> Call(Name("decode_shift"), str(CS:IntSeq)) => str(decodeCodes(CS)) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires lowerCodes(CS)

  // Per-character inverse law for the prompt's supplied encoder.
  claim [char-inverse]:
    <k> decodeChar(encodeChar(C:Int)) => C </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 97 <=Int C andBool C <=Int 122
endmodule
