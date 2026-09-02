requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports FLOAT-SYNTAX
  imports STRING-SYNTAX

  // The portion of the py2mpy constructor language used by solution.mpy.
  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::=
      "FuncDef" "(" String "," Params "," Stmts ")"
    | "Assign" "(" Expr "," Expr ")"
    | "For" "(" Expr "," Expr "," Stmts ")"
    | "If" "(" Expr "," Stmts "," Stmts ")"
    | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::=
      "Int" "(" Int ")"
    | "Float" "(" Float ")"
    | "Bool" "(" Bool ")"
    | "Name" "(" String ")"
    | "BinOp" "(" String "," Expr "," Expr ")"
    | "Compare" "(" Expr "," CmpOps ")"
    | "Call" "(" Expr "," Exprs ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Runtime values.  Typed cons constructors make both list structure and
  // Python runtime tags available to symbolic induction.
  syntax Val ::=
      "pyInt" "(" Int ")"
    | "pyFloat" "(" Float ")"
    | "pyBool" "(" Bool ")"
    | "pyList" "(" Vals ")"
  syntax Vals ::=
      "nil"
    | "intCons" "(" Int "," Vals ")"
    | "floatCons" "(" Float "," Vals ")"
    | "boolCons" "(" Bool "," Vals ")"
    | "listCons" "(" Vals "," Vals ")"

  syntax Result ::= "noResult" | Val
  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax FunctionSlot ::= "noFunction" | Function
  syntax ValSlot ::= "noValue" | Val
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports FLOAT
  imports STRING

  configuration
    <py>
      <k> $PGM:Module </k>
      <input> $INPUT:Val </input>
      <lst> noValue </lst>
      <total> pyInt(0) </total>
      <value> pyInt(0) </value>
      <function> noFunction </function>
      <result> noResult </result>
    </py>

  // Internal control items.
  syntax KItem ::= "start"
                 | "bind" "(" String "," Val ")"
                 | "branch" "(" Bool "," Stmts "," Stmts ")"
                 | "loop" "(" String "," Val "," Stmts ")"
                 | "returnValue" "(" Val ")"

  // Pure expression evaluation for the expression forms in solution.py.
  syntax Val ::= eval(Expr, Val, Val, Val) [function]
  syntax Val ::= isIntVal(Val) [function]
               | addVal(Val, Val) [function]
               | mulVal(Val, Val) [function]
               | modVal(Val, Val) [function]
               | geVal(Val, Val) [function]
               | eqVal(Val, Val) [function]
  syntax Int ::= asInt(Val) [function]
  syntax Bool ::= asBool(Val) [function]

  rule eval(Int(I), _, _, _) => pyInt(I)
  rule eval(Float(F), _, _, _) => pyFloat(F)
  rule eval(Bool(B), _, _, _) => pyBool(B)
  rule eval(Name("lst"), L, _, _) => L
  rule eval(Name("total"), _, T, _) => T
  rule eval(Name("value"), _, _, V) => V

  rule eval(BinOp("+", E1, E2), L, T, V)
    => addVal(eval(E1, L, T, V), eval(E2, L, T, V))
  rule eval(BinOp("*", E1, E2), L, T, V)
    => mulVal(eval(E1, L, T, V), eval(E2, L, T, V))
  rule eval(BinOp("%", E1, E2), L, T, V)
    => modVal(eval(E1, L, T, V), eval(E2, L, T, V))

  rule eval(Compare(E1, CmpOp(">=", E2)), L, T, V)
    => geVal(eval(E1, L, T, V), eval(E2, L, T, V))
  rule eval(Compare(E1, CmpOp("==", E2)), L, T, V)
    => eqVal(eval(E1, L, T, V), eval(E2, L, T, V))

  rule eval(Call(Name("isinstance"), E, Name("int")), L, T, V)
    => isIntVal(eval(E, L, T, V))

  // CPython considers bool a subclass of int.
  rule isIntVal(pyInt(_))   => pyBool(true)
  rule isIntVal(pyBool(_))  => pyBool(true)
  rule isIntVal(_)          => pyBool(false) [owise]

  rule asInt(pyInt(I))     => I
  rule asInt(pyBool(true)) => 1
  rule asInt(pyBool(false)) => 0
  rule asBool(pyBool(B)) => B

  rule addVal(V1, V2) => pyInt(asInt(V1) +Int asInt(V2))
  rule mulVal(V1, V2) => pyInt(asInt(V1) *Int asInt(V2))
  rule modVal(V1, V2) => pyInt(asInt(V1) %Int asInt(V2))
  rule geVal(V1, V2)  => pyBool(asInt(V1) >=Int asInt(V2))
  rule eqVal(V1, V2)  => pyBool(asInt(V1) ==Int asInt(V2))

  // Load module-level definitions, then invoke the requested entry point.
  rule <k> Module(SS) => SS ~> start ... </k>

  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> FuncDef("double_the_difference", P, BODY) => .K ... </k>
       <function> noFunction => function(P, BODY) </function>

  rule <k> start => BODY ... </k>
       <input> INPUT </input>
       <lst> noValue => INPUT </lst>
       <function> function(Params("lst"), BODY) </function>

  rule <k> Assign(Name("total"), E) => .K ... </k>
       <lst> L </lst>
       <total> T => eval(E, L, T, V) </total>
       <value> V </value>

  rule <k> If(E, THEN, ELSE)
        => branch(asBool(eval(E, L, T, V)), THEN, ELSE) ... </k>
       <lst> L </lst>
       <total> T </total>
       <value> V </value>

  rule <k> branch(true, THEN, _) => THEN ... </k>
  rule <k> branch(false, _, ELSE) => ELSE ... </k>

  rule <k> For(Name(X), E, BODY)
        => loop(X, eval(E, L, T, V), BODY) ... </k>
       <lst> L </lst>
       <total> T </total>
       <value> V </value>

  rule <k> loop(_, pyList(nil), _) => .K ... </k>
  rule <k> loop(X, pyList(intCons(I, VS)), BODY)
        => bind(X, pyInt(I)) ~> BODY
        ~> loop(X, pyList(VS), BODY) ... </k>
  rule <k> loop(X, pyList(floatCons(F, VS)), BODY)
        => bind(X, pyFloat(F)) ~> BODY
        ~> loop(X, pyList(VS), BODY) ... </k>
  rule <k> loop(X, pyList(boolCons(true, VS)), BODY)
        => bind(X, pyBool(true)) ~> BODY
        ~> loop(X, pyList(VS), BODY) ... </k>
  rule <k> loop(X, pyList(boolCons(false, VS)), BODY)
        => bind(X, pyBool(false)) ~> BODY
        ~> loop(X, pyList(VS), BODY) ... </k>
  rule <k> loop(X, pyList(listCons(ITEMS, VS)), BODY)
        => bind(X, pyList(ITEMS)) ~> BODY
        ~> loop(X, pyList(VS), BODY) ... </k>

  rule <k> bind("value", V) => .K ... </k>
       <value> _ => V </value>

  rule <k> Return(E) => returnValue(eval(E, L, T, V)) ... </k>
       <lst> L </lst>
       <total> T </total>
       <value> V </value>

  // Returning from the entry point halts and clears its local runtime state.
  rule <k> returnValue(V) ~> _REST => .K </k>
       <lst> _ => noValue </lst>
       <total> _ => pyInt(0) </total>
       <value> _ => pyInt(0) </value>
       <function> _ => noFunction </function>
       <result> noResult => V </result>

  rule <k> returnValue(V) => .K </k>
       <lst> _ => noValue </lst>
       <total> _ => pyInt(0) </total>
       <value> _ => pyInt(0) </value>
       <function> _ => noFunction </function>
       <result> noResult => V </result>
endmodule
