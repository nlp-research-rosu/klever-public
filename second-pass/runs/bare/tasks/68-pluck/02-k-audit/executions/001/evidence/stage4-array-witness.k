requires "verification.k"

module ARRAY-WITNESS
  imports VERIFICATION

  // Ground interpretations of the proof's otherwise opaque array element
  // observer. Each ID represents one concrete satisfying entry input.
  rule arrayAt(68, 0) => 4
  rule arrayAt(68, 1) => 2
  rule arrayAt(68, 2) => 3

  rule arrayAt(70, 0) => 7
  rule arrayAt(70, 1) => 5
  rule arrayAt(70, 2) => 9

  rule arrayAt(71, 0) => 2
  rule arrayAt(71, 1) => 2

  rule arrayAt(72, 0) => 5
  rule arrayAt(72, 1) => 0
  rule arrayAt(72, 2) => 3
  rule arrayAt(72, 3) => 0
  rule arrayAt(72, 4) => 4
  rule arrayAt(72, 5) => 2
endmodule
