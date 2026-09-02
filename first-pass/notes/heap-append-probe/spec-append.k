requires "verification.k"

module HAP-APPEND-SPEC
  imports HEAP-APPEND-PROBE-VERIFICATION

claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Expr(Call(Attribute(Name("result"), "append"), BinOp("*", Name("i"), Name("i")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Val ] [ "result" <- ref(RN:Int) ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "result" <- ref(RN) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <heap> (RN |-> list(ACC:ValSeq)) HREST:Map
        => (RN |-> list(sqFold(I, N, ACC))) HREST </heap>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Claim 2: plus-builder invariant. Each iteration allocates the [i] literal
  // and the concatenation result; `out` rebinds to the fresh ref. keysBelow lets the
  // allocator's freshness guard discharge against the abstract rest.
  
endmodule
