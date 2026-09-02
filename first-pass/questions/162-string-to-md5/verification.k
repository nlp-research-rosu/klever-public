// verification.k — string_to_md5 on the UNIFIED semantics, TRAP-FREE (P162).
// solution.py is canonical verbatim; the hashlib chain is the shared trusted
// opaque md5hexCodes (length-32/hex-charset lemmas in lemmas/builtins.k).

requires "../../reference/src/lemmas.k"

module STRING-TO-MD5-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  syntax Val ::= s2mRes(IntSeq) [function, total, no-evaluators]
  // guards spelled on isLen — the truthy branch pins emptiness as isLen(CS)==0
  rule s2mRes(CS:IntSeq) => noneV requires isLen(CS) ==Int 0 [simplification]
  rule s2mRes(CS:IntSeq) => str(md5hexCodes(CS))
    requires notBool (isLen(CS) ==Int 0) [simplification]
endmodule
