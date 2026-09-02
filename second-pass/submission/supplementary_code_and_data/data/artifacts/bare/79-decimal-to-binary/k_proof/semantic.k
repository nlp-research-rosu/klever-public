requires "domains.md"

module SEMANTIC-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmt ")" [symbol(moduleProgram)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                [symbol(functionDefinition)]
                | "Return" "(" Expr ")" [symbol(returnStatement)]

  syntax Params ::= "Params" "(" String ")" [symbol(parameters)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(integerExpression)]
                | "Str" "(" String ")" [symbol(stringExpression)]
                | "Name" "(" String ")" [symbol(nameExpression)]
                | "BinOp" "(" String "," Expr "," Expr ")"
                  [symbol(binaryExpression)]
                | "Call" "(" Expr "," Expr ")" [symbol(callExpression)]
                | "Subscript" "(" Expr "," Slice ")"
                  [symbol(subscriptExpression)]

  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
                   [symbol(sliceExpression)]
  syntax Bound ::= Expr | "NoBound" [symbol(noBound)]
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax Env ::= "bind" "(" String "," Int ")" [symbol(bind)]

  syntax Val ::= "intVal" "(" Int ")" [symbol(intVal)]
               | "strVal" "(" String ")" [symbol(strVal)]
               | "binVal" "(" String ")" [symbol(binVal)]
               | "negativeBinVal" "(" String ")" [symbol(negativeBinVal)]

  syntax Val ::= eval(Expr, Env) [function]
               | addValues(Val, Val) [function]
               | callBin(Val) [function]
               | suffixFrom(Val, Int) [function]

  syntax String ::= binDigits(Int) [function]

  configuration
    <python>
      <k> $PGM:Program </k>
      <arg> $ARG:Int </arg>
      <result> .K </result>
    </python>

  rule <k>
         Module(
           FuncDef("decimal_to_binary", Params("decimal"), Return(E))
         )
       => .K
       </k>
       <arg> I </arg>
       <result> .K => eval(E, bind("decimal", I)) </result>

  rule eval(Int(I), _) => intVal(I)
  rule eval(Str(S), _) => strVal(S)
  rule eval(Name(X), bind(X, I)) => intVal(I)
  rule eval(BinOp("+", LEFT, RIGHT), RHO)
    => addValues(eval(LEFT, RHO), eval(RIGHT, RHO))
  rule eval(Call(Name("bin"), ARG), RHO) => callBin(eval(ARG, RHO))
  rule eval(Subscript(BASE, Slice(Int(START), NoBound, NoBound)), RHO)
    => suffixFrom(eval(BASE, RHO), START)

  rule addValues(intVal(I), intVal(J)) => intVal(I +Int J)
  rule addValues(strVal(S), strVal(T)) => strVal(S +String T)

  // binVal(S) is the internal value denoting Python's string "0b" + S.
  rule callBin(intVal(I)) => binVal(binDigits(I))
    requires I >=Int 0
  // Python renders a negative input as "-0b" + digits.
  rule callBin(intVal(I)) => negativeBinVal(binDigits(0 -Int I))
    requires I <Int 0

  rule suffixFrom(binVal(S), 2) => strVal(S)
  rule suffixFrom(negativeBinVal(S), 2) => strVal("b" +String S)

  rule binDigits(I) => Int2String(I)
    requires (0 <=Int I) andBool (I <Int 2)
  rule binDigits(I) => binDigits(I /Int 2) +String Int2String(I %Int 2)
    requires I >=Int 2
endmodule
