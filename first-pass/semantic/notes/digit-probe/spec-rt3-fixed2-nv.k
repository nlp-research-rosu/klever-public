requires "verif3.k"
module RT3FNV-SPEC
  imports VERIF3
  claim <k> #intOf(iCons(C:Int, iCons(D:Int, .IntSeq)), 0) => iCons(C, iCons(D +Int 1, .IntSeq)) </k>
    requires 49 <=Int C andBool C <=Int 57 andBool 48 <=Int D andBool D <=Int 57 [all-path]
endmodule
