// verification.k — int_to_mini_roman on the UNIFIED semantics. The canonical greedy nested-while over a
// 13-entry value table blows up symbolically; solution.py is the CLOSED FORM over the decimal digits of
// `number` (valid for 1 <= number <= 1000): result = M[n//1000] + H[(n//100)%10] + T[(n//10)%10] +
// U[n%10], four fixed per-place Roman tables. Diff-tested 0/1000 over the whole domain.
//
// The four tables are held OPAQUE (function/total, no reduction) so the 40-odd-node literals the program
// builds never bloat the symbolic config (the prior partial ground ~1s/step carrying four full ValSeq
// literals through the nested `+` continuation). The Roman rendering is still PINNED, not trusted: each
// table's content is DECLARED by a collapse simplification `vlk(<exact literal>, I) => vlk(<sym>, I)`
// (vlk-headed, so kompile accepts it — a constructor-headed reverse fold would not), and the executed
// deref (which materializes the literal on the heap) folds through valSeqAt=>vlk=>the symbol. So the
// opaque symbol carries EXACTLY the literal the ListExpr builds. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module INT-TO-MINI-ROMAN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // A symbolic-index lookup folds to the opaque total vlk (the executed valSeqAt over the heap literal
  // and the model's valSeqAt over the table both route here); the result is seqConcat of 4 opaque
  // codesProj(vlk(..)), verifying the STRUCTURE without enumerating the tables.
  syntax Val ::= vlk(ValSeq, Int) [function, total]
  rule valSeqAt(VS:ValSeq, I:Int) => vlk(VS, I) requires allStr(VS) [simplification]

  // the place indices are floored //,% forms — non-negative for N>=0. Establishing that lets normIdx
  // and the subscript resolve without sign-branching per lookup (the residual index-layer blowup).
  rule 0 <=Int (N:Int -Int pyMod(N, M:Int)) /Int M => true requires N >=Int 0 andBool M >Int 0 [simplification]
  rule (N:Int -Int pyMod(N, M:Int)) /Int M <Int 0 => false requires N >=Int 0 andBool M >Int 0 [simplification]

  // knownStr: a lookup into an all-str table is a str (an opaque valSeqAt is not syntactically str(...)).
  syntax Bool ::= knownStr(Val) [function]
  rule knownStr(V:Val) => true requires isStr(V) [simplification]
  rule knownStr(vlk(VS:ValSeq, _I:Int)) => true requires allStr(VS) [simplification]

  // vlk/valSeqAt of an all-str table is a str element, never a heap ref NOR a list — kill BOTH
  // narrower junk branches. The `+` dispatch narrows each opaque lookup operand into ref(_) (deref
  // layer) AND into list(_) (the list-concat applyBin rule); a str element is neither, so both are
  // #Bottom. Without the list twin the `+` is (wrongly) read as list concatenation and sticks.
  rule { ref(_:Int) #Equals vlk(VS:ValSeq, _:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { vlk(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { ref(_:Int) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { list(_:ValSeq) #Equals vlk(VS:ValSeq, _:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { vlk(VS:ValSeq, _:Int) #Equals list(_:ValSeq) } => #Bottom requires allStr(VS) [simplification]
  rule { list(_:ValSeq) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals list(_:ValSeq) } => #Bottom requires allStr(VS) [simplification]

  // str `+` bridging opaque str Vals via codesProj under knownStr (confluent with the shared str+str).
  // fn-headed scoping (the P68 lesson): the bare-V spelling entailment-checks
  // every + in every proof step; these fire only on the roman-table lookups
  rule applyBin("+", str(CS:IntSeq), vlk(WS:ValSeq, J:Int))
    => str(seqConcat(CS, codesProj(vlk(WS, J))))
    requires allStr(WS) [simplification]
  rule applyBin("+", vlk(VS:ValSeq, I:Int), vlk(WS:ValSeq, J:Int))
    => str(seqConcat(codesProj(vlk(VS, I)), codesProj(vlk(WS, J))))
    requires allStr(VS) andBool allStr(WS) [simplification]

  // ---- the four per-place tables — held OPAQUE. Content DECLARED via allStr + the collapse below.
  // lowercase codes: i=105 v=118 x=120 l=108 c=99 d=100 m=109; '' = str(.IntSeq).
  syntax ValSeq ::= "mTab" [function, total]
  syntax ValSeq ::= "hTab" [function, total]
  syntax ValSeq ::= "tTab" [function, total]
  syntax ValSeq ::= "uTab" [function, total]
  rule allStr(mTab) => true [simplification]
  rule allStr(hTab) => true [simplification]
  rule allStr(tTab) => true [simplification]
  rule allStr(uTab) => true [simplification]

  // ---- the collapse: the executed deref materializes the EXACT ListExpr literal on the heap; its
  // valSeqAt folds to vlk(<literal>, I), and this pins <literal> to the opaque symbol. vlk-headed LHS
  // (a constructor-headed reverse fold is rejected by kompile). One rule per table.
  rule vlk(vCons(str(.IntSeq), vCons(str(iCons(109, .IntSeq)), .ValSeq)), I:Int) => vlk(mTab, I) [simplification]

  rule vlk(vCons(str(.IntSeq),
    vCons(str(iCons(99, .IntSeq)),
    vCons(str(iCons(99, iCons(99, .IntSeq))),
    vCons(str(iCons(99, iCons(99, iCons(99, .IntSeq)))),
    vCons(str(iCons(99, iCons(100, .IntSeq))),
    vCons(str(iCons(100, .IntSeq)),
    vCons(str(iCons(100, iCons(99, .IntSeq))),
    vCons(str(iCons(100, iCons(99, iCons(99, .IntSeq)))),
    vCons(str(iCons(100, iCons(99, iCons(99, iCons(99, .IntSeq))))),
    vCons(str(iCons(99, iCons(109, .IntSeq))), .ValSeq)))))))))), I:Int) => vlk(hTab, I) [simplification]

  rule vlk(vCons(str(.IntSeq),
    vCons(str(iCons(120, .IntSeq)),
    vCons(str(iCons(120, iCons(120, .IntSeq))),
    vCons(str(iCons(120, iCons(120, iCons(120, .IntSeq)))),
    vCons(str(iCons(120, iCons(108, .IntSeq))),
    vCons(str(iCons(108, .IntSeq)),
    vCons(str(iCons(108, iCons(120, .IntSeq))),
    vCons(str(iCons(108, iCons(120, iCons(120, .IntSeq)))),
    vCons(str(iCons(108, iCons(120, iCons(120, iCons(120, .IntSeq))))),
    vCons(str(iCons(120, iCons(99, .IntSeq))), .ValSeq)))))))))), I:Int) => vlk(tTab, I) [simplification]

  rule vlk(vCons(str(.IntSeq),
    vCons(str(iCons(105, .IntSeq)),
    vCons(str(iCons(105, iCons(105, .IntSeq))),
    vCons(str(iCons(105, iCons(105, iCons(105, .IntSeq)))),
    vCons(str(iCons(105, iCons(118, .IntSeq))),
    vCons(str(iCons(118, .IntSeq)),
    vCons(str(iCons(118, iCons(105, .IntSeq))),
    vCons(str(iCons(118, iCons(105, iCons(105, .IntSeq)))),
    vCons(str(iCons(118, iCons(105, iCons(105, iCons(105, .IntSeq))))),
    vCons(str(iCons(105, iCons(120, .IntSeq))), .ValSeq)))))))))), I:Int) => vlk(uTab, I) [simplification]

  // ---- result = M[t] + H[h] + T[e] + U[u], left-assoc; indices are applyBin's floored //,% forms.
  // t = n//1000, h = (n//100)%10, e = (n//10)%10, u = n%10.
  syntax Val ::= romanRes(Int) [function]
  rule romanRes(N:Int) => str(seqConcat(seqConcat(seqConcat(
      codesProj(vlk(mTab, (N -Int pyMod(N, 1000)) /Int 1000)),
      codesProj(vlk(hTab, pyMod((N -Int pyMod(N, 100)) /Int 100, 10)))),
      codesProj(vlk(tTab, pyMod((N -Int pyMod(N, 10)) /Int 10, 10)))),
      codesProj(vlk(uTab, pyMod(N, 10))))) [simplification]
endmodule
