// (A) arithmetic digit-peel: does while(n>0){acc+=ev(n%10); n/=10} close by induction on n?
requires "verif.k"
module PEEL-SPEC
  imports VERIF
  claim <k> #peel(N:Int, A:Int) => evenOfInt(N, A) </k> requires N >=Int 0 [all-path]
endmodule
