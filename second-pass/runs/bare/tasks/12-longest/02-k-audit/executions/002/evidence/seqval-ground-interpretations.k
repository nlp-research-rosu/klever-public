requires "verification.k"

module WITNESS
  imports VERIFICATION

  // A concrete interpretation of the proof-only symbolic sequence.
  rule stringAt("case", 0) => "a"
  rule stringAt("case", 1) => "bb"
  rule stringAt("case", 2) => "ccc"

  // A distinct interpretation changes the result, showing that stringAt is
  // input data rather than a fixed answer oracle.
  rule stringAt("opposite", 0) => "zzzz"
  rule stringAt("opposite", 1) => "b"
  rule stringAt("opposite", 2) => "ccc"
endmodule
