// SPLIT: loop invariant is LOCAL — reduces loop+endcall to #pop, value stashed in <ret>,
// NEVER touches <stack>. The frame pop (#pop) is a separate step, done in the entry.
requires "verif-split.k"
module SPLIT-SPEC
  imports RET
  claim <k> loop(S:IntSeq) ~> endcall => #pop </k>
        <ret> noRet => retV(anyPos(S)) </ret>
        [all-path]
  claim <k> callAny(S:IntSeq) => anyPos(S) </k>
        <stack> .List </stack> <ret> noRet </ret>
        [all-path]
endmodule
