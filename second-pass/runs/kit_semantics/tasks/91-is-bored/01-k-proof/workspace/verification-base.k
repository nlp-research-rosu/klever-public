requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY
  imports INT
  imports BOOL

  // These two macros are representation aliases for the exact AST emitted in
  // solution.mpy.  They do not replace or accelerate any MPY execution.
  syntax Stmts ::= "BORED-LOOP-BODY" [macro]
  rule BORED-LOOP-BODY
    => If(
         BoolOp(
           "or",
           Compare(Name("c"), CmpOp("==", Str("."))),
           Compare(Name("c"), CmpOp("==", Str("?"))),
           Compare(Name("c"), CmpOp("==", Str("!"))),
           .Exprs),
         If(
           Name("pending_i"),
           AugAssign(Name("count"), "+", Int(1)) .Stmts,
           .Stmts)
         Assign(Name("at_start"), Bool(true))
         Assign(Name("pending_i"), Bool(false))
         .Stmts,
         If(
           Name("at_start"),
           If(
             Compare(
               Call(Attribute(Name("c"), "strip"), .Exprs),
               CmpOp("!=", Str(""))),
             If(
               Compare(Name("c"), CmpOp("==", Str("I"))),
               Assign(Name("at_start"), Bool(false))
               Assign(Name("pending_i"), Bool(true))
               .Stmts,
               Assign(Name("at_start"), Bool(false))
               .Stmts)
             .Stmts,
             .Stmts)
           .Stmts,
           If(
             Name("pending_i"),
             If(
               Compare(
                 Call(Attribute(Name("c"), "strip"), .Exprs),
                 CmpOp("==", Str(""))),
               AugAssign(Name("count"), "+", Int(1))
               .Stmts,
               .Stmts)
             Assign(Name("pending_i"), Bool(false))
             .Stmts,
             .Stmts)
           .Stmts)
         .Stmts)
       .Stmts

  syntax Stmts ::= "BORED-FUNCTION-BODY" [macro]
  rule BORED-FUNCTION-BODY
    => Assign(Name("count"), Int(0))
       Assign(Name("at_start"), Bool(true))
       Assign(Name("pending_i"), Bool(false))
       Assign(Name("c"), Str(""))
       For(Name("c"), Name("S"), BORED-LOOP-BODY)
       If(
         Name("pending_i"),
         AugAssign(Name("count"), "+", Int(1)) .Stmts,
         .Stmts)
       Return(Name("count"))
       .Stmts

  // Mathematical scanner state: accumulated count, still at sentence start,
  // and "the first non-whitespace character was I, awaiting its boundary".
  syntax ScanState ::= scanState(Int, Bool, Bool)

  syntax Bool ::= isDelimiter(Int) [function, total]
  rule isDelimiter(46) => true [simplification]
  rule isDelimiter(63) => true [simplification]
  rule isDelimiter(33) => true [simplification]
  rule isDelimiter(C)  => false
    requires C =/=Int 46
     andBool C =/=Int 63
     andBool C =/=Int 33
    [simplification]

  syntax Int ::= flag(Bool) [function, total]
  rule flag(true)  => 1
  rule flag(false) => 0

  // `c.strip() == ""` for an MPY one-code-point string is exactly isWSC(C).
  // connection-spec.k proves the whitespace and non-whitespace cases without the
  // following bridge rules.
  syntax Bool ::= charIsWhitespace(Int) [function, total]
  rule charIsWhitespace(C) => true
    requires isWSC(C)
    [simplification]
  rule charIsWhitespace(C) => false
    requires notBool isWSC(C)
    [simplification]

  syntax Bool ::= charIsI(Int) [function, total]
  rule charIsI(C) => true
    requires C ==Int 73
    [simplification]
  rule charIsI(C) => false
    requires C =/=Int 73
    [simplification]

  // Operational bridges for the two pure comparisons left opaque by symbolic
  // evaluation of the supplied trim/reverse functions.  The exact binding,
  // expression, arbitrary continuation, and complete all-Int domain are covered
  // by the bridge-free claims in connection-spec.k.
  rule <k>
         Compare(
           Call(Attribute(Name("c"), "strip"), .Exprs),
           CmpOp("==", Str("")))
         => isWSC(C)
         ...
       </k>
       <env> 1 </env>
       <scopes>
         ... 1 |-> scope(
           ( "S"         |-> str(ORIG:IntSeq)
             "count"     |-> N:Int
             "at_start"  |-> A:Bool
             "pending_i" |-> P:Bool
             "c"         |-> str(iCons(C, .IntSeq)) ),
           parent(0))
         ...
       </scopes>
       [priority(40)]

  rule <k>
         Compare(
           Call(Attribute(Name("c"), "strip"), .Exprs),
           CmpOp("!=", Str("")))
         => notBool isWSC(C)
         ...
       </k>
       <env> 1 </env>
       <scopes>
         ... 1 |-> scope(
           ( "S"         |-> str(ORIG:IntSeq)
             "count"     |-> N:Int
             "at_start"  |-> A:Bool
             "pending_i" |-> P:Bool
             "c"         |-> str(iCons(C, .IntSeq)) ),
           parent(0))
         ...
       </scopes>
       [priority(40)]

  // One input-character transition.  The guards are disjoint and exhaustive.
  syntax ScanState ::= scanStep(Int, ScanState) [function, total]

  rule scanStep(C, scanState(N, A, P))
    => #if isDelimiter(C)
       #then scanState(N +Int flag(P), true, false)
       #else
         #if A
         #then
           #if charIsWhitespace(C)
           #then scanState(N, true, P)
           #else
             #if charIsI(C)
             #then scanState(N, false, true)
             #else scanState(N, false, P)
             #fi
           #fi
         #else
           #if P
           #then
             #if charIsWhitespace(C)
             #then scanState(N +Int 1, false, false)
             #else scanState(N, false, false)
             #fi
           #else scanState(N, false, false)
           #fi
         #fi
       #fi

  // Structurally recursive fold over every finite IntSeq represented by MPY.
  syntax ScanState ::= scan(IntSeq, ScanState) [function, total]
  rule scan(.IntSeq, ST) => ST
  rule scan(iCons(C, REST), ST) => scan(REST, scanStep(C, ST))

  // The post-loop if-statement counts an I that reaches end-of-input.
  syntax Int ::= finishScan(ScanState) [function, total]
  rule finishScan(scanState(N, A, P)) => N +Int flag(P)

  syntax Int ::= scanResult(IntSeq, Int, Bool, Bool) [function, total]
  rule scanResult(IS, N, A, P)
    => finishScan(scan(IS, scanState(N, A, P)))

  syntax Int ::= boredoms(IntSeq) [function, total]
  rule boredoms(IS) => scanResult(IS, 0, true, false)
endmodule
