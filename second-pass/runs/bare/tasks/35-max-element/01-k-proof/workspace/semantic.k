requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar consumed by py2mpy.py for this program.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax Exprs ::= List{Expr, ","}

  // A deliberately inductive, non-empty input domain.  The HumanEval
  // contract has no result for an empty list, so empty lists are not inputs.
  syntax IntSeq ::= "[" NonEmptyInts "]"
  syntax NonEmptyInts ::= Int
                        | Int "," NonEmptyInts
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports MAP

  syntax Function ::= "closure" "(" Params "," Stmts ")"
  syntax Result ::= "noResult" | "result" "(" Int ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "invoke" "(" String "," IntSeq ")"
                 | "eval" "(" Expr ")"
                 | "intVal" "(" Int ")"
                 | "doReturn"

  // Mathematical meaning of Python's max on a non-empty integer list.
  syntax Int ::= maxInts(IntSeq) [function, total]
  syntax Int ::= imax(Int, Int) [function, total]

  rule maxInts([ I:Int ]) => I
  rule maxInts([ I:Int, IS:NonEmptyInts ]) => imax(I, maxInts([ IS ]))

  rule imax(I, J) => I requires I >=Int J
  rule imax(I, J) => J requires I <Int J

  configuration
    <mpy>
      <k> $PGM:Program ~> invoke("max_element", $ARGS:IntSeq) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Module and statement-list execution.
  rule <k> Module(SS) => exec(SS) ... </k>
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt REST:Stmts) => S ~> exec(REST) ... </k>

  // Function definitions are closures.  This task has no free variables, so
  // the function body and its parameter list are the entire closure value.
  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FUNS => FUNS [ F <- closure(PS, BODY) ] </functions>

  // The requested entry point has one argument.  A fresh function environment
  // is installed when it is invoked.
  rule <k> invoke(F, ARG) => exec(BODY) ... </k>
       <functions>
         ... F |-> closure(Params(P:String, .Strings), BODY) ...
       </functions>
       <env> _ => P |-> ARG </env>

  rule <k> Return(E) => eval(E) ~> doReturn ... </k>

  // Expression evaluation needed by solution.mpy.  Name lookup is modeled
  // separately from the max call so the environment is explicit in the state.
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k>
         eval(Call(Name("max"), Name(X), .Exprs))
         => intVal(maxInts(IS))
       ... </k>
       <env> ... X |-> IS:IntSeq ... </env>

  rule <k> intVal(I) ~> doReturn => .K ... </k>
       <result> noResult => result(I) </result>
endmodule
