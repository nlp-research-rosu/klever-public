requires "reference-semantics/semantics.k"

module PARSE-MUSIC-BASE
  imports MPY

  // An arbitrary finite sequence of valid notes.
  syntax Music ::= ".Music"
                 | whole(Music)
                 | half(Music)
                 | quarter(Music)

  // Opaque canonical encoding of a valid, whitespace-delimited music string.
  // The standard split implementation is concrete; the rule below supplies
  // an equivalent proof-only iterator without changing concrete execution.
  syntax IntSeq ::= musicCodes(Music)

  // Keeping the symbolic sequence as an iterator preserves the constructor
  // relation between the input note and the expected output during induction.
  syntax Iterable ::= musicIter(Music)
  rule <k> #iterNext(musicIter(.Music)) => #iterDone ... </k>
  rule <k> #iterNext(musicIter(whole(M:Music)))
        => #iterYield(str(iCons(111, .IntSeq)), musicIter(M)) ... </k>
  rule <k> #iterNext(musicIter(half(M:Music)))
        => #iterYield(str(iCons(111, iCons(124, .IntSeq))), musicIter(M)) ... </k>
  rule <k> #iterNext(musicIter(quarter(M:Music)))
        => #iterYield(str(iCons(46, iCons(124, .IntSeq))), musicIter(M)) ... </k>

  // AUDITOR MUTATION: the candidate's proof-only split bridge is removed.

  // Executable specification: left-to-right append of each note duration.
  syntax ValSeq ::= musicAcc(ValSeq, Music) [function, total]
  rule musicAcc(A:ValSeq, .Music) => A
  rule musicAcc(A:ValSeq, whole(M:Music))
    => musicAcc(valSeqConcat(A, vCons(4, .ValSeq)), M)
  rule musicAcc(A:ValSeq, half(M:Music))
    => musicAcc(valSeqConcat(A, vCons(2, .ValSeq)), M)
  rule musicAcc(A:ValSeq, quarter(M:Music))
    => musicAcc(valSeqConcat(A, vCons(1, .ValSeq)), M)

  // The loop's only local-scope effect is rebinding "note".
  syntax Val ::= musicLast(Val, Music) [function, total]
  rule musicLast(V:Val, .Music) => V
  rule musicLast(_:Val, whole(M:Music))
    => musicLast(str(iCons(111, .IntSeq)), M)
  rule musicLast(_:Val, half(M:Music))
    => musicLast(str(iCons(111, iCons(124, .IntSeq))), M)
  rule musicLast(_:Val, quarter(M:Music))
    => musicLast(str(iCons(46, iCons(124, .IntSeq))), M)

  // These macros are the exact translated implementation fragments from
  // solution.mpy, named so the reachability claims remain readable.
  syntax Stmts ::= "parseMusicLoopBody" [macro]
  rule parseMusicLoopBody
    => If(Compare(Name("note"), CmpOp("==", Str("o"))),
          Expr(Call(Attribute(Name("beats"), "append"), Int(4))),
          If(Compare(Name("note"), CmpOp("==", Str("o|"))),
             Expr(Call(Attribute(Name("beats"), "append"), Int(2))),
             Expr(Call(Attribute(Name("beats"), "append"), Int(1)))))

  syntax Stmts ::= "parseMusicBody" [macro]
  rule parseMusicBody
    => Assign(Name("beats"), ListExpr(.Exprs))
       Assign(Name("note"), Str(""))
       For(Name("note"),
           Call(Attribute(Name("music_string"), "split"), .Exprs),
           parseMusicLoopBody)
       Return(Name("beats"))

  syntax Val ::= "parseMusicClosure" [macro]
  rule parseMusicClosure
    => closureVal(("music_string", .ParamNames), parseMusicBody, 0)

  syntax Module ::= "parseMusicProgram" [macro]
  rule parseMusicProgram
    => Module(
         ImportFrom("typing", "List")
         FuncDef("parse_music", Params("music_string"),
           parseMusicBody))
endmodule

module PARSE-MUSIC-VERIFICATION
  imports PARSE-MUSIC-BASE

  // Proven loop lemma used by the entry-point proof.  The matching claim in
  // PARSE-MUSIC-LOOP-SPEC is proved against PARSE-MUSIC-BASE, where this rule
  // is absent, so the lemma cannot prove itself.
  rule
    <k> #loop(musicIter(M:Music), Name("note"), parseMusicLoopBody)
        => .K
        ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            ("music_string" |-> S:Val)
            ("beats" |-> ref(B))
            ("note" |-> (N:Val => musicLast(N, M))),
            P:Parent)
          ...
    </scopes>
    <heap>
      ... B:Int |-> list(A:ValSeq => musicAcc(A, M)) ...
    </heap>
    [priority(35)]
endmodule
