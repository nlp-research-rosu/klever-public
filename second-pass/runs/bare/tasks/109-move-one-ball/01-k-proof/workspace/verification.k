requires "mpy-syntax.k"

module HUMAN-EVAL-VERIFICATION
  imports HUMAN-EVAL-SYNTAX
  imports INT
  imports BOOL

  // Mathematical operations on the input representation.
  syntax Int ::= length(IList) [function, total]
               | last(IList) [function]
               | dropBit(Int, Int) [function, total]
               | dropsFrom(Int, IList) [function, total]
               | cyclicDrops(IList) [function, total]
  syntax Bool ::= rotationSortable(IList) [function, total]

  rule length(.IList) => 0
  rule length(_I :: IS) => 1 +Int length(IS)

  rule last(I :: .IList) => I
  rule last(_I :: J :: IS) => last(J :: IS)

  rule dropBit(I, J) => 1 requires I >Int J
  rule dropBit(I, J) => 0 requires I <=Int J

  rule dropsFrom(_PREVIOUS, .IList) => 0
  rule dropsFrom(PREVIOUS, I :: IS)
    => dropBit(PREVIOUS, I) +Int dropsFrom(I, IS)

  rule cyclicDrops(.IList) => 0
  rule cyclicDrops(I :: IS) => dropsFrom(last(I :: IS), I :: IS)

  // For a list of distinct integers, this is equivalent to existence of a
  // right rotation that is strictly increasing: a circle has at most one drop.
  rule rotationSortable(L) => cyclicDrops(L) <=Int 1
endmodule
