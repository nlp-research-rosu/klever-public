requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports MAP

  // The constructor syntax emitted by py2mpy.py for the subset used by
  // solution.py.  Source expressions and run-time values are deliberately
  // different sorts: evaluating an Expr produces a Value.
  syntax Program ::= Module(Stmts)
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Assign(Expr, Expr)
                | While(Expr, Stmts)
                | If(Expr, Stmts, Stmts)
                | Return(Expr)

  syntax Params ::= Params(Strings)
  syntax Strings ::= List{String, ","}

  syntax Expr ::= Name(String)
                | Int(Int)
                | Bool(Bool)
                | Call(Expr, Exprs)
                | BinOp(String, Expr, Expr)
                | Compare(Expr, CmpOp)
                | Subscript(Expr, Slice)
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= CmpOp(String, Expr)
  syntax Slice ::= Slice(Bound, Bound, Bound)
  syntax Bound ::= Expr | "NoBound"

  syntax Value ::= pyInt(Int) | pyBool(Bool) | pyStr(String)
  syntax Values ::= List{Value, ""}
  syntax Result ::= "NoResult" | Result(Value)

  syntax KItem ::= exec(Stmts)
                 | assignTo(String)
                 | whileGuard(Expr, Stmts)
                 | ifGuard(Stmts, Stmts)
                 | "ReturnValue"
                 | binLeft(String, Expr)
                 | binRight(String, Value)
                 | compareLeft(String, Expr)
                 | compareRight(String, Value)
                 | sliceBase(Bound, Bound, Bound)
                 | sliceLower(String, Bound, Bound)
                 | sliceUpper(String, Int, Bound)
                 | sliceStep(String, Int, Int)
                 | "LenCall"

  syntax KResult ::= Value
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  configuration
    <mpy>
      <k> $PGM:Program ~> start </k>
      <args> $ARGS:Values </args>
      <env> .Map </env>
      <out> NoResult </out>
    </mpy>

  syntax KItem ::= "start"

  // Total string-search primitive.  On concrete strings it is exactly K's
  // builtin findString; symbolically it remains a total Int-valued operation,
  // which gives the prover the ordinary integer ordering laws it needs.
  syntax Int ::= indexOf(String, String, Int) [function, total]
  rule indexOf(HAYSTACK, NEEDLE, FROM)
    => findString(HAYSTACK, NEEDLE, FROM) [concrete]

  // Loading the one top-level function also invokes the requested HumanEval
  // entry point.  Function bodies themselves are still evaluated by the
  // statement and expression rules below.
  rule <k> Module(FuncDef("cycpattern_check", Params("a", "b"), BODY)) ~> start
         => exec(BODY) ... </k>
       <args> pyStr(A) pyStr(B) </args>
       <env> .Map => ("a" |-> pyStr(A)) ("b" |-> pyStr(B)) </env>

  // Statement sequencing.
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => S ~> exec(SS) ... </k>

  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> If(COND, THEN, ELSE) => COND ~> ifGuard(THEN, ELSE) ... </k>
  rule <k> pyBool(BV) ~> ifGuard(THEN, _) => exec(THEN) ... </k>
    requires BV
  rule <k> pyBool(BV) ~> ifGuard(_, ELSE) => exec(ELSE) ... </k>
    requires notBool BV

  rule <k> While(COND, BODY) => COND ~> whileGuard(COND, BODY) ... </k>
  rule <k> pyBool(BV) ~> whileGuard(COND, BODY)
         => exec(BODY) ~> While(COND, BODY) ... </k>
    requires BV
  rule <k> pyBool(BV) ~> whileGuard(_, _) => .K ... </k>
    requires notBool BV

  rule <k> Return(E) => E ~> ReturnValue ... </k>
  rule <k> V:Value ~> ReturnValue ~> _REST => .K </k>
       <out> _ => Result(V) </out>

  // Literals and variables.
  rule <k> Int(I) => pyInt(I) ... </k>
  rule <k> Bool(B) => pyBool(B) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>

  // The only builtin needed by the submitted program.
  rule <k> Call(Name("len"), E:Expr) => E ~> LenCall ... </k>
  rule <k> pyStr(S) ~> LenCall => pyInt(lengthString(S)) ... </k>

  // Left-to-right binary expression evaluation.
  rule <k> BinOp(OP, L, R) => L ~> binLeft(OP, R) ... </k>
  rule <k> L:Value ~> binLeft(OP, R) => R ~> binRight(OP, L) ... </k>
  rule <k> pyInt(R) ~> binRight("+", pyInt(L)) => pyInt(L +Int R) ... </k>
  rule <k> pyStr(R) ~> binRight("+", pyStr(L)) => pyStr(L +String R) ... </k>

  // Single comparisons (the exact Compare shape used in solution.mpy).
  rule <k> Compare(L, CmpOp(OP, R)) => L ~> compareLeft(OP, R) ... </k>
  rule <k> L:Value ~> compareLeft(OP, R) => R ~> compareRight(OP, L) ... </k>
  rule <k> pyInt(R) ~> compareRight("<", pyInt(L))
         => pyBool(true) ... </k>
    requires L <Int R
  rule <k> pyInt(R) ~> compareRight("<", pyInt(L))
         => pyBool(false) ... </k>
    requires L >=Int R
  rule <k> pyStr(HAYSTACK) ~> compareRight("in", pyStr(NEEDLE))
         => pyBool(true) ... </k>
    requires indexOf(HAYSTACK, NEEDLE, 0) >=Int 0
  rule <k> pyStr(HAYSTACK) ~> compareRight("in", pyStr(NEEDLE))
         => pyBool(false) ... </k>
    requires indexOf(HAYSTACK, NEEDLE, 0) <Int 0

  // Python slices used by b[i:] and b[:i].  Bounds are evaluated in source
  // order.  NoBound defaults to 0 / string length; step defaults to 1.
  rule <k> Subscript(BASE, Slice(LO, HI, STEP))
         => BASE ~> sliceBase(LO, HI, STEP) ... </k>
  rule <k> pyStr(S) ~> sliceBase(NoBound, HI, STEP)
         => sliceLower(S, HI, STEP) ... </k>
  rule <k> pyStr(S) ~> sliceBase(LO:Expr, HI, STEP)
         => LO ~> sliceLower(S, HI, STEP) ... </k>
  rule <k> sliceLower(S, HI, _STEP)
         => sliceUpper(S, 0, HI) ... </k>
  rule <k> pyInt(LO) ~> sliceLower(S, HI, _STEP)
         => sliceUpper(S, LO, HI) ... </k>
  rule <k> sliceUpper(S, LO, NoBound)
         => pyStr(substrString(S, LO, lengthString(S))) ... </k>
  rule <k> sliceUpper(S, LO, HI:Expr)
         => HI ~> sliceStep(S, LO, 1) ... </k>
  rule <k> pyInt(HI) ~> sliceStep(S, LO, 1)
         => pyStr(substrString(S, LO, HI)) ... </k>

endmodule
