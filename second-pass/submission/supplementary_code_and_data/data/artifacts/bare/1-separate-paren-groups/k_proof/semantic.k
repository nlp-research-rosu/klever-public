requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Ids ::= List{String, ","}
  syntax Params ::= "Params" "(" Ids ")"

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "ImportFrom" "(" String "," Ids ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Expr" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // The task's source alphabet, represented independently of K's strings.
  // This makes the executable string decoder a small boundary component and
  // lets the proof quantify structurally over arbitrary inputs.
  syntax Char ::= "LP" | "RP" | "SP"
  syntax Chars ::= List{Char, ""}

  syntax Output ::= "out" "(" Chars ")"
  syntax Outputs ::= List{Output, ""}

  syntax PInt ::= "zero" | "succ" "(" PInt ")"

  syntax Value ::= PInt | Bool
                 | "SVal" "(" Chars ")"
                 | "OutList" "(" Outputs ")"
                 | "none"

  syntax Input ::= "Raw" "(" String ")"
                 | "Encoded" "(" Chars ")"

  syntax Function ::= "fun" "(" String "," Stmts ")"

  syntax Chars ::= "#chars" "(" String ")" [function]
  syntax Chars ::= "#concat" "(" Chars "," Chars ")" [function]
  syntax Char ::= "#char" "(" String ")" [function]
  syntax Outputs ::= "#snocOut" "(" Outputs "," Chars ")" [function]
  syntax Value ::= "#inputValue" "(" Input ")" [function]
  syntax Bool ::= "#eqChars" "(" Chars "," Chars ")" [function]
  syntax Bool ::= "#eqChar" "(" Char "," Char ")" [function]

  syntax KItem ::= "#boot" "(" Program ")"
                 | "#load" "(" Stmts ")"
                 | "#invoke" "(" String ")"
                 | "#exec" "(" Stmts ")"
                 | "#assign" "(" String ")"
                 | "#augAssign" "(" String "," String ")"
                 | "#cmpLeft" "(" String "," Expr ")"
                 | "#cmpRight" "(" String "," Value ")"
                 | "#if" "(" Stmts "," Stmts ")"
                 | "#for" "(" String "," Stmts ")"
                 | "#loop" "(" String "," Chars "," Stmts ")"
                 | "#set" "(" String "," Value ")"
                 | "#append" "(" String ")"
                 | "#discard"
                 | "#return"

endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  configuration
    <mpy>
      <k> #boot($PGM:Program) </k>
      <input> $INPUT:Input </input>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> none </result>
    </mpy>

  rule #chars(S) => .Chars
    requires lengthString(S) ==Int 0
  rule #chars(S) => #char(substrString(S, 0, 1)) #chars(substrString(S, 1, lengthString(S)))
    requires lengthString(S) >Int 0

  rule #char("(") => LP
  rule #char(")") => RP
  rule #char(" ") => SP

  rule #concat(.Chars, CS) => CS
  rule #concat(C CS1, CS2) => C #concat(CS1, CS2)

  rule #snocOut(.Outputs, CS) => out(CS)
  rule #snocOut(out(OLD) OS, CS) => out(OLD) #snocOut(OS, CS)

  rule #inputValue(Raw(S)) => SVal(#chars(S))
  rule #inputValue(Encoded(CS)) => SVal(CS)

  rule #eqChars(.Chars, .Chars) => true
  rule #eqChars(.Chars, _C _CS) => false
  rule #eqChars(_C _CS, .Chars) => false
  rule #eqChars(C1 CS1, C2 CS2) => #eqChar(C1, C2) andBool #eqChars(CS1, CS2)

  rule #eqChar(LP, LP) => true
  rule #eqChar(RP, RP) => true
  rule #eqChar(SP, SP) => true
  rule #eqChar(LP, RP) => false
  rule #eqChar(LP, SP) => false
  rule #eqChar(RP, LP) => false
  rule #eqChar(RP, SP) => false
  rule #eqChar(SP, LP) => false
  rule #eqChar(SP, RP) => false

  rule <k> #boot(Module(SS)) => #load(SS) ... </k>

  rule <k> #load(.Stmts) => #invoke("separate_paren_groups") ... </k>
  rule <k> #load(ImportFrom(_, _) SS) => #load(SS) ... </k>
  rule <k> #load(FuncDef(F, Params(P), BODY) SS) => #load(SS) ... </k>
       <functions> FS => FS [ F <- fun(P, BODY) ] </functions>

  rule <k> #invoke(F) => #exec(BODY) ... </k>
       <input> IN </input>
       <functions> ... F |-> fun(P, BODY) ... </functions>
       <env> _ => P |-> #inputValue(IN) </env>

  rule <k> #exec(.Stmts) => .K ... </k>
  rule <k> #exec(S SS) => S ~> #exec(SS) ... </k>

  rule <k> Assign(Name(X), E) => E ~> #assign(X) ... </k>
  rule <k> V:Value ~> #assign(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> AugAssign(Name(X), OP, E) => E ~> #augAssign(X, OP) ... </k>
  rule <k> SVal(CS2) ~> #augAssign(X, "+") => .K ... </k>
       <env> ... X |-> (SVal(CS1) => SVal(#concat(CS1, CS2))) ... </env>
  rule <k> succ(zero) ~> #augAssign(X, "+") => .K ... </k>
       <env> ... X |-> (N:PInt => succ(N)) ... </env>
  rule <k> succ(zero) ~> #augAssign(X, "-") => .K ... </k>
       <env> ... X |-> (zero => zero) ... </env>
  rule <k> succ(zero) ~> #augAssign(X, "-") => .K ... </k>
       <env> ... X |-> (succ(N) => N) ... </env>

  rule <k> If(E, THEN, ELSE) => E ~> #if(THEN, ELSE) ... </k>
  rule <k> true ~> #if(THEN, _) => #exec(THEN) ... </k>
  rule <k> false ~> #if(_, ELSE) => #exec(ELSE) ... </k>

  rule <k> For(Name(X), E, BODY) => E ~> #for(X, BODY) ... </k>
  rule <k> SVal(CS) ~> #for(X, BODY) => #loop(X, CS, BODY) ... </k>
  rule <k> #loop(_, .Chars, _) => .K ... </k>
  rule <k> #loop(X, C CS, BODY) => #set(X, SVal(C)) ~> #exec(BODY) ~> #loop(X, CS, BODY) ... </k>

  rule <k> #set(X, V) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> Return(E) => E ~> #return ... </k>
  rule <k> V:Value ~> #return ~> _ => .K </k>
       <result> _ => V </result>

  rule <k> Expr(E) => E ~> #discard ... </k>
  rule <k> _V:Value ~> #discard => .K ... </k>

  rule <k> Call(Attribute(Name(X), "append"), E) => E ~> #append(X) ... </k>
  rule <k> SVal(CS) ~> #append(X) => none ... </k>
       <env> ... X |-> (OutList(OS) => OutList(#snocOut(OS, CS))) ... </env>

  rule <k> Compare(E1, CmpOp(OP, E2)) => E1 ~> #cmpLeft(OP, E2) ... </k>
  rule <k> V:Value ~> #cmpLeft(OP, E2) => E2 ~> #cmpRight(OP, V) ... </k>
  rule <k> zero ~> #cmpRight("==", zero) => true ... </k>
  rule <k> zero ~> #cmpRight("==", succ(_)) => false ... </k>
  // Character/literal comparisons used by this translated program.  Keeping
  // these constructor-disjoint also lets symbolic execution split cleanly on
  // the finite Char datatype.
  rule <k> SVal(SP) ~> #cmpRight("!=", SVal(SP)) => false ... </k>
  rule <k> SVal(SP) ~> #cmpRight("!=", SVal(LP)) => true ... </k>
  rule <k> SVal(SP) ~> #cmpRight("!=", SVal(RP)) => true ... </k>
  rule <k> SVal(LP) ~> #cmpRight("==", SVal(LP)) => true ... </k>
  rule <k> SVal(LP) ~> #cmpRight("==", SVal(RP)) => false ... </k>
  rule <k> SVal(LP) ~> #cmpRight("==", SVal(SP)) => false ... </k>

  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>
  rule <k> Str(S) => SVal(#chars(S)) ... </k>
  rule <k> Int(0) => zero ... </k>
  rule <k> Int(1) => succ(zero) ... </k>
  rule <k> ListExpr() => OutList(.Outputs) ... </k>

endmodule
