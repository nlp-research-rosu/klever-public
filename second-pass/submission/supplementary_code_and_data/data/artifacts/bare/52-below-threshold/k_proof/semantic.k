module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The source subset emitted by py2mpy.py for solution.py.
  syntax Pgm    ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Stmt   ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  | "For" "(" Expr "," Expr "," Stmts ")"
                  | "If" "(" Expr "," Stmts "," Stmts ")"
                  | "Return" "(" Expr ")"
  syntax ParamItems ::= List{String, ","}
  syntax Params ::= "Params" "(" ParamItems ")"
  syntax Expr   ::= "Name" "(" String ")"
                  | "Bool" "(" Bool ")"
                  | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp  ::= "CmpOp" "(" String "," Expr ")"

  // A recursive input representation gives the prover an inductive shape.
  syntax IntSeq ::= "nil"
                  | "cons" "(" Int "," IntSeq ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  syntax Value ::= VInt(Int) | VBool(Bool) | VList(IntSeq)
  syntax Slot ::= "unbound" | "slot" "(" Value ")"
  syntax Result ::= "noResult" | "result" "(" Bool ")"

  syntax KItem ::= "boot"
                 | "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "ifK" "(" Stmts "," Stmts ")"
                 | "forK" "(" Expr "," Stmts ")"
                 | "loop" "(" Expr "," IntSeq "," Stmts ")"
                 | "cmpRight" "(" Expr ")"
                 | "cmpValues" "(" Value "," String ")"
                 | "returnK"

  configuration
    <bt>
      <k> boot </k>
      <program> $PGM:Pgm </program>
      <input> $INPUT:IntSeq </input>
      <threshold> $THRESHOLD:Int </threshold>
      <l> unbound </l>
      <t> unbound </t>
      <x> unbound </x>
      <result> noResult </result>
    </bt>

  // Loading the module and invoking its required two-argument entry point.
  rule <k> boot => exec(BODY) ... </k>
       <program>
         Module(FuncDef("below_threshold", Params("l", "t"), BODY))
       </program>
       <input> XS </input>
       <threshold> T </threshold>
       <l> unbound => slot(VList(XS)) </l>
       <t> unbound => slot(VInt(T)) </t>

  // Sequential statement execution.
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => S ~> exec(SS) ... </k>

  // Expression evaluation and environment lookup.
  rule <k> eval(Bool(B)) => VBool(B) ... </k>
  rule <k> eval(Name("l")) => V ... </k>
       <l> slot(V) </l>
  rule <k> eval(Name("t")) => V ... </k>
       <t> slot(V) </t>
  rule <k> eval(Name("x")) => V ... </k>
       <x> slot(V) </x>

  // The comparison shape used by the implementation, evaluated left-to-right.
  rule <k> eval(Compare(E1, CmpOp(">=", E2)))
        => eval(E1) ~> cmpRight(E2) ... </k>
  rule <k> V1:Value ~> cmpRight(E2)
        => eval(E2) ~> cmpValues(V1, ">=") ... </k>
  rule <k> VInt(I2) ~> cmpValues(VInt(I1), ">=")
        => VBool(I1 >=Int I2) ... </k>

  // Conditional statements execute exactly one branch.
  rule <k> If(COND, THEN, ELSE)
        => eval(COND) ~> ifK(THEN, ELSE) ... </k>
  rule <k> VBool(true) ~> ifK(THEN, _ELSE)
        => exec(THEN) ... </k>
  rule <k> VBool(false) ~> ifK(_THEN, ELSE)
        => exec(ELSE) ... </k>

  // For loops consume the iterable from left to right and bind the target.
  rule <k> For(TARGET, ITER, BODY)
        => eval(ITER) ~> forK(TARGET, BODY) ... </k>
  rule <k> VList(XS) ~> forK(TARGET, BODY)
        => loop(TARGET, XS, BODY) ... </k>
  rule <k> loop(_TARGET, nil, _BODY) => .K ... </k>
  rule <k> loop(Name("x"), cons(I, XS), BODY)
        => exec(BODY) ~> loop(Name("x"), XS, BODY) ... </k>
       <x> _ => slot(VInt(I)) </x>

  // Return discards the rest of the current function computation.
  rule <k> Return(E) ~> _REST => eval(E) ~> returnK </k>
  rule <k> VBool(B) ~> returnK => .K </k>
       <result> noResult => result(B) </result>
endmodule
