// verification.k — parse_music on the UNIFIED semantics, TRAP-FREE (P17).
// solution.py is canonical verbatim: real dict literal, real dict-subscript
// read, real listcomp over the real split(' ') reading the free var note_map
// off the parent frame (PEP-709 inlined scope: py2mpy emits no CellVars).
//
// Membership machinery is the 148-bf idiom: string-eq case splits are
// UNDECIDABLE to the backend (==K on Str is not smtlib-hooked), so the token
// maps to an OPAQUE INT noteDur(V) and every split is an integer split.

requires "../../reference/src/lemmas.k"

module PARSE-MUSIC-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // split always yields >= 1 token (P67 lemma pair)
  rule vsLen(splitSep(_:IntSeq, _:Int, _:IntSeq)) >Int 0 => true [simplification]
  rule 0 <Int vsLen(splitSep(_:IntSeq, _:Int, _:IntSeq)) => true [simplification]

  // ---- domain premise + the opaque duration ---------------------------------
  // validTok(V): V is one of 'o' / 'o|' / '.|' / '' (opaque membership).
  // noteDur(V): the duration the dict assigns (4/2/1), 0 for the empty token.
  // Their coupling axioms below have the intended model (the 4 concrete
  // tokens), so they are consistent; everything else stays underspecified.
  syntax Bool ::= validTok(Val) [function, total, no-evaluators]
  syntax Int  ::= noteDur(Val)  [function, total, no-evaluators]
  syntax Bool ::= validToks(ValSeq) [function, total]
  rule validToks(.ValSeq)                => true
  rule validToks(vCons(V:Val, R:ValSeq)) => validTok(V) andBool validToks(R)

  // a token is a real string value: kill the k-top cellRef-deref and If-ref
  // narrowing branches (a heap ref never flows out of the split as an element)
  rule validTok(cellRef(_:Int)) => false [simplification]
  rule validTok(ref(_:Int))     => false [simplification]

  // the filter's truthy becomes a TOTAL INT test (branchable by Z3): a valid
  // token is truthy iff it is not the empty token, i.e. its duration is not 0
  rule truthy(V:Val) => noteDur(V) =/=Int 0
    requires validTok(V)
    [simplification]

  // the real dict read on a kept valid token IS its duration (the cascade's
  // ==K guards are undecidable on an abstract token, so dGet stays opaque and
  // this bridge names its value)
  rule dGet(vCons(str(iCons(111, .IntSeq)),
              vCons(str(iCons(111, iCons(124, .IntSeq))),
                vCons(str(iCons(46, iCons(124, .IntSeq))), .ValSeq))),
            vCons(4, vCons(2, vCons(1, .ValSeq))), V:Val)
    => noteDur(V)
    requires validTok(V) andBool noteDur(V) =/=Int 0
    [simplification]

  // ---- the comprehension's builder fold, arms guarded by the branch atoms --
  syntax ValSeq ::= musicFold(ValSeq, ValSeq) [function, total, no-evaluators]
  rule musicFold(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule musicFold(vCons(V:Val, R:ValSeq), ACC:ValSeq) => musicFold(R, ACC)
    requires validTok(V) andBool noteDur(V) ==Int 0 [simplification]
  rule musicFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => musicFold(R, valSeqConcat(ACC, vCons(noteDur(V), .ValSeq)))
    requires validTok(V) andBool noteDur(V) =/=Int 0 [simplification]
endmodule
