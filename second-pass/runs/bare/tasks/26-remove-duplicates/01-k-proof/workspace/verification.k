requires "semantic.k"

module VERIFICATION
  imports MPY

  // Executable mathematical contract: traverse the input from left to right
  // and retain an element exactly when its occurrence count in the *original*
  // list is one.  Thus the survivors keep their original order.
  syntax Ints ::= "removeRepeated" "(" Ints "," Ints ")" [function]
                | "removeRepeatedOnto" "(" Ints "," Ints "," Ints ")" [function]
  rule removeRepeated(INPUT, ORIGINAL)
    => removeRepeatedOnto(INPUT, ORIGINAL, .Ints)
  rule removeRepeatedOnto(.Ints, _, SUFFIX) => SUFFIX
  rule removeRepeatedOnto((I, IS), ORIGINAL, SUFFIX)
    => ifCons(count(I, ORIGINAL) ==Int 1,
              I,
              removeRepeatedOnto(IS, ORIGINAL, SUFFIX))
endmodule
