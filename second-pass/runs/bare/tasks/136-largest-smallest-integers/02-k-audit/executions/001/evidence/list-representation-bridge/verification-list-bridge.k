requires "verification.k"

module VERIFICATION-LIST-BRIDGE
  imports VERIFICATION

  syntax List ::= "#asPyList" "(" IntSeq ")" [function, total]

  rule #asPyList(nil) => .List
  rule #asPyList(icon(I, IS))
    => ListItem(pyInt(I)) #asPyList(IS)
endmodule
