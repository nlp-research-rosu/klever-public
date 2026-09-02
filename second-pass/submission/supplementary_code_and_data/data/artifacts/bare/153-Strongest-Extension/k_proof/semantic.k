// A small executable semantics for the py2mpy constructors used by solution.py.
// It models Python integers, strings, lists, local variables, sequencing,
// conditionals, for-loops, method calls to str.isupper/islower, and return.

requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Program ::= Module ( Stmts )

  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= Params ( String , String )
  syntax Exprs ::= List{Expr,","}
  syntax CmpOps ::= List{CmpOp,","}

  syntax Stmt ::= FuncDef ( String , Params , Stmts )
                | Assign ( Expr , Expr ) [strict(2)]
                | AugAssign ( Expr , String , Expr ) [strict(3)]
                | If ( Expr , Stmts , Stmts ) [strict(1)]
                | For ( Expr , Expr , Stmts ) [strict(2)]
                | Return ( Expr ) [strict]

  syntax Expr ::= Int ( Int )
                | Str ( String )
                | Name ( String )
                | BinOp ( String , Expr , Expr ) [strict(2,3)]
                | Compare ( Expr , CmpOps ) [strict(1)]
                | Subscript ( Expr , Expr ) [strict(1)]
                | Slice ( Bound , Bound , Bound )
                | Attribute ( Expr , String ) [strict(1)]
                | Call ( Expr , Exprs ) [strict(1)]

  syntax CmpOp ::= CmpOp ( String , Expr )
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  // Runtime values.  A semicolon deliberately separates Values so this list
  // syntax cannot be confused with constructor argument commas.
  syntax Value ::= "intVal" "(" Int ")"
                 | "strVal" "(" String ")"
                 | "listVal" "(" Values ")"
                 | "boolVal" "(" Bool ")"
                 | "boundStringMethod" "(" String "," String ")"
  syntax Values ::= List{Value,";"}
  syntax KResult ::= Value
  syntax Expr ::= Value

  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax Result ::= "noResult" | "returned" "(" Value ")"

  configuration
    <py>
      <k> $PGM:Program ~> #start </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <inputClass> $CLASS:String </inputClass>
      <inputExtensions> $EXTENSIONS:Values </inputExtensions>
      <result> noResult </result>
    </py>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "setVar" "(" String "," Value ")"
                 | "loopValues" "(" String "," Values "," Stmts ")"
                 | "loopString" "(" String "," String "," Int "," Stmts ")"
                 | "#start"

  // Module loading and ordinary statement sequencing.
  rule <k> Module(S) => exec(S) ... </k>
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => S ~> exec(SS) ... </k>

  rule <k> FuncDef(F, P, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  // This task's required entry point is called after the translated module
  // has installed its definition.  Parameters are bound by their source names.
  rule <k> #start => exec(BODY) ... </k>
       <functions> ... "Strongest_Extension" |-> function(Params("class_name", "extensions"), BODY) ... </functions>
       <inputClass> C </inputClass>
       <inputExtensions> ES </inputExtensions>
       <env> _ => "class_name" |-> strVal(C)
                  "extensions" |-> listVal(ES) </env>

  // Literals, lookup, and assignment.
  rule Int(I) => intVal(I)
  rule Str(S) => strVal(S)
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V:Value ... </env>

  rule <k> Assign(Name(X), V:Value) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>
  rule <k> setVar(X, V) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> AugAssign(Name(X), "+", intVal(I)) => .K ... </k>
       <env> X |-> intVal(J) ENV => X |-> intVal(J +Int I) ENV </env>
  rule <k> AugAssign(Name(X), "-", intVal(I)) => .K ... </k>
       <env> X |-> intVal(J) ENV => X |-> intVal(J -Int I) ENV </env>

  // The two subscript forms emitted by this solution: [0] and [1:].
  rule Subscript(listVal(V ; _), Int(0)) => V
  rule Subscript(listVal(_ ; VS), Slice(Int(1), NoBound, NoBound))
    => listVal(VS)

  // List and string iteration.  The string loop exposes one Unicode code
  // point at a time through K's String hooks.
  rule <k> For(Name(X), listVal(VS), BODY) => loopValues(X, VS, BODY) ... </k>
  rule <k> loopValues(_, .Values, _) => .K ... </k>
  rule <k> loopValues(X, V ; VS, BODY)
        => setVar(X, V) ~> exec(BODY) ~> loopValues(X, VS, BODY) ... </k>

  rule <k> For(Name(X), strVal(S), BODY) => loopString(X, S, 0, BODY) ... </k>
  rule <k> loopString(_, S, I, _) => .K ... </k>
       requires I >=Int lengthString(S)
  rule <k> loopString(X, S, I, BODY)
        => setVar(X, strVal(substrString(S, I, I +Int 1)))
           ~> exec(BODY) ~> loopString(X, S, I +Int 1, BODY) ... </k>
       requires I <Int lengthString(S)

  // String methods needed by the program.  For one-character strings,
  // CPython's ASCII upper/lower cases coincide with these code-point ranges.
  syntax Bool ::= "isUpperChar" "(" String ")" [function, total]
                | "isLowerChar" "(" String ")" [function, total]
  rule isUpperChar(S) => (65 <=Int ordChar(S)) andBool (ordChar(S) <=Int 90)
  rule isLowerChar(S) => (97 <=Int ordChar(S)) andBool (ordChar(S) <=Int 122)

  rule Attribute(strVal(S), METHOD) => boundStringMethod(S, METHOD)
  rule Call(boundStringMethod(S, "isupper"), .Exprs)
    => boolVal(isUpperChar(S))
  rule Call(boundStringMethod(S, "islower"), .Exprs)
    => boolVal(isLowerChar(S))

  rule If(boolVal(true), THEN, _) => exec(THEN)
  rule If(boolVal(false), _, ELSE) => exec(ELSE)

  rule BinOp("+", intVal(I), intVal(J)) => intVal(I +Int J)
  rule BinOp("+", strVal(S), strVal(T)) => strVal(S +String T)
  rule <k> Compare(intVal(I), CmpOp(">", Name(X))) => boolVal(I >Int J) ... </k>
       <env> ... X |-> intVal(J) ... </env>

  rule <k> Return(V:Value) => .K ... </k>
       <result> noResult => returned(V) </result>
endmodule

module SEMANTIC
  imports MPY-SEMANTIC
endmodule
