module SEMANTIC-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX
  imports MAP

  syntax Pgm ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," String ")"
                | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String "," String ")"
  syntax CellVars ::= "CellVars" "(" String ")"
  syntax FreeVars ::= "FreeVars" "(" ")"

  syntax Expr ::= "Name" "(" String ")"
                | "ListComp" "(" Expr "," CompFors ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax CompFors ::= List{CompFor, ""}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax PyList ::= "Nil"
                  | "Cons" "(" String "," PyList ")"

  syntax KItem ::= execute(Pgm, String, PyList, String)
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP

  configuration <k> execute($PGM:Pgm,
                             $FUNCTION:String,
                             $INPUT:PyList,
                             $SUBSTRING:String)
                </k>

  syntax Function ::= function(Params, Stmts)
  syntax Function ::= lookupFunction(String, Stmts) [function]

  rule lookupFunction(FUNCTION,
         ImportFrom(_MODULE, _NAMES) REST)
    => lookupFunction(FUNCTION, REST)
  rule lookupFunction(FUNCTION,
         FuncDef(FUNCTION, PARAMS, _CELLS, _FREES, BODY) _REST)
    => function(PARAMS, BODY)
  rule lookupFunction(FUNCTION,
         FuncDef(OTHER, _PARAMS, _CELLS, _FREES, _BODY) REST)
    => lookupFunction(FUNCTION, REST)
    requires FUNCTION =/=String OTHER

  syntax Expr ::= returnExpr(Stmts) [function]
  rule returnExpr(Return(EXPRESSION) _REST) => EXPRESSION

  syntax PyList ::= invoke(Function, PyList, String) [function]
  syntax PyList ::= evalList(Expr, Map) [function]
  syntax SubstringFilter ::= substringFilter(String)
  syntax PyList ::= evalComp(PyList, SubstringFilter) [function, total]
  syntax String ::= evalString(Expr, Map) [function]
  syntax Bool ::= containsString(String, String) [function]

  rule <k> execute(Module(STATEMENTS), FUNCTION, INPUT, SUBSTRING)
        => invoke(lookupFunction(FUNCTION, STATEMENTS), INPUT, SUBSTRING)
       </k>

  rule invoke(function(Params(INPUTNAME, SUBSTRINGNAME), BODY),
              INPUT, SUBSTRING)
    => evalList(returnExpr(BODY),
                (INPUTNAME |-> INPUT) (SUBSTRINGNAME |-> SUBSTRING))

  rule evalList(Name(NAME), (NAME |-> VALUE:PyList) _REST) => VALUE
  rule evalString(Name(NAME), (NAME |-> VALUE:String) _REST) => VALUE

  rule evalList(
         ListComp(Name(TARGET),
           CompFor(Name(TARGET),
                   ITERABLE,
                   Compare(NEEDLE, CmpOp("in", Name(TARGET))))),
         ENV)
    => evalComp(evalList(ITERABLE, ENV),
                substringFilter(evalString(NEEDLE, ENV)))

  rule evalComp(Nil, _FILTER) => Nil
  rule evalComp(Cons(HEAD, TAIL), substringFilter(NEEDLE))
    => Cons(HEAD, evalComp(TAIL, substringFilter(NEEDLE)))
    requires containsString(HEAD, NEEDLE)
  rule evalComp(Cons(HEAD, TAIL), substringFilter(NEEDLE))
    => evalComp(TAIL, substringFilter(NEEDLE))
    requires notBool containsString(HEAD, NEEDLE)

  rule containsString(HAYSTACK, NEEDLE)
    => findString(HAYSTACK, NEEDLE, 0) >=Int 0
endmodule
