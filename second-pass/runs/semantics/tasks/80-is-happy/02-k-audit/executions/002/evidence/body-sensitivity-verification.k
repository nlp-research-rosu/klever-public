requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // These constructor terms are exactly the translated statement blocks in
  // solution.mpy, named here so the reachability claims stay readable.
  syntax Stmts ::= "happyLoopBody" [macro]
  rule happyLoopBody
    => If(
         Compare(
           Subscript(Name("s"), Name("i")),
           CmpOp("==",
             Subscript(Name("s"), BinOp("+", Name("i"), Int(1))))),
         Return(Bool(false)),
         .Stmts)
       If(
         Compare(
           Subscript(Name("s"), Name("i")),
           CmpOp("==",
             Subscript(Name("s"), BinOp("+", Name("i"), Int(2))))),
         Return(Bool(false)),
         .Stmts)
       If(
         Compare(
           Subscript(Name("s"), BinOp("+", Name("i"), Int(1))),
           CmpOp("==",
             Subscript(Name("s"), BinOp("+", Name("i"), Int(2))))),
         Return(Bool(false)),
         .Stmts)
       AugAssign(Name("i"), "+", Int(1))
       .Stmts

  syntax Expr ::= "happyLoopCondition" [macro]
  rule happyLoopCondition
    => Compare(
         BinOp("+", Name("i"), Int(2)),
         CmpOp("<", Call(Name("len"), Name("s"))))

  syntax Stmts ::= "isHappyBody" [macro]
  rule isHappyBody
    => If(
         Compare(Call(Name("len"), Name("s")), CmpOp("<", Int(3))),
         Return(Bool(false)),
         .Stmts)
       Assign(Name("i"), Int(0))
       While(happyLoopCondition, happyLoopBody)
       Return(Bool(false))
       .Stmts

  syntax Val ::= "isHappyClosure" [function, total]
  rule isHappyClosure => closureVal("s", isHappyBody, 0)

  syntax Scope ::= "solutionScope" [function, total]
  rule solutionScope
    => scope(.Map [ "is_happy" <- isHappyClosure ], parent(-1))

  // Totalized in-bounds indexing: on concrete sequences safeAt has exactly
  // the reference intSeqAt equations. The bridge only applies under the valid
  // index condition established by the loop guard.
  syntax Int ::= safeAt(IntSeq, Int) [function, total]
  rule safeAt(iCons(C:Int, _:IntSeq), 0) => C
  rule safeAt(iCons(_:Int, R:IntSeq), I:Int) => safeAt(R, I -Int 1)
    requires I >Int 0

  rule intSeqAt(IS:IntSeq, I:Int) => safeAt(IS, I)
    requires I >=Int 0 andBool I <Int isLen(IS)
    [priority(60)]

  // Declarative sliding-window contract from starting index I.
  syntax Bool ::= happyFrom(IntSeq, Int) [function, total]

  rule happyFrom(IS:IntSeq, I:Int) => true
    requires I >=Int 0
     andBool I +Int 2 >=Int isLen(IS)

  rule happyFrom(IS:IntSeq, I:Int) => false
    requires I >=Int 0
     andBool I +Int 2 <Int isLen(IS)
     andBool safeAt(IS, I) ==Int safeAt(IS, I +Int 1)

  rule happyFrom(IS:IntSeq, I:Int) => false
    requires I >=Int 0
     andBool I +Int 2 <Int isLen(IS)
     andBool safeAt(IS, I) =/=Int safeAt(IS, I +Int 1)
     andBool safeAt(IS, I) ==Int safeAt(IS, I +Int 2)

  rule happyFrom(IS:IntSeq, I:Int) => false
    requires I >=Int 0
     andBool I +Int 2 <Int isLen(IS)
     andBool safeAt(IS, I) =/=Int safeAt(IS, I +Int 1)
     andBool safeAt(IS, I) =/=Int safeAt(IS, I +Int 2)
     andBool safeAt(IS, I +Int 1) ==Int safeAt(IS, I +Int 2)

  rule happyFrom(IS:IntSeq, I:Int) => happyFrom(IS, I +Int 1)
    requires I >=Int 0
     andBool I +Int 2 <Int isLen(IS)
     andBool safeAt(IS, I) =/=Int safeAt(IS, I +Int 1)
     andBool safeAt(IS, I) =/=Int safeAt(IS, I +Int 2)
     andBool safeAt(IS, I +Int 1) =/=Int safeAt(IS, I +Int 2)

  syntax Bool ::= isHappySpec(IntSeq) [function, total]
  rule isHappySpec(IS:IntSeq) => false
    requires isLen(IS) <Int 3
  rule isHappySpec(IS:IntSeq) => happyFrom(IS, 0)
    requires isLen(IS) >=Int 3
endmodule

// Second proof stage. The rule is the already-proved happy-loop-correct claim
// from LOOP-SPEC, installed as a lemma so the public function proof can use it.
module VERIFICATION
  imports VERIFICATION-BASE

  rule
    <k>
      While(happyLoopCondition, happyLoopBody)
      ~> (Return(Bool(true)) .Stmts)
      ~> #endcall
    =>
      #pop
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("s" |-> str(IS:IntSeq)) ("i" |-> 0),
        parent(0))
      ...
    </scopes>
    <ret> noRet => retV(happyFrom(IS, 0)) </ret>
    [priority(40)]
endmodule
