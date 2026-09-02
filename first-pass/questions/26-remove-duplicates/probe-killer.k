// probe-killer.k — does the shared ref-disjointness killer still fire?
requires "verification.k"
module PROBE-KILLER
  imports REMOVE-DUPLICATES-VERIFICATION
  imports K-EQUAL
  claim <k> 1 => 2 </k>
    requires allInt(VS:ValSeq)
     andBool cellRef(H:Int) ==K valSeqAt(VS, J:Int)
    [all-path]
endmodule
