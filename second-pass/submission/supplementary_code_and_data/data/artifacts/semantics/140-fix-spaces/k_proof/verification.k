requires "reference-semantics/semantics.k"

module FIX-SPACES-BASE
  imports MPY

  // The output contributed by one completed run of pending spaces.
  syntax IntSeq ::= pendingSpaces(Int) [function, total]
  rule pendingSpaces(N:Int)
    => #if N >Int 2
       #then iCons(45, .IntSeq)
       #else #if N ==Int 1
             #then iCons(95, .IntSeq)
             #else #if N ==Int 2
                   #then iCons(95, iCons(95, .IntSeq))
                   #else .IntSeq
                   #fi
             #fi
       #fi

  syntax IntSeq ::= appendPending(IntSeq, Int) [function, total]
  rule appendPending(A:IntSeq, N:Int)
    => #if N >Int 2
       #then seqConcat(A, iCons(45, .IntSeq))
       #else #if N ==Int 1
             #then seqConcat(A, iCons(95, .IntSeq))
             #else #if N ==Int 2
                   #then seqConcat(
                           A,
                           iCons(95, iCons(95, .IntSeq)))
                   #else A
                   #fi
             #fi
       #fi

  // Independent mathematical model of the loop.  A is the output already
  // emitted, IS is the unprocessed suffix, and N is the pending-space count.
  syntax IntSeq ::= fixSpacesLoop(IntSeq, IntSeq, Int) [function, total]
  rule fixSpacesLoop(A:IntSeq, .IntSeq, _:Int)
    => A
  rule fixSpacesLoop(A:IntSeq, iCons(32, R:IntSeq), N:Int)
    => fixSpacesLoop(A, R, N +Int 1)
    [simplification]
  rule fixSpacesLoop(A:IntSeq, iCons(C:Int, R:IntSeq), N:Int)
    => fixSpacesLoop(
         seqConcat(appendPending(A, N), iCons(C, .IntSeq)),
         R,
         0)
    requires C =/=Int 32
    [simplification]

  // The two remaining pieces of loop state are specified as folds too.  They
  // let the loop lemma describe the exact final local frame, not just result.
  syntax Int ::= trailingSpaces(IntSeq, Int) [function, total]
  rule trailingSpaces(.IntSeq, N:Int) => N
  rule trailingSpaces(iCons(32, R:IntSeq), N:Int)
    => trailingSpaces(R, N +Int 1)
    [simplification]
  rule trailingSpaces(iCons(C:Int, R:IntSeq), _:Int)
    => trailingSpaces(R, 0)
    requires C =/=Int 32
    [simplification]

  syntax IntSeq ::= finalChar(IntSeq, IntSeq) [function, total]
  rule finalChar(.IntSeq, CH:IntSeq) => CH
  rule finalChar(iCons(C:Int, R:IntSeq), _:IntSeq)
    => finalChar(R, iCons(C, .IntSeq))

  // Constructor terms copied exactly from solution.mpy, factored only to keep
  // the proof rule and claims readable.
  syntax Stmt ::= "fixSpacesLoopBodyStmt" [macro]
  rule fixSpacesLoopBodyStmt
    => If(
         BinOp(
           "-",
           Call(Name("ord"), Name("char")),
           Int(32)),
         If(Compare(Name("spaces"), CmpOp(">", Int(2))),
           AugAssign(Name("result"), "+", Str("-")),
           If(
             Compare(Name("spaces"), CmpOp("==", Int(1))),
             AugAssign(Name("result"), "+", Str("_")),
             If(
               Compare(Name("spaces"), CmpOp("==", Int(2))),
               AugAssign(Name("result"), "+", Str("__")),
               .Stmts)))
         AugAssign(Name("result"), "+", Name("char"))
         Assign(Name("spaces"), Int(0)),
         AugAssign(Name("spaces"), "+", Int(1)))

  syntax Stmts ::= "fixSpacesLoopBody" [macro]
  rule fixSpacesLoopBody => fixSpacesLoopBodyStmt

  syntax Stmt ::= "fixSpacesTailStmt" [macro]
  rule fixSpacesTailStmt
    => If(
         Compare(Name("spaces"), CmpOp(">", Int(2))),
         AugAssign(Name("result"), "+", Str("-")),
         If(
           Compare(Name("spaces"), CmpOp("==", Int(1))),
           AugAssign(Name("result"), "+", Str("_")),
           If(
             Compare(Name("spaces"), CmpOp("==", Int(2))),
             AugAssign(Name("result"), "+", Str("__")),
             .Stmts))
         )

  syntax Stmts ::= "fixSpacesTail" [macro]
  rule fixSpacesTail => fixSpacesTailStmt

  syntax Stmts ::= "fixSpacesFunctionBody" [macro]
  rule fixSpacesFunctionBody
    => Assign(Name("result"), Str(""))
       Assign(Name("spaces"), Int(0))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("text"), fixSpacesLoopBody)
       If(
         Compare(Name("spaces"), CmpOp(">", Int(2))),
         AugAssign(Name("result"), "+", Str("-")),
         If(
           Compare(Name("spaces"), CmpOp("==", Int(1))),
           AugAssign(Name("result"), "+", Str("_")),
           If(
             Compare(Name("spaces"), CmpOp("==", Int(2))),
             AugAssign(Name("result"), "+", Str("__")),
             .Stmts))
         )
       Return(Name("result"))

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef(
           "fix_spaces",
           Params("text"),
           fixSpacesFunctionBody))
