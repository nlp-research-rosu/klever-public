requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmt ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Slice ")"
                | "ListComp" "(" Expr "," CompFor ")"
                | "Call" "(" Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= "NoBound" | Expr
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Expr ")"

  syntax Ints ::= "nil"
                | "cons" "(" Int "," Ints ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "listVal" "(" Ints ")"
  syntax Env ::= "emptyEnv"
               | "bind" "(" String "," Val "," Env ")"

  syntax KItem ::= "run" "(" Pgm "," Ints "," Ints "," Int ")"
                 | "result" "(" Int ")"

  // The second list is the unmodified function argument; the first is the
  // zero-based-even-position scan cursor. ACC is the running value of sum.
  configuration <k> run($PGM:Pgm, $INPUT:Ints, $INPUT:Ints, 0) </k>

  syntax Val ::= "lookup" "(" String "," Env ")" [function]
  rule lookup(X, bind(X, V, _)) => V
  rule lookup(X, bind(Y, _, ENV)) => lookup(X, ENV)
    requires X =/=String Y

  syntax Val ::= "eval" "(" Expr "," Env ")" [function]
  rule eval(Int(I), _) => intVal(I)
  rule eval(Name(X), ENV) => lookup(X, ENV)

  rule eval(BinOp("%", LEFT, RIGHT), ENV)
    => intVal(asInt(eval(LEFT, ENV)) modInt asInt(eval(RIGHT, ENV)))

  rule eval(Compare(LEFT, CmpOp("!=", RIGHT)), ENV)
    => boolVal(asInt(eval(LEFT, ENV)) =/=Int asInt(eval(RIGHT, ENV)))

  rule eval(Subscript(BASE, Slice(NoBound, NoBound, Int(2))), ENV)
    => listVal(everyOther(asInts(eval(BASE, ENV))))

  syntax Int ::= "asInt" "(" Val ")" [function]
  syntax Bool ::= "asBool" "(" Val ")" [function]
  syntax Ints ::= "asInts" "(" Val ")" [function]
  rule asInt(intVal(I)) => I
  rule asBool(boolVal(B)) => B
  rule asInts(listVal(IS)) => IS

  syntax Ints ::= "everyOther" "(" Ints ")" [function]
  rule everyOther(nil) => nil
  rule everyOther(cons(I, nil)) => cons(I, nil)
  rule everyOther(cons(I, cons(_, IS))) => cons(I, everyOther(IS))

  syntax Bool ::= "testAt" "(" Expr "," String "," Int "," String "," Ints ")" [function]
  rule testAt(COND, VAR, I, PARAM, ORIGINAL)
    => asBool(eval(COND,
         bind(VAR, intVal(I), bind(PARAM, listVal(ORIGINAL), emptyEnv))))

  syntax Int ::= "valueAt" "(" Expr "," String "," Int "," String "," Ints ")" [function]
  rule valueAt(BODY, VAR, I, PARAM, ORIGINAL)
    => asInt(eval(BODY,
         bind(VAR, intVal(I), bind(PARAM, listVal(ORIGINAL), emptyEnv))))

  // Operational semantics for sum([body for var in base[::2] if cond]).
  // Keeping PGM in the machine state makes every transition traceable to the
  // parsed source term. The tail after two list cells is the next cursor.
  rule <k> run(Module(FuncDef(_FNAME, Params(PARAM),
                    Return(Call(Name("sum"),
                      ListComp(_BODY, CompFor(Name(_VAR),
                        Subscript(Name(PARAM),
                          Slice(NoBound, NoBound, Int(2))), _COND)))))),
                 nil, _ORIGINAL, ACC)
        => result(ACC) ... </k>

  rule <k> run(Module(FuncDef(_FNAME, Params(PARAM),
                    Return(Call(Name("sum"),
                      ListComp(BODY, CompFor(Name(VAR),
                        Subscript(Name(PARAM),
                          Slice(NoBound, NoBound, Int(2))), COND)))))),
                 cons(I, nil), ORIGINAL, ACC)
        => result(ACC +Int valueAt(BODY, VAR, I, PARAM, ORIGINAL)) ... </k>
    requires testAt(COND, VAR, I, PARAM, ORIGINAL)

  rule <k> run(Module(FuncDef(_FNAME, Params(PARAM),
                    Return(Call(Name("sum"),
                      ListComp(_BODY, CompFor(Name(VAR),
                        Subscript(Name(PARAM),
                          Slice(NoBound, NoBound, Int(2))), COND)))))),
                 cons(I, nil), ORIGINAL, ACC)
        => result(ACC) ... </k>
    requires notBool testAt(COND, VAR, I, PARAM, ORIGINAL)

  rule <k> run(Module(FuncDef(_FNAME, Params(PARAM),
                    Return(Call(Name("sum"),
                      ListComp(BODY, CompFor(Name(VAR),
                        Subscript(Name(PARAM),
                          Slice(NoBound, NoBound, Int(2))), COND)))))) #as PGM,
                 cons(I, cons(_SKIPPED, REST)), ORIGINAL, ACC)
        => run(PGM, REST, ORIGINAL,
             ACC +Int valueAt(BODY, VAR, I, PARAM, ORIGINAL)) ... </k>
    requires testAt(COND, VAR, I, PARAM, ORIGINAL)

  rule <k> run(Module(FuncDef(_FNAME, Params(PARAM),
                    Return(Call(Name("sum"),
                      ListComp(_BODY, CompFor(Name(VAR),
                        Subscript(Name(PARAM),
                          Slice(NoBound, NoBound, Int(2))), COND)))))) #as PGM,
                 cons(I, cons(_SKIPPED, REST)), ORIGINAL, ACC)
        => run(PGM, REST, ORIGINAL, ACC) ... </k>
    requires notBool testAt(COND, VAR, I, PARAM, ORIGINAL)
endmodule
