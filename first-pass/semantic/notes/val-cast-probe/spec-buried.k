// BURIED: the symbolic var IS is hidden inside ints2vals(...) -> kprove can't split what it can't see.
requires "verif.k"
module BURIED-SPEC
  imports VERIF
  claim <k> floop(list(ints2vals(IS:IntSeq))) => .K </k> <acc> A:Int => sumAcc(ints2vals(IS), A) </acc> [all-path]
endmodule
