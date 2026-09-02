module MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Index ")"
                | "Call" "(" Expr "," Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Expr "," NoBound "," NoBound ")"
  syntax NoBound ::= "NoBound"
endmodule

module XOR-SEMANTICS
  imports MPY-SYNTAX

  // Text is either concrete (empty/cons) or a symbolic N-character segment.
  // A Stream denotes an arbitrary sequence of bits, least-significant bit
  // first.  The length is stored by segment, so leading zeroes are preserved.
  syntax Stream ::= "seed" "(" Int ")"
  syntax Stream ::= "next" "(" Stream ")" [function]
  syntax Bool ::= "head" "(" Stream ")" [function, total]
  syntax Text ::= "empty"
                | "cons" "(" Bool "," Text ")"
                | "segment" "(" Int "," Stream ")"

  syntax Value ::= "str" "(" Text ")"
                 | "i" "(" Int ")"
                 | "truth" "(" Bool ")"
  syntax Args ::= "Args" "(" Value "," Value ")"
  syntax Env ::= "env" "(" Value "," Value ")"
  syntax ExecResult ::= "normal" "(" Env ")"
                      | "returned" "(" Value ")"
  syntax KResult ::= Value | ExecResult
  syntax Sem ::= Value | ExecResult
  syntax Sem ::= "eval" "(" Expr "," Env "," Stmts ")"
               | "equal" "(" Sem "," Sem ")" [strict]
               | "concat" "(" Sem "," Sem ")" [strict]
               | "index" "(" Sem "," Sem ")" [strict]
               | "tail" "(" Sem ")" [strict]
               | "call" "(" Sem "," Sem "," Stmts ")" [strict(1, 2)]
               | "returnValue" "(" Sem ")" [strict]
               | "makeReturn" "(" Sem ")" [strict]
               | "exec" "(" Stmts "," Env "," Stmts ")"
               | "decide" "(" Sem "," Stmts "," Stmts "," Stmts "," Env "," Stmts ")" [strict(1)]
               | "continue" "(" Sem "," Stmts "," Stmts ")" [strict(1)]

  rule head(seed(I)) => (I modInt 2) ==Int 1
  rule next(seed(I)) => seed(I divInt 2)

  configuration
    <k> $PGM:Module </k>
    <args> $ARGS:Args </args>

  rule <k> Module(FuncDef("string_xor", Params("a", "b"), BODY))
        => exec(BODY, env(A, B), BODY) ... </k>
       <args> Args(A, B) </args>

  rule eval(Name("a"), env(A, _), _) => A
  rule eval(Name("b"), env(_, B), _) => B
  rule eval(Str(""), _, _) => str(empty)
  rule eval(Str("0"), _, _) => str(cons(false, empty))
  rule eval(Str("1"), _, _) => str(cons(true, empty))
  rule eval(Int(I), _, _) => i(I)

  rule eval(Compare(E1, CmpOp("==", E2)), ENV, BODY)
    => equal(eval(E1, ENV, BODY), eval(E2, ENV, BODY))
  rule eval(BinOp("+", E1, E2), ENV, BODY)
    => concat(eval(E1, ENV, BODY), eval(E2, ENV, BODY))
  rule eval(Subscript(E, I:Expr), ENV, BODY)
    => index(eval(E, ENV, BODY), eval(I, ENV, BODY))
  rule eval(Subscript(E, Slice(Int(1), NoBound, NoBound)), ENV, BODY)
    => tail(eval(E, ENV, BODY))
  rule eval(Call(Name("string_xor"), E1, E2), ENV, BODY)
    => call(eval(E1, ENV, BODY), eval(E2, ENV, BODY), BODY)

  rule equal(str(empty), str(empty)) => truth(true)
  rule equal(str(cons(_, _)), str(empty)) => truth(false)
  rule equal(str(empty), str(cons(_, _))) => truth(false)
  rule equal(str(segment(N, _)), str(empty)) => truth(N ==Int 0)
  rule equal(str(empty), str(segment(N, _))) => truth(N ==Int 0)
  rule equal(str(cons(B1, empty)), str(cons(B2, empty)))
    => truth(B1 ==Bool B2)

  rule concat(str(cons(B, empty)), str(T)) => str(cons(B, T))
  rule index(str(cons(B, _)), i(0)) => str(cons(B, empty))
  rule index(str(segment(N, S)), i(0)) => str(cons(head(S), empty))
    requires N >Int 0
  rule tail(str(cons(_, T))) => str(T)
  rule tail(str(segment(N, S))) => str(segment(N -Int 1, next(S)))
    requires N >Int 0

  rule call(A, B, BODY) => returnValue(exec(BODY, env(A, B), BODY))
  rule returnValue(returned(V)) => V

  rule exec(.Stmts, ENV, _) => normal(ENV)
  rule exec(Return(E) _REST, ENV, BODY) => makeReturn(eval(E, ENV, BODY))
  rule exec(If(E, THEN, ELSE) REST, ENV, BODY)
    => decide(eval(E, ENV, BODY), THEN, ELSE, REST, ENV, BODY)
  rule decide(truth(C), THEN, _, REST, ENV, BODY)
    => continue(exec(THEN, ENV, BODY), REST, BODY)
    requires C
  rule decide(truth(C), _, ELSE, REST, ENV, BODY)
    => continue(exec(ELSE, ENV, BODY), REST, BODY)
    requires notBool C
  rule makeReturn(V:Value) => returned(V)
  rule continue(returned(V), _, _) => returned(V)
  rule continue(normal(ENV), REST, BODY) => exec(REST, ENV, BODY)
endmodule

module XOR
  imports XOR-SEMANTICS
endmodule
