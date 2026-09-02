module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Exprs ::= List{Expr, ","}

  syntax Bound ::= Expr | "NoBound"
  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Slice" "(" Bound "," Bound "," Bound ")"
                | "TupleExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Ops ::= ".Ops" | "Op" "(" String "," Ops ")"
  syntax Ints ::= ".Ints" | "Num" "(" Int "," Ints ")"
  syntax OpList ::= "ops" "(" Ops ")"
  syntax NumList ::= "ints" "(" Ints ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL

  syntax KItem ::= "invoke"
                 | "exec" "(" Stmts ")"
                 | "answer" "(" Int ")"

  syntax Text ::= "noText"
                | "builder" "(" Ops "," Ints "," Ops "," Ints ")"

  configuration
    <mpy>
      <k> $PGM:Pgm ~> invoke </k>
      <operators> $OPS:OpList </operators>
      <operands> $OPERANDS:NumList </operands>
      <expression> noText </expression>
    </mpy>

  rule <k> Module(FuncDef("do_algebra", Params("operator", "operand"), BODY))
            ~> invoke => exec(BODY) ... </k>

  rule <k> exec(Assign(
                    Name("expression"),
                    Call(Name("str"), Subscript(Name("operand"), Int(0))))
                  REST) => exec(REST) ... </k>
       <operators> ops(OS) </operators>
       <operands> ints(Num(I, IS)) </operands>
       <expression> _ => builder(OS, Num(I, IS), OS, IS) </expression>

  rule <k> exec(For(
                    TupleExpr(Name("oprt"), Name("oprn")),
                    Call(Name("zip"),
                         Name("operator"),
                         Subscript(Name("operand"),
                                   Slice(Int(1), NoBound, NoBound))),
                    AugAssign(
                      Name("expression"),
                      "+",
                      BinOp("+", Name("oprt"),
                            Call(Name("str"), Name("oprn")))))
                  REST) => exec(REST) ... </k>
       <expression>
         builder(ALLOPS, ALLINTS, OS, IS)
         => builder(ALLOPS, ALLINTS, .Ops, .Ints)
       </expression>
    requires aligned(OS, IS)

  rule <k> exec(Return(Call(Name("eval"), Name("expression"))) _REST)
            => answer(pyEval(ALLOPS, ALLINTS)) ... </k>
       <expression> builder(ALLOPS, ALLINTS, .Ops, .Ints) </expression>

  // The zip loop consumes exactly one operand for each operator.
  syntax Bool ::= aligned ( Ops , Ints ) [function, total]
  rule aligned(.Ops, .Ints) => true
  rule aligned(Op(_, OS), Num(_, IS)) => aligned(OS, IS)
  rule aligned(.Ops, Num(_, _)) => false
  rule aligned(Op(_, _), .Ints) => false

  // A small expression evaluator with Python's precedence and associativity.
  // parsePow consumes one right-associative exponentiation group.
  syntax ParseResult ::= "parsed" "(" Int "," Ops "," Ints ")"
  syntax ParseResult ::= parsePow ( Ops , Ints ) [function]
                       | powCombine ( Int , ParseResult ) [function]

  rule parsePow(.Ops, Num(I, .Ints)) => parsed(I, .Ops, .Ints)
  rule parsePow(Op("**", OS), Num(I, IS))
    => powCombine(I, parsePow(OS, IS))
  rule parsePow(Op("+", OS), Num(I, IS))
    => parsed(I, Op("+", OS), IS)
  rule parsePow(Op("-", OS), Num(I, IS))
    => parsed(I, Op("-", OS), IS)
  rule parsePow(Op("*", OS), Num(I, IS))
    => parsed(I, Op("*", OS), IS)
  rule parsePow(Op("//", OS), Num(I, IS))
    => parsed(I, Op("//", OS), IS)
  rule powCombine(I, parsed(J, OS, IS))
    => parsed(powNat(I, J), OS, IS)

  syntax Tokens ::= "tokens" "(" Ops "," Ints ")"
  syntax Tokens ::= powerPass ( Ops , Ints ) [function]
                  | powerNext ( ParseResult ) [function]
                  | powerCons ( Int , String , Tokens ) [function]

  rule powerPass(OS, IS) => powerNext(parsePow(OS, IS))
  rule powerNext(parsed(I, .Ops, .Ints))
    => tokens(.Ops, Num(I, .Ints))
  rule powerNext(parsed(I, Op(O, OS), IS))
    => powerCons(I, O, powerPass(OS, IS))
  rule powerCons(I, O, tokens(OS, IS))
    => tokens(Op(O, OS), Num(I, IS))

  // parseMul consumes one left-associative multiplication/division group.
  syntax ParseResult ::= parseMul ( Ops , Ints ) [function]
  rule parseMul(.Ops, Num(I, .Ints)) => parsed(I, .Ops, .Ints)
  rule parseMul(Op("*", OS), Num(I, Num(J, IS)))
    => parseMul(OS, Num(I *Int J, IS))
  rule parseMul(Op("//", OS), Num(I, Num(J, IS)))
    => parseMul(OS, Num(I /Int J, IS))
    requires J =/=Int 0
  rule parseMul(Op("+", OS), Num(I, IS))
    => parsed(I, Op("+", OS), IS)
  rule parseMul(Op("-", OS), Num(I, IS))
    => parsed(I, Op("-", OS), IS)

  syntax Tokens ::= mulPass ( Ops , Ints ) [function]
                  | mulNext ( ParseResult ) [function]
                  | mulCons ( Int , String , Tokens ) [function]
  rule mulPass(OS, IS) => mulNext(parseMul(OS, IS))
  rule mulNext(parsed(I, .Ops, .Ints))
    => tokens(.Ops, Num(I, .Ints))
  rule mulNext(parsed(I, Op(O, OS), IS))
    => mulCons(I, O, mulPass(OS, IS))
  rule mulCons(I, O, tokens(OS, IS))
    => tokens(Op(O, OS), Num(I, IS))

  // Only addition/subtraction remain, so a left fold completes evaluation.
  syntax Int ::= addPass ( Ops , Ints ) [function]
  rule addPass(.Ops, Num(I, .Ints)) => I
  rule addPass(Op("+", OS), Num(I, Num(J, IS)))
    => addPass(OS, Num(I +Int J, IS))
  rule addPass(Op("-", OS), Num(I, Num(J, IS)))
    => addPass(OS, Num(I -Int J, IS))

  syntax Int ::= pyEval ( Ops , Ints ) [function]
               | afterPower ( Tokens ) [function]
               | afterMul ( Tokens ) [function]
  rule pyEval(OS, IS) => afterPower(powerPass(OS, IS))
  rule afterPower(tokens(OS, IS)) => afterMul(mulPass(OS, IS))
  rule afterMul(tokens(OS, IS)) => addPass(OS, IS)

  syntax Int ::= powNat ( Int , Int ) [function]
  rule powNat(_, 0) => 1
  rule powNat(A, E) => A *Int powNat(A, E -Int 1)
    requires E >Int 0
endmodule
