module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The source grammar mirrors the constructors emitted by py2mpy.py for the
  // deliberately small Python fragment used by solution.py.
  syntax Pgm ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "ListExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"

  // Semantic values. Ints is a mathematical finite sequence of integers.
  syntax Ints ::= List{Int, ","}
  syntax Val ::= "VInt" "(" Int ")"
               | "VBool" "(" Bool ")"
               | "VList" "(" "[" Ints "]" ")"
  syntax Vals ::= List{Val, ","}

  syntax Run ::= "Invoke" "(" Pgm "," String "," Vals ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  configuration <k> $PGM:Run </k>

  // The environment and whole translated program are explicit. Recursive
  // source calls therefore re-enter Invoke with the same parsed program.
  syntax Env ::= "env" "(" Ints "," Int ")"
  syntax KItem ::= "exec" "(" Stmts "," Env "," Pgm ")"
                 | "eval" "(" Expr "," Env "," Pgm ")"
                 | "decide" "(" Stmts "," Stmts "," Stmts "," Env "," Pgm ")"
                 | "listSecond" "(" Expr "," Env "," Pgm ")"
                 | "makePair" "(" Val ")"
                 | "binopRight" "(" Expr "," Env "," Pgm ")"
                 | "concatWith" "(" Val ")"
                 | "concat" "(" Val "," Val ")"
                 | "prepend" "(" Int ")"
                 | "callSecond" "(" Expr "," Env "," Pgm ")"
                 | "callWith" "(" Val "," Pgm ")"

  rule <k>
    Invoke(
      Module(ImportFrom(MOD, IMPS)
             FuncDef(F, PARAMS, BODY)),
      F,
      VList([IS]), VInt(D))
    => exec(BODY, env(IS, D),
            Module(ImportFrom(MOD, IMPS)
                   FuncDef(F, PARAMS, BODY))) ...
  </k>

  rule <k> exec(Return(E) _REST, ENV, PGM) => eval(E, ENV, PGM) ... </k>
  rule <k> exec(If(COND, THEN, ELSE) REST, ENV, PGM)
        => eval(COND, ENV, PGM)
        ~> decide(THEN, ELSE, REST, ENV, PGM) ... </k>
  rule <k> VBool(true) ~> decide(THEN, _ELSE, _REST, ENV, PGM)
        => exec(THEN, ENV, PGM) ... </k>
  rule <k> VBool(false) ~> decide(_THEN, .Stmts, REST, ENV, PGM)
        => exec(REST, ENV, PGM) ... </k>

  rule <k> eval(Name("numbers"), env(IS, _D), _PGM) => VList([IS]) ... </k>
  rule <k> eval(Name("delimeter"), env(_IS, D), _PGM) => VInt(D) ... </k>
  rule <k> eval(Int(I), _ENV, _PGM) => VInt(I) ... </k>

  // This is the exact meaning of the source test len(numbers) <= 1. Lists
  // carry their structure directly, so the primitive can decide after at most
  // two constructors (as a real Python list's stored length does).
  rule <k> eval(Compare(Call(Name("len"), Name("numbers")),
                       CmpOp("<=", Int(1))),
                  env(.Ints, _D), _PGM)
        => VBool(true) ... </k>
  rule <k> eval(Compare(Call(Name("len"), Name("numbers")),
                       CmpOp("<=", Int(1))),
                  env(_I, .Ints, _D), _PGM)
        => VBool(true) ... </k>
  rule <k> eval(Compare(Call(Name("len"), Name("numbers")),
                       CmpOp("<=", Int(1))),
                  env(_I, _J, _REST, _D), _PGM)
        => VBool(false) ... </k>

  rule <k> eval(Subscript(Name("numbers"), Int(0)),
                  env(I, _REST, _D), _PGM)
        => VInt(I) ... </k>
  rule <k> eval(Subscript(Name("numbers"),
                         Slice(Int(1), NoBound, NoBound)),
                  env(_I, REST, _D), _PGM)
        => VList([REST]) ... </k>

  rule <k> eval(ListExpr(E1, E2), ENV, PGM)
        => eval(E1, ENV, PGM) ~> listSecond(E2, ENV, PGM) ... </k>
  rule <k> V1:Val ~> listSecond(E2, ENV, PGM)
        => eval(E2, ENV, PGM) ~> makePair(V1) ... </k>
  rule <k> VInt(J) ~> makePair(VInt(I)) => VList([I, J]) ... </k>

  rule <k> eval(BinOp("+", E1, E2), ENV, PGM)
        => eval(E1, ENV, PGM) ~> binopRight(E2, ENV, PGM) ... </k>
  rule <k> V1:Val ~> binopRight(E2, ENV, PGM)
        => eval(E2, ENV, PGM) ~> concatWith(V1) ... </k>
  rule <k> V2:Val ~> concatWith(V1) => concat(V1, V2) ... </k>
  rule <k> concat(VList([.Ints]), VList([JS])) => VList([JS]) ... </k>
  rule <k> concat(VList([I, IS]), VList([JS]))
        => concat(VList([IS]), VList([JS])) ~> prepend(I) ... </k>
  rule <k> VList([JS]) ~> prepend(I) => VList([I, JS]) ... </k>

  rule <k> eval(Call(Name("intersperse"), E1, E2), ENV, PGM)
        => eval(E1, ENV, PGM) ~> callSecond(E2, ENV, PGM) ... </k>
  rule <k> V1:Val ~> callSecond(E2, ENV, PGM)
        => eval(E2, ENV, PGM) ~> callWith(V1, PGM) ... </k>
  rule <k> VInt(D) ~> callWith(VList([IS]), PGM)
        => Invoke(PGM, "intersperse", VList([IS]), VInt(D)) ... </k>
endmodule
