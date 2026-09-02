requires "reference-semantics/semantics.k"

module MATCH-PARENS-VERIFICATION-BODY-MUTATED
  imports MPY

  // Symbolic normalization of a fresh Map insertion (the hooked operation
  // already normalizes when the map is ground).
  rule BASE:Map [ N:Int <- SCOPE:Scope ]
    => BASE (N |-> SCOPE)
    requires notBool (N in_keys(BASE))
    [simplification]

  // Symbolic counterpart of deleting a freshly allocated scope at #pop.
  // Ground Map update already has this behavior through the MAP hook.
  rule ((BASE:Map (N:Int |-> _SCOPE:Scope)) [ N <- undef ]) => BASE
    requires notBool (N in_keys(BASE))
    [simplification]

  // Targeted symbolic forms of the literal assignment and arithmetic updates
  // in is_good.  They avoid strictness freezers around primitive Int tokens.
  rule <k> (Assign(Name("balance"), Int(0)):Stmt) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           M:Map => M [ "balance" <- 0 ],
           P:Parent) ...
       </scopes>
    requires notBool ("$cells" in_keys(M))
    [priority(40)]

  rule <k> (AugAssign(Name("balance"), "+", Int(1)):Stmt)
        => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           M:Map => M [ "balance" <- B +Int 1 ],
           P:Parent) ...
       </scopes>
    requires "balance" in_keys(M)
     andBool {M["balance"]}:>Val ==K B
     andBool notBool ("$cells" in_keys(M))
    [priority(40)]

  rule <k> (AugAssign(Name("balance"), "-", Int(1)):Stmt)
        => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           M:Map => M [ "balance" <- B -Int 1 ],
           P:Parent) ...
       </scopes>
    requires "balance" in_keys(M)
     andBool {M["balance"]}:>Val ==K B
     andBool notBool ("$cells" in_keys(M))
    [priority(40)]

  rule <k> (For(Name("char"), Name("s"), BODY:Stmts):Stmt)
        => #loop(str(S), Name("char"), BODY) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("s" |-> str(S:IntSeq)) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    [priority(40)]

  // Fused frame-entry form for is_good: MPY-CALL frame allocation,
  // parameter binding, and the literal balance assignment, ending at the
  // actual loop proved in spec.k.
  rule <k> #applyK(toCall(GOOD:Val), (str(S:IntSeq), .Vals))
           ~> CONT
        => #loop(str(S), Name("char"), isGoodLoopBody)
           ~> If(Compare(Name("balance"), CmpOp("==", Int(0))),
                Return(Str("T")) .Stmts,
                .Stmts)
           ~> Return(Str(""))
           ~> #endcall </k>
       <env> CALLER:Int => N </env>
       <scopes>
         BASE:Map
         => BASE (N |-> scope(
              ("s" |-> str(S)) ("balance" |-> 0),
              parent(0)))
       </scopes>
       <scopeLoc> N:Int => N +Int 1 </scopeLoc>
       <stack>
         STACK:List
         => ListItem(frame(CONT, CALLER, N)) STACK
       </stack>
    requires GOOD ==K isGoodClosure
     andBool notBool (N in_keys(BASE))
    [priority(40)]

  // Symbolic call/branch continuation for the two exact calls made by
  // match_parens.  This is the reference Call + strict If behavior specialized
  // to the constructor-valued truthy/falsey strings returned by is_good.
  syntax KItem ::= #goodBranch(Stmts, Stmts)
                 | #forceBranch(IntSeq, Stmts, Stmts)
                 | #forceGood(IntSeq, Int)
                 | #runIsGood(IntSeq)

  rule <k> (If(
              Call(Name("is_good"),
                BinOp("+",
                  Subscript(Name("lst"), Int(0)),
                  Subscript(Name("lst"), Int(1)))),
              THEN:Stmts, ELSE:Stmts):Stmt)
        => #runIsGood(seqConcat(A, B))
           ~> #forceBranch(seqConcat(A, B), THEN, ELSE) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
               "lst" |-> list(vCons(str(A:IntSeq),
                               vCons(str(B:IntSeq), .ValSeq))),
               parent(0))
             0 |-> scope(
               ("is_good" |-> GOOD:Val) _MODULE:Map,
               parent(-1)) ...
       </scopes>
    requires GOOD ==K isGoodClosure
    [priority(40)]

  rule <k> (If(
              Call(Name("is_good"),
                BinOp("+",
                  Subscript(Name("lst"), Int(1)),
                  Subscript(Name("lst"), Int(0)))),
              THEN:Stmts, ELSE:Stmts):Stmt)
        => #runIsGood(seqConcat(B, A))
           ~> #forceBranch(seqConcat(B, A), THEN, ELSE) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
               "lst" |-> list(vCons(str(A:IntSeq),
                               vCons(str(B:IntSeq), .ValSeq))),
               parent(0))
             0 |-> scope(
               ("is_good" |-> GOOD:Val) _MODULE:Map,
               parent(-1)) ...
       </scopes>
    requires GOOD ==K isGoodClosure
    [priority(40)]

  // Modular use of the separately proved isGoodCorrect claim.
  rule <k> #runIsGood(S:IntSeq) => goodValue(S, 0) ... </k>

  rule <k> V:Val ~> #forceBranch(S:IntSeq, THEN:Stmts, ELSE:Stmts)
        => #forceGood(S, 0) ~> V ~> #goodBranch(THEN, ELSE) ... </k>

  rule <k> str(iCons(84, .IntSeq))
           ~> #goodBranch(THEN:Stmts, _ELSE:Stmts)
        => THEN ... </k>
  rule <k> str(.IntSeq)
           ~> #goodBranch(_THEN:Stmts, ELSE:Stmts)
        => ELSE ... </k>

  syntax KItem ::= #expectedBranch(Bool, Stmts, Stmts)
  rule <k> #expectedBranch(B:Bool, THEN:Stmts, _ELSE:Stmts)
        => THEN ... </k>
    requires B
  rule <k> #expectedBranch(B:Bool, _THEN:Stmts, ELSE:Stmts)
        => ELSE ... </k>
    requires notBool B

  // Lockstep structural driver used to prove goodBranchCorrect.  V is kept
  // abstract on the LHS (rather than placing a function symbol under a rewrite
  // pattern), with equality pinning it to the mathematical helper result.
  rule <k> #forceGood(.IntSeq, B:Int)
           ~> _V:Val
           ~> #goodBranch(THEN:Stmts, ELSE:Stmts)
        => #expectedBranch(B ==Int 0, THEN, ELSE) ... </k>

  rule <k> #forceGood(iCons(40, R:IntSeq), B:Int)
           ~> _V:Val
           ~> #goodBranch(THEN:Stmts, ELSE:Stmts)
        => #forceGood(R, B +Int 1)
           ~> goodValue(R, B +Int 1)
           ~> #goodBranch(THEN, ELSE) ... </k>
    requires B >=Int 0

  rule <k> #forceGood(iCons(C:Int, R0:IntSeq), B:Int)
           ~> _V:Val
           ~> #goodBranch(THEN:Stmts, ELSE:Stmts)
        => #expectedBranch(false, THEN, ELSE) ... </k>
    requires C =/=Int 40
     andBool B -Int 1 <Int 0
     andBool B >=Int 0

  rule <k> #forceGood(iCons(C:Int, R:IntSeq), B:Int)
           ~> _V:Val
           ~> #goodBranch(THEN:Stmts, ELSE:Stmts)
        => #forceGood(R, B -Int 1)
           ~> goodValue(R, B -Int 1)
           ~> #goodBranch(THEN, ELSE) ... </k>
    requires C =/=Int 40
     andBool B -Int 1 >=Int 0
     andBool B >=Int 0

  // The same strictness limitation affects Return after a literal Str has
  // become a constructor Val.  All returns in solution.py are string
  // literals, so fuse literal evaluation with MPY-FUNCTIONS' Return rule.
  rule <k> (Return(Str(S:String)):Stmt) ~> _ => #pop </k>
       <ret> noRet => retV(str(strToCodes(S))) </ret>
    [priority(40)]

  // Proof-only symbolic execution lemmas for the three comparisons used by
  // the program.  The reference semantics' generated strictness coolers only
  // recognize constructor results, so hooked comparisons over symbolic Ints
  // otherwise remain under a freezer.  These rules are the corresponding
  // MPY lookup/applyCmp/If transitions fused into one step.
  rule <k> Compare(Name("char"), CmpOp("==", Str("(")))
        => true ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("char" |-> str(iCons(C:Int, .IntSeq))) _LOCALS:Map,
           _PARENT:Parent) ...
       </scopes>
    requires C ==Int 40
    [priority(40)]

  rule <k> Compare(Name("char"), CmpOp("==", Str("(")))
        => false ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("char" |-> str(iCons(C:Int, .IntSeq))) _LOCALS:Map,
           _PARENT:Parent) ...
       </scopes>
    requires C =/=Int 40
    [priority(40)]

  rule <k> Compare(Name("balance"), CmpOp("<", Int(0)))
        => true ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B <Int 0
    [priority(40)]

  rule <k> Compare(Name("balance"), CmpOp("<", Int(0)))
        => false ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B >=Int 0
    [priority(40)]

  rule <k> Compare(Name("balance"), CmpOp("==", Int(0)))
        => true ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B ==Int 0
    [priority(40)]

  rule <k> Compare(Name("balance"), CmpOp("==", Int(0)))
        => false ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B =/=Int 0
    [priority(40)]

  rule <k> (If(Compare(Name("char"), CmpOp("==", Str("("))),
               THEN:Stmts, _ELSE:Stmts):Stmt) => THEN ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("char" |-> str(iCons(C:Int, .IntSeq))) _LOCALS:Map,
           _PARENT:Parent) ...
       </scopes>
    requires C ==Int 40
    [priority(40)]

  rule <k> (If(Compare(Name("char"), CmpOp("==", Str("("))),
               _THEN:Stmts, ELSE:Stmts):Stmt) => ELSE ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("char" |-> str(iCons(C:Int, .IntSeq))) _LOCALS:Map,
           _PARENT:Parent) ...
       </scopes>
    requires C =/=Int 40
    [priority(40)]

  rule <k> (If(Compare(Name("balance"), CmpOp("<", Int(0))),
               THEN:Stmts, _ELSE:Stmts):Stmt) => THEN ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B <Int 0
    [priority(40)]

  rule <k> (If(Compare(Name("balance"), CmpOp("<", Int(0))),
               _THEN:Stmts, ELSE:Stmts):Stmt) => ELSE ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B >=Int 0
    [priority(40)]

  rule <k> (If(Compare(Name("balance"), CmpOp("==", Int(0))),
               THEN:Stmts, _ELSE:Stmts):Stmt) => THEN ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B ==Int 0
    [priority(40)]

  rule <k> (If(Compare(Name("balance"), CmpOp("==", Int(0))),
               _THEN:Stmts, ELSE:Stmts):Stmt) => ELSE ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("balance" |-> B:Int) _LOCALS:Map,
                         _PARENT:Parent) ...
       </scopes>
    requires B =/=Int 0
    [priority(40)]

  // The exact statement bodies emitted in solution.mpy.  Giving them names
  // keeps the configuration patterns in spec.k readable.
  syntax Stmts ::= "isGoodLoopBody" [function]
  rule isGoodLoopBody
    => If(Compare(Name("char"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)) .Stmts,
          AugAssign(Name("balance"), "-", Int(1)) .Stmts)
       If(Compare(Name("balance"), CmpOp("<", Int(0))),
          Return(Str("")) .Stmts,
          .Stmts)
       .Stmts

  syntax Stmts ::= "isGoodBody" [function]
  rule isGoodBody => Return(Str("")) .Stmts

  syntax Stmts ::= "matchParensBody" [function]
  rule matchParensBody
    => If(Call(Name("is_good"),
              BinOp("+",
                    Subscript(Name("lst"), Int(0)),
                    Subscript(Name("lst"), Int(1)))),
          Return(Str("Yes")) .Stmts,
          .Stmts)
       If(Call(Name("is_good"),
              BinOp("+",
                    Subscript(Name("lst"), Int(1)),
                    Subscript(Name("lst"), Int(0)))),
          Return(Str("Yes")) .Stmts,
          .Stmts)
       Return(Str("No"))
       .Stmts

  syntax Val ::= "isGoodClosure" [function]
  rule isGoodClosure
    => closureVal(("s", .ParamNames), isGoodBody, 0)

  syntax Val ::= "matchParensClosure" [function]
  rule matchParensClosure
    => closureVal(("lst", .ParamNames), matchParensBody, 0)

  // Mathematical balance scan corresponding to is_good.  The implementation
  // treats every non-'(' character as ')'; the entry theorem restricts inputs
  // to the two characters promised by the HumanEval contract.
  syntax Bool ::= goodFrom(IntSeq, Int) [function, total]
  rule goodFrom(.IntSeq, B:Int) => B ==Int 0
  rule goodFrom(iCons(C:Int, R:IntSeq), B:Int)
    => #if C ==Int 40
       #then goodFrom(R, B +Int 1)
       #else #if B -Int 1 <Int 0
             #then false
             #else goodFrom(R, B -Int 1)
             #fi
       #fi

  syntax Val ::= goodValue(IntSeq, Int) [function, total]
  rule goodValue(.IntSeq, B:Int)
    => #if B ==Int 0
       #then str(strToCodes("T"))
       #else str(.IntSeq)
       #fi
  rule goodValue(iCons(C:Int, R:IntSeq), B:Int)
    => #if C ==Int 40
       #then goodValue(R, B +Int 1)
       #else #if B -Int 1 <Int 0
             #then str(.IntSeq)
             #else goodValue(R, B -Int 1)
             #fi
       #fi

  syntax Bool ::= parensOnly(IntSeq) [function, total]
  rule parensOnly(.IntSeq) => true
  rule parensOnly(iCons(C:Int, R:IntSeq))
    => (C ==Int 40 orBool C ==Int 41) andBool parensOnly(R)

  syntax Val ::= expectedAnswer(IntSeq, IntSeq) [function]
  rule expectedAnswer(A:IntSeq, B:IntSeq) => str(strToCodes("Yes"))
    requires goodFrom(seqConcat(A, B), 0)
      orBool goodFrom(seqConcat(B, A), 0)
  rule expectedAnswer(A:IntSeq, B:IntSeq) => str(strToCodes("No"))
    requires notBool (goodFrom(seqConcat(A, B), 0)
      orBool goodFrom(seqConcat(B, A), 0))
endmodule
