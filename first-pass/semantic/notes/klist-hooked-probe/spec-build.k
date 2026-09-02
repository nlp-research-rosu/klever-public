requires "verif-klist.k"

module SPEC-BUILD-SPEC
  imports VERIF-KLIST

  // the flattening question: (L ListItem(N)) buildL(N-1) must fold to L buildL(N) with NO lemmas
  claim <k> #build(N:Int) => .K ... </k>
        <out> L:List => L buildL(N) </out>
        requires N >=Int 0
        [all-path]
endmodule
