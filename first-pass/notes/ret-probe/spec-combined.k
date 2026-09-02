// COMBINED: loop invariant POPS THE FRAME itself in one step, off a SYMBOLIC <stack> (frame(CONT)
// with CONT a variable + a symbolic tail). This is the formulation once claimed to "jam" — it #Tops.
requires "verif-combined.k"
module COMBINED-SPEC
  imports RET
  claim <k> loop(S:IntSeq) ~> endcall => anyPos(S) ~> CONT:K </k>
        <stack> ListItem(frame(CONT:K)) => .List ... </stack>
        [all-path]
  claim <k> callAny(S:IntSeq) => anyPos(S) </k>
        <stack> .List </stack>
        [all-path]
endmodule
