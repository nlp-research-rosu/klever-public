module MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP
  imports LIST

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" String ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"                         [strict]
                | "If" "(" Expr "," Stmts "," Stmts ")"      [strict(1)]

  syntax Expr ::= "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | PyVal
                | "BinOp" "(" String "," Expr "," Expr ")"   [strict(2,3)]
                | "BoolOp" "(" String "," Expr "," Expr ")"  [strict(2)]
                | "Compare" "(" Expr "," CmpOp ")"            [strict(1)]
                | "Subscript" "(" Expr "," Expr ")"           [strict]
                | "Subscript" "(" Expr "," Slice ")"          [strict(1)]
                | "Call" "(" Expr "," Expr ")"                [strict(2)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"

  syntax PyVal ::= "intVal" "(" Int ")"
                 | "strVal" "(" String ")"
                 | "boolVal" "(" Bool ")"
  syntax KResult ::= PyVal
endmodule

module SOLUTION
  imports MPY-SYNTAX

  // These macros are a readable name for the exact tree in solution.mpy.
  syntax Stmts ::= "vowelBody" [macro]
  rule vowelBody =>
    If(Compare(Name("s"), CmpOp("==", Str(""))),
       Return(Int(0)),
       .Stmts)
    If(Compare(Subscript(Name("s"), Int(0)),
               CmpOp("in", Str("aeiouAEIOU"))),
       Return(BinOp("+", Int(1),
                    Call(Name("vowels_count"),
                         Subscript(Name("s"),
                                   Slice(Int(1), NoBound, NoBound))))),
       .Stmts)
    If(BoolOp("and",
              Compare(Call(Name("len"), Name("s")),
                      CmpOp("==", Int(1))),
              Compare(Subscript(Name("s"), Int(0)),
                      CmpOp("in", Str("yY")))),
       Return(Int(1)),
       .Stmts)
    Return(Call(Name("vowels_count"),
                Subscript(Name("s"), Slice(Int(1), NoBound, NoBound))))

  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(FuncDef("vowels_count", Params("s"), vowelBody))
endmodule

module SEMANTIC
  imports SOLUTION

  syntax Function ::= "function" "(" String "," Stmts ")"
  syntax Expr ::= "#compare" "(" String "," PyVal "," Expr ")" [strict(3)]
  syntax Bool ::= "#isVowelChar" "(" String ")" [function, total]
                | "#isYChar" "(" String ")"     [function, total]
  syntax KItem ::= "#entry" "(" String ")"
                 | "#return" "(" PyVal ")"
                 | "#endCall"

  configuration
    <py>
      <k> $PGM:Program ~> #entry($INPUT:String) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <stack> .List </stack>
    </py>

  // Modules load their definitions before the configured entry call runs.
  rule <k> Module(SS) => SS ... </k>
  rule <k> S:Stmt SS:Stmts => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>
  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>
  rule <k> #entry(S) => Call(Name("vowels_count"), strVal(S)) ... </k>

  // Literal and variable evaluation.
  rule Int(I) => intVal(I)
  rule Str(S) => strVal(S)
  rule <k> Name(X) => V ... </k>
       <env>... X |-> V:PyVal ...</env>

  // Function calls replace the local environment and save the caller's one.
  rule <k> Call(Name("len"), strVal(S)) => intVal(lengthString(S)) ... </k>
  rule <k> Call(Name(F), V:PyVal) => BODY ~> #endCall ... </k>
       <env> ENV => P |-> V </env>
       <functions>... F |-> function(P, BODY) ...</functions>
       <stack> STACK => ListItem(ENV) STACK </stack>

  // A return discards the rest of the current body, restores the caller, and
  // leaves its value for the heating/cooling continuation of the call site.
  rule Return(V:PyVal) => #return(V)
  rule <k> #return(V) ~> _S:Stmt => #return(V) ... </k>
  rule <k> #return(V) ~> _SS:Stmts => #return(V) ... </k>
  rule <k> #return(V) ~> #endCall => V ... </k>
       <env> _ => ENV </env>
       <stack> ListItem(ENV) REST => REST </stack>

  // Control flow is path-sensitive, which lets the prover split a symbolic
  // total Boolean while concrete krun executions remain deterministic.
  rule <k> (If(boolVal(B), THEN, _ELSE):Stmt) => THEN ... </k>
       requires B
  rule <k> (If(boolVal(B), _THEN, ELSE):Stmt) => ELSE ... </k>
       requires notBool B
  rule BoolOp("and", boolVal(B), RHS) => RHS requires B
  rule BoolOp("and", boolVal(B), _RHS) => boolVal(false) requires notBool B

  // The expression fragment needed by solution.mpy.
  rule BinOp("+", intVal(I), intVal(J)) => intVal(I +Int J)
  rule Compare(V:PyVal, CmpOp(OP, RHS)) => #compare(OP, V, RHS)
  rule #compare("==", strVal(A), strVal(B)) => boolVal(true)
       requires A ==String B
  rule #compare("==", strVal(A), strVal(B)) => boolVal(false)
       requires A =/=String B
  rule #compare("==", intVal(I), intVal(J)) => boolVal(true)
       requires I ==Int J
  rule #compare("==", intVal(I), intVal(J)) => boolVal(false)
       requires I =/=Int J
  rule #compare("in", strVal(C), strVal("aeiouAEIOU")) =>
       boolVal(#isVowelChar(C))
  rule #compare("in", strVal(C), strVal("yY")) => boolVal(#isYChar(C))

  rule #isVowelChar(C) => true requires C ==String "a"
  rule #isVowelChar(C) => true requires C ==String "e"
  rule #isVowelChar(C) => true requires C ==String "i"
  rule #isVowelChar(C) => true requires C ==String "o"
  rule #isVowelChar(C) => true requires C ==String "u"
  rule #isVowelChar(C) => true requires C ==String "A"
  rule #isVowelChar(C) => true requires C ==String "E"
  rule #isVowelChar(C) => true requires C ==String "I"
  rule #isVowelChar(C) => true requires C ==String "O"
  rule #isVowelChar(C) => true requires C ==String "U"
  rule #isVowelChar(C) => false
    requires C =/=String "a" andBool C =/=String "e"
     andBool C =/=String "i" andBool C =/=String "o"
     andBool C =/=String "u" andBool C =/=String "A"
     andBool C =/=String "E" andBool C =/=String "I"
     andBool C =/=String "O" andBool C =/=String "U"

  rule #isYChar(C) => true requires C ==String "y"
  rule #isYChar(C) => true requires C ==String "Y"
  rule #isYChar(C) => false
    requires C =/=String "y" andBool C =/=String "Y"
  rule Subscript(strVal(S), intVal(I)) =>
       strVal(substrString(S, I, I +Int 1))
  rule Subscript(strVal(S), Slice(Int(1), NoBound, NoBound)) =>
       strVal(substrString(S, 1, lengthString(S)))
endmodule
