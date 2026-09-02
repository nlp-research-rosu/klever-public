requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // A finite Python string represented as a list of Unicode code points.
  syntax PString ::= "eps"
                   | "ch" "(" Int "," PString ")"

  syntax PValue ::= "pyInt" "(" Int ")"
                  | "pyBool" "(" Bool ")"
                  | "pyStr" "(" PString ")"
                  | "pyTest" "(" Test ")"

  syntax Test ::= "yes" | "no"
                | "#short3" "(" PString ")"
                | "#same" "(" Int "," Int ")"

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Bool" "(" Bool ")"
                | "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Slice" "(" Bound "," Bound "," Bound ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= "NoBound" | Expr
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  configuration
    <k> #call($PGM:Program, "is_happy", pyStr($INPUT:PString)) </k>

  // Mathematical operations on the concrete inductive representation of
  // Python strings.  Code points are compared as Python characters are.
  syntax Int ::= #len ( PString ) [function, total]
  rule #len(eps) => 0
  rule #len(ch(_, S)) => 1 +Int #len(S)

  syntax Int ::= #at ( PString , Int ) [function]
  rule #at(ch(C, _), 0) => C
  rule #at(ch(_, S), I) => #at(S, I -Int 1) requires I >Int 0

  syntax PString ::= #drop ( PString , Int ) [function]
  rule #drop(S, 0) => S
  rule #drop(ch(_, S), I) => #drop(S, I -Int 1) requires I >Int 0

  // This non-functional predicate gives symbolic execution an explicit,
  // exhaustive constructor split for the only length test in solution.mpy.
  rule #short3(eps) => yes
  rule #short3(ch(_, eps)) => yes
  rule #short3(ch(_, ch(_, eps))) => yes
  rule #short3(ch(_, ch(_, ch(_, _)))) => no

  rule #same(I, I) => yes
  rule #same(I, J) => no requires I =/=Int J

  syntax Int ::= #asInt ( PValue ) [function]
  syntax Bool ::= #asBool ( PValue ) [function]
  syntax PString ::= #asStr ( PValue ) [function]
  syntax Test ::= #asTest ( PValue ) [function]
  rule #asInt(pyInt(I)) => I
  rule #asBool(pyBool(B)) => B
  rule #asStr(pyStr(S)) => S
  rule #asTest(pyTest(T)) => T

  syntax Bool ::= #valueEq ( PValue , PValue ) [function]
  rule #valueEq(pyInt(I), pyInt(J)) => I ==Int J

  // Function lookup retains the whole module so recursive calls use the same
  // definitions.  This semantics deliberately implements only the AST nodes
  // exercised by solution.mpy; unsupported constructs cannot silently run.
  syntax PValue ::= #call ( Program , String , PValue ) [function]
  syntax PValue ::= #findCall ( Stmts , Program , String , PValue ) [function]
  rule #call(Module(DEFS), F, V) => #findCall(DEFS, Module(DEFS), F, V)
  rule #findCall(FuncDef(F, Params(P), BODY) _REST, PGM, F, V)
    => #exec(BODY, P, V, PGM)
  rule #findCall(FuncDef(G, Params(_), _) REST, PGM, F, V)
    => #findCall(REST, PGM, F, V)
    requires F =/=String G

  syntax PValue ::= #exec ( Stmts , String , PValue , Program ) [function]
  syntax PValue ::= #choose ( Test , Stmts , Stmts , Stmts , String , PValue , Program )
  syntax PValue ::= #branch ( Stmts , Stmts , String , PValue , Program ) [function]

  rule #exec(Return(E) _, P, V, PGM) => #eval(E, P, V, PGM)
  rule #exec(If(COND, YES, NO) REST, P, V, PGM)
    => #choose(#asTest(#eval(COND, P, V, PGM)), YES, NO, REST, P, V, PGM)

  rule #choose(yes, YES, _, REST, P, V, PGM)
    => #branch(YES, REST, P, V, PGM)
  rule #choose(no, _, NO, REST, P, V, PGM)
    => #branch(NO, REST, P, V, PGM)

  // Direct contextual rules expose constructor/equality case splits to the
  // symbolic backend without relying on an evaluation-order extension.
  rule #choose(#short3(eps), YES, _, REST, P, V, PGM)
    => #branch(YES, REST, P, V, PGM)
  rule #choose(#short3(ch(_, eps)), YES, _, REST, P, V, PGM)
    => #branch(YES, REST, P, V, PGM)
  rule #choose(#short3(ch(_, ch(_, eps))), YES, _, REST, P, V, PGM)
    => #branch(YES, REST, P, V, PGM)
  rule #choose(#short3(ch(_, ch(_, ch(_, _)))), _, NO, REST, P, V, PGM)
    => #branch(NO, REST, P, V, PGM)
  rule #choose(#same(I, I), YES, _, REST, P, V, PGM)
    => #branch(YES, REST, P, V, PGM)
  rule #choose(#same(I, J), _, NO, REST, P, V, PGM)
    => #branch(NO, REST, P, V, PGM)
    requires I =/=Int J

  rule #branch(.Stmts, REST, P, V, PGM) => #exec(REST, P, V, PGM)
  rule #branch(Return(E) _, _, P, V, PGM) => #eval(E, P, V, PGM)
  rule #branch(If(COND, YES, NO) MORE, REST, P, V, PGM)
    => #choose(#asTest(#eval(COND, P, V, PGM)), YES, NO,
               #append(MORE, REST), P, V, PGM)

  syntax Stmts ::= #append ( Stmts , Stmts ) [function, total]
  rule #append(.Stmts, REST) => REST
  rule #append(S MORE, REST) => S #append(MORE, REST)

  syntax PValue ::= #eval ( Expr , String , PValue , Program ) [function]
  rule #eval(Bool(B), _, _, _) => pyBool(B)
  rule #eval(Int(I), _, _, _) => pyInt(I)
  rule #eval(Name(P), P, V, _) => V

  rule #eval(Call(Name("len"), E), P, V, PGM)
    => pyInt(#len(#asStr(#eval(E, P, V, PGM))))
  rule #eval(Call(Name(F), E), P, V, PGM)
    => #call(PGM, F, #eval(E, P, V, PGM))
    requires F =/=String "len"

  rule #eval(Compare(Call(Name("len"), E), CmpOp("<", Int(3))), P, V, PGM)
    => pyTest(#short3(#asStr(#eval(E, P, V, PGM))))
  rule #eval(Compare(L, CmpOp("==", R)), P, V, PGM)
    => pyTest(#same(#asInt(#eval(L, P, V, PGM)),
                    #asInt(#eval(R, P, V, PGM))))

  rule #eval(Subscript(E, Int(I)), P, V, PGM)
    => pyInt(#at(#asStr(#eval(E, P, V, PGM)), I))
  rule #eval(Subscript(E, Slice(Int(I), NoBound, NoBound)), P, V, PGM)
    => pyStr(#drop(#asStr(#eval(E, P, V, PGM)), I))
endmodule
