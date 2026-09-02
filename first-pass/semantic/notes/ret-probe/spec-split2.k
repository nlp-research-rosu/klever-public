requires "verif-split.k"
module SPLIT2-SPEC
  imports RET
  claim <k> loop(S:IntSeq) ~> endcall => anyPos(S) ~> CONT:K </k>
        <stack> ListItem(frame(CONT:K)) => .List ... </stack>
        <ret> noRet </ret>
        [all-path]
  claim <k> callAny(S:IntSeq) => anyPos(S) </k>
        <stack> .List </stack> <ret> noRet </ret>
        [all-path]
endmodule
