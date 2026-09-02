// A small, executable semantics for exactly the Python-AST constructors used by
// solution.mpy.  The source translator is purely syntactic; all computation is
// defined here.

requires "rat.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports FLOAT-SYNTAX
  imports RAT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module(Stmts)
  syntax Stmts  ::= List{Stmt, ""}
  syntax Stmt   ::= FuncDef(String, Params, Stmts)
                  | "If" "(" Exp "," Stmts "," ")"
                  | Assign(Exp, Exp)
                  | Return(Exp)

  syntax Params  ::= Params(Strings)
  syntax Strings ::= List{String, ","}

  syntax Exp ::= Int(Int)
               | Float(Float)
               | Name(String)
               | Call(Exp, Exprs)
  syntax Exp ::= UnaryOp(String, Exp) [strict(2)]
               | BinOp(String, Exp, Exp) [seqstrict(2, 3)]
               | Compare(Exp, CmpOp) [strict(1)]
  syntax CmpOp ::= CmpOp(String, Exp)
  syntax Exprs ::= List{Exp, ","}

  syntax NumValue ::= VInt(Int) | VRat(Rat)
  syntax Value  ::= NumValue
                  | VFloat(Float)
                  | VSqrt(Rat)
                  | VRounded(Int)
                  | VBool(Bool)
  syntax Values ::= List{Value, ","}
  syntax Args   ::= Args(Values)
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports RAT
  imports BOOL
  imports MAP

  configuration
    <triangle>
      <k> launch($PGM:Program, $ARGS:Args) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult </result>
    </triangle>

  syntax Result ::= "NoResult" | Value
  syntax Exp ::= Value
  syntax KResult ::= Value

  syntax Function ::= function(Strings, Stmts)
  syntax KItem ::= launch(Program, Args)
                 | exec(Stmts)
                 | invoke(String, Values)
                 | bind(Strings, Values)
                 | branch(Stmts)
                 | assignTo(String)
                 | "returnValue"
                 | compareLE(Value)
                 | "round2"

  // Module loading and entry-point invocation.
  rule launch(Module(SS), Args(VS))
    => exec(SS) ~> invoke("triangle_area", VS)

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule <k> FuncDef(F, Params(PS), BODY) => .K ...</k>
       <functions> FS => FS [ F <- function(PS, BODY) ] </functions>

  rule <k> invoke(F, VS) => bind(PS, VS) ~> exec(BODY) ...</k>
       <functions>... F |-> function(PS, BODY) ...</functions>

  rule bind(.Strings, .Values) => .K
  rule <k> bind((P, PS), (V, VS)) => bind(PS, VS) ...</k>
       <env> RHO => RHO [ P <- V ] </env>

  // Statements and non-local return from the one active function call.
  rule If(E, THEN,) => E ~> branch(THEN)
  rule VBool(true)  ~> branch(THEN) => exec(THEN)
  rule VBool(false) ~> branch(_) => .K

  rule Assign(Name(X), E) => E ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ...</k>
       <env> RHO => RHO [ X <- V ] </env>

  rule Return(E) => E ~> returnValue
  rule <k> V:Value ~> returnValue ~> _REST:K => .K </k>
       <env> _ => .Map </env>
       <functions> _ => .Map </functions>
       <result> NoResult => V </result>

  // Literals, variables, and unary negation.
  rule Int(I) => VInt(I)
  rule Float(F) => VFloat(F)
  rule <k> Name(X) => V ...</k>
       <env>... X |-> V ...</env>

  rule UnaryOp("-", VInt(I))   => VInt(0 -Int I)
  rule UnaryOp("-", VRat(R)) => VRat(0 -Rat R)

  // Python numeric promotion for the arithmetic needed by this program.
  syntax Rat ::= asRat(NumValue) [function, total]
  rule asRat(VInt(I)) => I
  rule asRat(VRat(R)) => R

  rule BinOp("+", VInt(I), VInt(J)) => VInt(I +Int J)
  rule BinOp("+", V:NumValue, W:NumValue)
    => VRat(asRat(V) +Rat asRat(W))
    [owise]

  rule BinOp("-", VInt(I), VInt(J)) => VInt(I -Int J)
  rule BinOp("-", V:NumValue, W:NumValue)
    => VRat(asRat(V) -Rat asRat(W))
    [owise]

  rule BinOp("*", VInt(I), VInt(J)) => VInt(I *Int J)
  rule BinOp("*", V:NumValue, W:NumValue)
    => VRat(asRat(V) *Rat asRat(W))
    [owise]

  rule BinOp("/", V:NumValue, W:NumValue)
    => VRat(asRat(V) /Rat asRat(W))
  rule BinOp("**", V:NumValue, VFloat(0.5))
    => VSqrt(asRat(V))

  // The emitted comparisons are single-link chains.  The continuation keeps
  // Python's left-to-right expression evaluation explicit.
  rule Compare(V:Value, CmpOp("<=", E)) => E ~> compareLE(V)
  rule VInt(J) ~> compareLE(VInt(I))
    => VBool(I <=Int J)
  rule W:NumValue ~> compareLE(V:NumValue)
    => VBool(asRat(V) <=Rat asRat(W))
    [owise]

  // round(sqrt(x), 2), represented exactly as an integer count of hundredths.
  // The integer/rational algorithm avoids relying on backend floating-point
  // hooks, so the same semantics is executable and symbolically provable.
  rule Call(Name("round"), E, Int(2)) => E ~> round2
  rule VSqrt(R) ~> round2 => VRounded(sqrtHundredths(R))
  rule VInt(I) ~> round2 => VInt(I)

  syntax Int ::= sqrtHundredths(Rat) [function]
               | findSqrtUpper(Rat, Int) [function]
               | bisectSqrt(Rat, Int, Int) [function]
               | finishSqrtRound(Rat, Int) [function]

  rule sqrtHundredths(R)
    => findSqrtUpper(R *Rat 10000, 1)
    [concrete(R), simplification]

  rule findSqrtUpper(R, H)
    => finishSqrtRound(R, bisectSqrt(R, H /Int 2, H))
    requires R <Rat (H *Int H)
  rule findSqrtUpper(R, H)
    => findSqrtUpper(R, H *Int 2)
    requires R >=Rat (H *Int H)

  rule bisectSqrt(_, L, H) => L
    requires H -Int L <=Int 1
  rule bisectSqrt(R, L, H)
    => bisectSqrt(R, (L +Int H) /Int 2, H)
    requires H -Int L >Int 1
     andBool (((L +Int H) /Int 2) *Int ((L +Int H) /Int 2) <=Rat R)
  rule bisectSqrt(R, L, H)
    => bisectSqrt(R, L, (L +Int H) /Int 2)
    requires H -Int L >Int 1
     andBool (R <Rat ((L +Int H) /Int 2) *Int ((L +Int H) /Int 2))

  rule finishSqrtRound(R, L) => L +Int 1
    requires (4 *Rat R) >Rat ((2 *Int L +Int 1) *Int (2 *Int L +Int 1))
  rule finishSqrtRound(R, L) => L
    requires (4 *Rat R) <Rat ((2 *Int L +Int 1) *Int (2 *Int L +Int 1))
  rule finishSqrtRound(R, L) => L
    requires (4 *Rat R) ==Rat ((2 *Int L +Int 1) *Int (2 *Int L +Int 1))
     andBool L %Int 2 ==Int 0
  rule finishSqrtRound(R, L) => L +Int 1
    requires (4 *Rat R) ==Rat ((2 *Int L +Int 1) *Int (2 *Int L +Int 1))
     andBool L %Int 2 =/=Int 0
endmodule
