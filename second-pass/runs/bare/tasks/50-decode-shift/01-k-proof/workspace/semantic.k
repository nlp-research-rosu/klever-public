requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax PyModule ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Expr ")"
                | "ListComp" "(" Expr "," CompFor ")"

  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Expr ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports VERIFICATION

  syntax Value ::= VInt(Int) [constructor]
                 | VBool(Bool) [constructor]
                 | VText(String) [constructor]
                 | VChar(Int) [constructor]
                 | VChars(Chars) [constructor]
                 | VList(Chars) [constructor]

  syntax KItem ::= exec(Stmts)
                 | eval(Expr)
                 | "discard"
                 | "finish"
                 | binLeft(String, Expr)
                 | binRight(String, Value)
                 | "doOrd"
                 | "doChr"
                 | "doJoin"
                 | comp(String, Expr, Chars)
                 | compTail(String, Expr, Chars, Int)
                 | prepend(Int)

  configuration
    <m>
      <k> $PGM:PyModule </k>
      <s> nil </s>
      <ch> 0 </ch>
      <input> $INPUT:Chars </input>
      <result> .K </result>
    </m>

  // Loading the translated definition also invokes its required entry point.
  rule <k> Module(FuncDef("decode_shift", Params("s"), BODY)) => exec(BODY) </k>
       <s> _ => CS </s>
       <input> CS </input>

  rule <k> exec(.Stmts) => .K </k>
  rule exec(Expr(E) REST) => eval(E) ~> discard ~> exec(REST)
  rule exec(Return(E) _REST) => eval(E) ~> finish

  rule _V:Value ~> discard => .K
  rule <k> V:Value ~> finish => .K </k>
       <result> .K => V </result>

  rule eval(Int(I)) => VInt(I)
  rule eval(Bool(B)) => VBool(B)
  rule eval(Str("")) => VChars(nil)
  rule eval(Str(S)) => VText(S) requires S =/=String ""
  rule <k> eval(Name("s")) => VChars(CS) ...</k>
       <s> CS </s>
  rule <k> eval(Name("ch")) => VChar(C) ...</k>
       <ch> C </ch>

  rule eval(BinOp(OP, LEFT, RIGHT))
    => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule V:Value ~> binLeft(OP, RIGHT)
    => eval(RIGHT) ~> binRight(OP, V)
  rule VInt(J) ~> binRight("+", VInt(I)) => VInt(I +Int J)
  rule VInt(J) ~> binRight("-", VInt(I)) => VInt(I -Int J)
  rule VInt(J) ~> binRight("%", VInt(I)) => VInt(I modInt J)

  rule eval(Call(Name("ord"), ARG)) => eval(ARG) ~> doOrd
  rule VChar(C) ~> doOrd => VInt(C)
  rule VText(S) ~> doOrd => VInt(ordChar(S))

  rule eval(Call(Name("chr"), ARG)) => eval(ARG) ~> doChr
  rule VInt(C) ~> doChr => VChar(C)

  rule eval(Call(Attribute(Str(""), "join"), ARG))
    => eval(ARG) ~> doJoin
  rule VList(CS) ~> doJoin => VChars(CS)

  // A single-generator, unfiltered comprehension over a character sequence.
  // The translator supplies Bool(true) when the Python comprehension has no ifs.
  rule <k> eval(ListComp(E, CompFor(Name(X), Name(Y), Bool(true))))
          => comp(X, E, CS) ...</k>
       <s> CS </s>
    requires Y ==String "s"

  rule comp(_X, _E, nil) => VList(nil)
  rule <k> comp(X, E, cons(C, CS))
          => eval(E) ~> compTail(X, E, CS, OLD) ...</k>
       <ch> OLD => C </ch>
    requires X ==String "ch"
  rule <k> VChar(D) ~> compTail(X, E, CS, SAVED)
          => comp(X, E, CS) ~> prepend(D) ...</k>
       <ch> _CURRENT => SAVED </ch>
  rule VList(DS) ~> prepend(D) => VList(cons(D, DS))
endmodule

module SEMANTIC
  imports MPY-SEMANTIC
endmodule
