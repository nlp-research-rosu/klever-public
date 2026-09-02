requires "verification.k"

module HAP-PLUS-SPEC
  imports HEAP-APPEND-PROBE-VERIFICATION

claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("i")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Val ] [ "out" <- ref(ON:Int) ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "out" <- ref(?ON2:Int) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <heap> (ON |-> list(ACC:ValSeq)) HREST:Map
        => (?ON2 |-> list(plusFold(I, N, ACC))) ?_:Map </heap>
    <heapLoc> HL:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int ON andBool ON <Int HL andBool keysBelow(HREST, HL)
    [all-path]

  // ---- Claim 3: entry (append builder) — res = build_squares(N), an existential
  // result ref whose heap entry holds the fold.
  
endmodule
