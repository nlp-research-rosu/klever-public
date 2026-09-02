requires "verif.k"
module PRIME-SPEC
  imports PRIME
  claim <k> scan(I:Int, N:Int) => .K </k>
        <res> noDiv => #if hasDiv(I, N) #then div #else noDiv #fi </res>
        requires I >=Int 2 [all-path]
endmodule
