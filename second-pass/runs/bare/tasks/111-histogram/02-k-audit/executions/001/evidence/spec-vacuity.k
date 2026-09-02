requires "lemmas.k"

module SPEC-VACUITY
  imports VERIFIED-LOOP-LEMMAS

  // Deliberately false: histogram("a b b a") returns a -> 2, not a -> 3.
  claim [false-tied-count]:
    <k>
      execute(histogramProgram(), "a b b a")
      => pyDict(
           pyString("a") |-> pyInt(3)
           pyString("b") |-> pyInt(2),
           ListItem(pyString("a"))
           ListItem(pyString("b")))
    </k>
endmodule
