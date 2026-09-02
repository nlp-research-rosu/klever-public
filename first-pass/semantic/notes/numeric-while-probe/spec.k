requires "verif.k"
module NWPROBE-SPEC
  imports NWPROBE-VERIFICATION
  // while-loop invariant: from (n=N, r=R) the digit-sum while leaves r := digitAcc(N, R).
  claim
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(0))),
        Assign(Name("r"), BinOp("+", Name("r"), BinOp("%", Name("n"), Int(10))))
        Assign(Name("n"), BinOp("//", Name("n"), Int(10))))
    => .K ... </k>
    <env> L:Int </env>
    <store>
      ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "r" <- R:Int ], P:Parent)
               => scope(.Map [ "n" <- ?_:Int ] [ "r" <- digitAcc(N, R) ], P) ) ...
    </store>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
