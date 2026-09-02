requires "pv.k"
module POW-PROBE-SPEC
  imports POW-PROBE
  claim
    <k> Assign(Name("r"), BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))) => .K ... </k>
    <env> L:Int </env>
    <store> ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "r" <- _:Val ], P:Parent)
                     => scope(.Map [ "n" <- N ] [ "r" <- ipow(10, N -Int 2) ], P) ) ... </store>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
    [all-path]
endmodule
