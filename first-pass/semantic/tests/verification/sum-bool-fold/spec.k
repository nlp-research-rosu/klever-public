requires "verification.k"

module SUM-BOOL-FOLD-SPEC
  imports SUM-BOOL-FOLD-VERIFICATION

  // sum(list(VS)) over a symbolic List[bool] counts the Trues.
  claim <k> #sumAcc(list(VS:ValSeq), ACC:Int) => ?R:Int ... </k>
        requires allBool(VS)
        ensures  ?R ==Int countTrue(VS, ACC)
        [all-path]
endmodule
