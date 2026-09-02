requires "rat.md"

// A deliberately small semantics for the pure-Python fragment used by
// solution.mpy.  Python numeric values are interpreted as exact rationals.
// This removes irrelevant IEEE-754 rounding from the functional proof while
// retaining the meaning of +, -, ordering, min, max, and division.
module MPY-SYNTAX
  imports RAT-SYNTAX
  imports BOOL
  imports MAP
  imports STRING

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}

  syntax Params ::= "Params" "(" Strings ")"
  syntax CellVars ::= "CellVars" "(" Strings ")"
  syntax FreeVars ::= "FreeVars" "(" Strings ")"

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "ListComp" "(" Expr "," CompFor ")"
                | "Bool" "(" Bool ")"

  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Expr ")"

  // Runtime input/output values.  vlist is a list of exact real (rational)
  // numbers.  For example, vlist(1, 2, 3) models Python [1.0, 2.0, 3.0].
  syntax Rats ::= List{Rat, ","}
  syntax Value ::= Rat
                 | "vlist" "(" Rats ")"
                 | "noResult"

  syntax Definition ::= "function" "(" Params "," Stmts ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports RAT

  configuration
    <python>
      <k> boot($PGM:Program, $ARGS:Value) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  syntax KItem ::= boot(Program, Value)
                 | exec(Stmts)
                 | invoke(String, Value)

  // Loading a module registers its definitions before invoking the requested
  // HumanEval entry point.  ImportFrom has no runtime effect because type
  // annotations have already been erased by the supplied AST translator.
  rule <k> boot(Module(SS), ARG) => exec(SS) ~> invoke("rescale_to_unit", ARG) </k>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(ImportFrom(_, _) SS) => exec(SS) ... </k>

  rule <k> exec(FuncDef(NAME, PARAMS, _, _, BODY) SS) => exec(SS) ... </k>
       <functions> FS => FS [ NAME <- function(PARAMS, BODY) ] </functions>

  rule <k> invoke(NAME, ARG) => exec(BODY) ... </k>
       <functions> ... NAME |-> function(Params(PARAM, .Strings), BODY) ... </functions>
       <env> _ => PARAM |-> ARG </env>

  rule <k> exec(Assign(Name(NAME), E) SS) => exec(SS) ... </k>
       <env> ENV => ENV [ NAME <- eval(E, ENV) ] </env>

  rule <k> exec(Return(E) _) => .K ... </k>
       <env> ENV </env>
       <result> _ => eval(E, ENV) </result>

  // Expression evaluation is functional: comprehensions use a temporary map
  // binding and therefore cannot mutate the surrounding function environment.
  syntax Value ::= eval(Expr, Map) [function]
                 | evalComp(Expr, String, Value, Map) [function]
                 | prepend(Rat, Value) [function]

  syntax Rat ::= evalNumber(Expr, Map) [function]
               | minValue(Value) [function]
               | maxValue(Value) [function]
               | minRats(Rat, Rats) [function]
               | maxRats(Rat, Rats) [function]

  rule eval(Name(NAME), (NAME |-> V:Value) _REST) => V

  rule eval(Call(Name("min"), E), ENV) => minValue(eval(E, ENV))
  rule eval(Call(Name("max"), E), ENV) => maxValue(eval(E, ENV))

  rule eval(BinOp(OP, L, R), ENV) => evalNumber(BinOp(OP, L, R), ENV)

  rule eval(ListComp(E, CompFor(Name(VAR), ITER, _)), ENV)
    => evalComp(E, VAR, eval(ITER, ENV), ENV)

  rule evalNumber(Name(NAME), (NAME |-> R:Rat) _REST) => R
  rule evalNumber(BinOp("-", L, R), ENV)
    => evalNumber(L, ENV) -Rat evalNumber(R, ENV)
  rule evalNumber(BinOp("/", L, R), ENV)
    => evalNumber(L, ENV) /Rat evalNumber(R, ENV)

  rule evalComp(_, _, vlist(.Rats), _) => vlist(.Rats)
  rule evalComp(E, VAR, vlist(R, RS), ENV)
    => prepend(evalNumber(E, ENV [ VAR <- R ]),
               evalComp(E, VAR, vlist(RS), ENV))

  rule prepend(R, vlist(RS)) => vlist(R, RS)

  rule minValue(vlist(R, RS)) => minRats(R, RS)
  rule maxValue(vlist(R, RS)) => maxRats(R, RS)

  rule minRats(M, .Rats) => M
  rule minRats(M, R, RS) => minRats(M, RS)
    requires M <Rat R
  rule minRats(M, R, RS) => minRats(M, RS)
    requires M ==Rat R
  rule minRats(M, R, RS) => minRats(R, RS)
    requires M >Rat R

  rule maxRats(M, .Rats) => M
  rule maxRats(M, R, RS) => maxRats(M, RS)
    requires M >Rat R
  rule maxRats(M, R, RS) => maxRats(M, RS)
    requires M ==Rat R
  rule maxRats(M, R, RS) => maxRats(R, RS)
    requires M <Rat R
endmodule