endmodule

// The four arithmetic cases of this summary are proved in
// FIX-SPACES-FLUSH-SPEC before this module is used for the loop proof.
module FIX-SPACES-FLUSH-VERIFICATION
  imports FIX-SPACES-BASE

  rule
    <k>
      fixSpacesTailStmt
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(CH:IntSeq)),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION:Val,
          parent(-1)))
      (-1 |-> BUILTINS:Scope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(appendPending(A, N)))
          ("spaces" |-> N)
          ("char"   |-> str(CH)),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION,
          parent(-1)))
      (-1 |-> BUILTINS)
    </scopes>
    requires N >=Int 0
    [priority(30)]
endmodule

// The space and non-space body cases are proved in FIX-SPACES-STEP-SPEC.
module FIX-SPACES-STEP-VERIFICATION
  imports FIX-SPACES-FLUSH-VERIFICATION

  rule
    <k> fixSpacesLoopBodyStmt => .K ... </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |-> MODULE:Scope)
      (-1 |-> BUILTINS:Scope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(A))
          ("spaces" |-> N +Int 1)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |-> MODULE)
      (-1 |-> BUILTINS)
    </scopes>
    requires N >=Int 0
      andBool BUILTINS ==K builtinsScope
    [priority(20)]

  rule
    <k> fixSpacesLoopBodyStmt => .K ... </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(iCons(C:Int, .IntSeq))),
          parent(0)))
      (0 |-> MODULE:Scope)
      (-1 |-> BUILTINS:Scope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |->
            str(
              seqConcat(
                appendPending(A, N),
                iCons(C, .IntSeq))))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(C, .IntSeq))),
          parent(0)))
      (0 |-> MODULE)
      (-1 |-> BUILTINS)
    </scopes>
    requires N >=Int 0 andBool C =/=Int 32
      andBool BUILTINS ==K builtinsScope
    [priority(20)]
endmodule

// This module promotes the separately proved loop claim to a proof-only
// summary rule.  It is never imported by the LLVM concrete definition.
module FIX-SPACES-VERIFICATION
  imports FIX-SPACES-STEP-VERIFICATION

  rule
    <k>
      #loop(str(IS:IntSeq), Name("char"), fixSpacesLoopBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(CH:IntSeq)),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION:Val,
          parent(-1)))
      (-1 |-> BUILTINS:Scope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(fixSpacesLoop(A, IS, N)))
          ("spaces" |-> trailingSpaces(IS, N))
          ("char"   |-> str(finalChar(IS, CH))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION,
          parent(-1)))
      (-1 |-> BUILTINS)
    </scopes>
    requires N >=Int 0
      andBool BUILTINS ==K builtinsScope
    [priority(20)]
endmodule
