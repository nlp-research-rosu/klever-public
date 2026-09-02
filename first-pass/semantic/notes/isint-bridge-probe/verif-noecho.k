// verif-noecho.k — CONTROL: identical to verif.k but WITHOUT the guarded echo. If the Probe 1
// claim (l[0]+l[1] => ?_:Int under allInt) FAILS here but PASSES with the echo, the echo is what
// discharges the isInt wall. If it passes here too, the probe was vacuous (?_:Int too weak).

requires "../../src/lemmas.k"

module ISINT-PROBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
endmodule
