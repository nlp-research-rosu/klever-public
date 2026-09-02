// FOLD: sum over a symbolic list(VS) — the projected value is CARRIED, never decided. Works.
requires "verif.k"
module FOLD-SPEC
  imports VERIF
  claim <k> floop(list(VS:ValSeq)) => .K </k> <acc> A:Int => sumAcc(VS, A) </acc> requires allInt(VS) [all-path]
endmodule