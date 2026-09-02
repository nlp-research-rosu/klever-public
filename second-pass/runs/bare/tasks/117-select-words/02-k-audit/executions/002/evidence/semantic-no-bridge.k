// A small, executable semantics for the py2mpy constructors used by
// solution.py.  The source term is kept as a genuine AST: py2mpy does not
// perform any of the semantic work below.

module MPY-SYNTAX
  imports DOMAINS-SYNTAX

  syntax Module
  syntax Stmt
  syntax Stmts    ::= List{Stmt, ""}
  syntax Expr
  syntax Exprs    ::= List{Expr, ","}
  syntax Strings  ::= List{String, ","}
  syntax CmpOp
  syntax CmpOps   ::= List{CmpOp, ","}
  syntax CompFor
  syntax CompFors ::= List{CompFor, ""}

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmt ::= "FuncDef" "(" String ","
                              "Params" "(" Strings ")" ","
                              Stmts ")"
                | "FuncDef" "(" String ","
                              "Params" "(" Strings ")" ","
                              "CellVars" "(" Strings ")" ","
                              "FreeVars" "(" Strings ")" ","
                              Stmts ")"
                | "Return" "(" Expr ")"
                | "Expr" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "ListComp" "(" Expr "," CompFors ")"
                | "Compare" "(" Expr "," CmpOps ")"

  syntax CmpOp   ::= "CmpOp" "(" String "," Expr ")"
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  // Words is both the internal sequence used by split/filter and the payload
  // of the observable Python-list value.  WCons preserves source order.
  syntax Words ::= ".Words"
                 | "WCons" "(" String "," Words ")"
  syntax PyValue ::= "pyList" "(" Words ")"
  syntax Result ::= "noResult" | PyValue

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr "," String "," Int ")"
                 | "finish"

  syntax Words ::= words(String)                       [function]
                 | scanWords(String, String, Words)   [function]
                 | appendWord(Words, String)          [function]
                 | filterWords(Words, Int)            [function]
  syntax Int ::= countConsonants(String)              [function]

  configuration
    <select-words>
      <k> $PGM:Module </k>
      <inputS> $S:String </inputS>
      <inputN> $N:Int </inputN>
      <result> noResult </result>
    </select-words>

  // Loading the translated module selects its required entry point.  Both
  // ordinary and closure-annotated FuncDef forms have a meaning.
  rule <k> Module(FuncDef("select_words", Params("s", "n"), BODY))
        => exec(BODY) ... </k>
  rule <k> Module(FuncDef("select_words", Params("s", "n"),
                          CellVars(_), FreeVars(_), BODY))
        => exec(BODY) ... </k>

  // A leading string expression is a Python docstring and has no value effect.
  rule <k> exec(Expr(Str(_)) REST) => exec(REST) ... </k>

  rule <k> exec(Return(E))
        => eval(E, S, N) ~> finish ... </k>
       <inputS> S </inputS>
       <inputN> N </inputN>

  rule <k> V:PyValue ~> finish => .K ... </k>
       <result> _ => V </result>

  // Denotation of this nested-comprehension shape:
  //
  // [word for word in s.split()
  //       if len([letter for letter in word
  //                    if letter.lower() not in "aeiou"]) == n]
  //
  // The rule is symbolic in S and N.  Its right side is an executable fold,
  // rather than a table of examples or a call out to Python.

  // Python str.split() with no argument, under the prompt's stated alphabet
  // (letters and spaces): discard empty fields from any run of spaces.
  rule words(S) => scanWords(S, "", .Words)

  rule scanWords("", "", WS) => WS
  rule scanWords("", CUR, WS) => appendWord(WS, CUR)
    requires CUR =/=String ""

  rule scanWords(S, CUR, WS)
       => scanWords(
            substrString(S, 1, lengthString(S)),
            "",
            WS)
    requires S =/=String ""
     andBool substrString(S, 0, 1) ==String " "
     andBool CUR ==String ""

  rule scanWords(S, CUR, WS)
       => scanWords(
            substrString(S, 1, lengthString(S)),
            "",
            appendWord(WS, CUR))
    requires S =/=String ""
     andBool substrString(S, 0, 1) ==String " "
     andBool CUR =/=String ""

  rule scanWords(S, CUR, WS)
       => scanWords(
            substrString(S, 1, lengthString(S)),
            CUR +String substrString(S, 0, 1),
            WS)
    requires S =/=String ""
     andBool substrString(S, 0, 1) =/=String " "

  rule appendWord(.Words, W) => WCons(W, .Words)
  rule appendWord(WCons(W, WS), NEW)
       => WCons(W, appendWord(WS, NEW))

  // For letters, testing against both cases of the five vowels is equivalent
  // to solution.py's lower() followed by membership in "aeiou".
  rule countConsonants("") => 0
  rule countConsonants(S)
       => countConsonants(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
     andBool findString(
               "aeiouAEIOU", substrString(S, 0, 1), 0) >=Int 0
  rule countConsonants(S)
       => 1 +Int countConsonants(
                     substrString(S, 1, lengthString(S)))
    requires S =/=String ""
     andBool findString(
               "aeiouAEIOU", substrString(S, 0, 1), 0) ==Int -1

  rule filterWords(.Words, _) => .Words
  rule filterWords(WCons(W, WS), N)
       => WCons(W, filterWords(WS, N))
    requires countConsonants(W) ==Int N
  rule filterWords(WCons(W, WS), N)
       => filterWords(WS, N)
    requires countConsonants(W) =/=Int N
endmodule
