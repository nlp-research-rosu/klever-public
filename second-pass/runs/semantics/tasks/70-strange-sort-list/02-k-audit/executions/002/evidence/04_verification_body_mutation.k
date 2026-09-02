requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The exact loop condition and body emitted by py2mpy.py for solution.py.
  // Naming them keeps the invariant and the whole-function claim readable.
  syntax Expr ::= strangeCondition() [macro]
  rule strangeCondition()
    => Compare(Name("i"),
         CmpOp("<", Call(Name("len"), Name("ordered"))))

  syntax Stmts ::= strangeLoopBody() [macro]
  rule strangeLoopBody()
    => If(
         Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             // AUDITOR MUTATION: even iterations always select index 0.
             Subscript(Name("ordered"), Int(0)))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Subscript(
               Name("ordered"),
               BinOp(
                 "-",
                 BinOp(
                   "-",
                   Call(Name("len"), Name("ordered")),
                   BinOp("//", Name("i"), Int(2))),
                 Int(1))))))
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= strangeBody() [macro]
  rule strangeBody()
    => Assign(Name("ordered"), Call(Name("sorted"), Name("lst")))
       Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       While(strangeCondition(), strangeLoopBody())
       Return(Name("result"))

  // Element selected at iteration I from an ascending sequence S of length N.
  // pyMod(I, 2) is either zero or one for the nonnegative loop index.
  syntax Val ::= strangePick(ValSeq, Int, Int) [function, total]
  rule strangePick(S:ValSeq, I:Int, _N:Int)
    => valSeqAt(S, (I -Int pyMod(I, 2)) /Int 2)
    requires pyMod(I, 2) ==Int 0
  rule strangePick(S:ValSeq, I:Int, N:Int)
    => valSeqAt(S, N -Int ((I -Int pyMod(I, 2)) /Int 2) -Int 1)
    requires pyMod(I, 2) =/=Int 0

  // Prefix produced after I loop iterations.  It is opaque at a symbolic
  // positive index; the append equation is its induction equation and exactly
  // matches the mutation performed by one loop step.
  syntax ValSeq ::= strangePrefix(ValSeq, Int, Int)
    [function, total, symbol(strangePrefix), no-evaluators]
  rule strangePrefix(_S:ValSeq, 0, _N:Int) => .ValSeq
  rule valSeqConcat(
         strangePrefix(S:ValSeq, I:Int, N:Int),
         vCons(valSeqAt(S, I /Int 2), .ValSeq))
    => strangePrefix(S, I +Int 1, N)
    requires I >=Int 0 andBool pyMod(I, 2) ==Int 0
    [simplification]
  rule valSeqConcat(
         strangePrefix(S:ValSeq, I:Int, N:Int),
         vCons(
           valSeqAt(
             S,
             N -Int
               ((I -Int (((I %Int 2) +Int 2) %Int 2)) /Int 2)
               +Int -1),
           .ValSeq))
    => strangePrefix(S, I +Int 1, N)
    requires I >=Int 0
      andBool (((I %Int 2) +Int 2) %Int 2) =/=Int 0
    [simplification]

  syntax ValSeq ::= strangeResult(ValSeq) [function, total]
  rule strangeResult(S:ValSeq)
    => strangePrefix(S, vsLen(S), vsLen(S))

  // ValSeq lengths are natural numbers.  This remains true for opaque
  // symbolic sequences such as sortVS(S), for which vsLen cannot unfold.
  rule 0 <=Int vsLen(_S:ValSeq) => true [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Compositional summary of the loop-invariant claim in LOOP-SPEC.  prove.sh
  // first proves that claim against VERIFICATION-BASE (where this rule is not
  // present), then uses the proved summary for the whole-function claim.
  rule
    <k> #while(strangeCondition(), strangeLoopBody()) => .K ... </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> LIST:Val
        "ordered" |-> ref(HO:Int)
        "result"  |-> ref(HR:Int)
        "i"       |-> I:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> BS:Scope
      =>
      1 |-> scope(
        "lst"     |-> LIST
        "ordered" |-> ref(HO)
        "result"  |-> ref(HR)
        "i"       |-> N:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> BS
    </scopes>
    <heap>
      HO |-> list(S:ValSeq)
      HR |-> list(ACC:ValSeq)
      =>
      HO |-> list(S)
      HR |-> list(strangePrefix(S, N, N))
    </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 2 </heapLoc>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int N
      andBool N ==Int vsLen(S)
      andBool ACC ==K strangePrefix(S, I, N)
    [priority(30)]
endmodule
