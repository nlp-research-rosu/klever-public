requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  // A concrete interpretation for the nonempty entry precondition:
  // seqVal("growth", 0, 3) denotes ["a", "bb", "ccc"].
  rule stringAt("growth", 0) => "a"
  rule stringAt("growth", 1) => "bb"
  rule stringAt("growth", 2) => "ccc"
endmodule
