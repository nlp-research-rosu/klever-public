// verification.k — md5hex trusted-property test: the hashlib.md5(...).hexdigest()
// chain returns a 32-char hex string (the opaque md5hexCodes + its lemmas).

requires "../../../src/lemmas.k"

module MD5HEX-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  syntax Expr ::= Val
endmodule
