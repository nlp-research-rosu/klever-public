requires "verif3.k"
module RT3F-SPEC
  imports VERIF3
  claim <k> #intOf(iCons(C:Int, iCons(D:Int, .IntSeq)), 0) => iCons(C, iCons(D, .IntSeq)) </k>
    requires 49 <=Int C andBool C <=Int 57 andBool 48 <=Int D andBool D <=Int 57 [all-path]
endmodule
