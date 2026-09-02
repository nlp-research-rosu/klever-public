module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports K-EQUAL-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(Module)]
               | "run" "(" Pgm "," Val "," Val ")" [symbol(runProgram)]
               | "programLoaded" [symbol(programLoaded)]

  syntax Stmts ::= Stmt [symbol(oneStmt)]
                 | Stmt Stmts [symbol(moreStmts)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")" [symbol(Return)]

  syntax Params ::= "Params" "(" String "," String ")" [symbol(Params)]

  syntax Expr ::= "Name" "(" String ")" [symbol(Name)]
                | "Int" "(" Int ")" [symbol(IntExpr)]
                | "UnaryOp" "(" String "," Expr ")" [symbol(UnaryOp)]
                | "BoolOp" "(" String "," Expr "," Expr ")" [symbol(BoolOp)]
                | "Compare" "(" Expr "," CmpOp ")" [symbol(Compare)]
                | "Call" "(" Expr "," Expr ")" [symbol(Call)]
                | "Subscript" "(" Expr "," Slice ")" [symbol(Subscript)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Expr ")" [symbol(Slice)]
  syntax Bound ::= "NoBound" [symbol(NoBound)]

  syntax IntList ::= "nil" [symbol(nilInts)]
                   | "cons" "(" Int "," IntList ")" [symbol(consInts)]

  syntax Val ::= "pyInt" "(" Int ")" [symbol(pyInt)]
               | "pyBool" "(" Bool ")" [symbol(pyBool)]
               | "pyList" "(" IntList ")" [symbol(pyList)]
endmodule

module HUMAN-EVAL-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports K-EQUAL

  configuration <k> $PGM:Pgm </k>

  // The source module is a function value when merely loaded.  A `run`
  // request invokes its sole top-level function with two concrete values.
  rule Module(FuncDef(_F, Params(_X, _Y), Return(_E)))
    => programLoaded

  rule run(
         Module(FuncDef("will_it_fly", Params("q", "w"), Return(E))),
         Q, W)
    => eval(E, env(Q, W))

  syntax Env ::= "env" "(" Val "," Val ")" [symbol(env)]

  syntax Val ::= "eval" "(" Expr "," Env ")" [function, symbol(eval)]
               | "negate" "(" Val ")" [function, symbol(negate)]
               | "reverseVal" "(" Val ")" [function, symbol(reverseVal)]
               | "sumVal" "(" Val ")" [function, symbol(sumVal)]
               | "compare" "(" CmpOp "," Val "," Env ")" [function, symbol(compare)]
               | "boolAnd" "(" Val "," Val ")" [function, symbol(boolAnd)]

  rule eval(Name("q"), env(Q, _W)) => Q
  rule eval(Name("w"), env(_Q, W)) => W
  rule eval(Int(I), _RHO) => pyInt(I)
  rule eval(UnaryOp("-", E), RHO) => negate(eval(E, RHO))
  rule eval(
         Subscript(
           E, Slice(NoBound, NoBound, UnaryOp("-", Int(1)))),
         RHO)
    => reverseVal(eval(E, RHO))
  rule eval(Call(Name("sum"), E), RHO) => sumVal(eval(E, RHO))
  rule eval(Compare(E, OP), RHO) => compare(OP, eval(E, RHO), RHO)
  rule eval(BoolOp("and", A, B), RHO)
    => boolAnd(eval(A, RHO), eval(B, RHO))

  rule negate(pyInt(I)) => pyInt(0 -Int I)
  rule reverseVal(pyList(IS)) => pyList(reverseInts(IS))
  rule sumVal(pyList(IS)) => pyInt(sumInts(IS))
  rule compare(CmpOp("==", E), V, RHO)
    => pyBool(equalVals(V, eval(E, RHO)))
  rule compare(CmpOp("<=", E), pyInt(I), RHO)
    => pyBool(I <=Int getInt(eval(E, RHO)))
  rule boolAnd(pyBool(A), pyBool(B)) => pyBool(A andBool B)

  syntax Int ::= "getInt" "(" Val ")" [function, symbol(getInt)]
               | "sumInts" "(" IntList ")" [function, symbol(sumInts)]
  rule getInt(pyInt(I)) => I
  rule sumInts(nil) => 0
  rule sumInts(cons(I, IS)) => I +Int sumInts(IS)

  syntax IntList ::= "reverseInts" "(" IntList ")" [function, symbol(reverseInts)]
                   | "reverseAcc" "(" IntList "," IntList ")"
                     [function, symbol(reverseAcc)]
  rule reverseInts(IS) => reverseAcc(IS, nil)
  rule reverseAcc(nil, ACC) => ACC
  rule reverseAcc(cons(I, IS), ACC) => reverseAcc(IS, cons(I, ACC))

  syntax Bool ::= "equalVals" "(" Val "," Val ")" [function, symbol(equalVals)]
                | "equalIntLists" "(" IntList "," IntList ")"
                  [function, symbol(equalIntLists)]
  rule equalVals(pyInt(I), pyInt(J)) => I ==Int J
  rule equalVals(pyBool(A), pyBool(B)) => A ==Bool B
  rule equalVals(pyList(IS), pyList(JS)) => equalIntLists(IS, JS)
  rule equalIntLists(nil, nil) => true
  rule equalIntLists(nil, cons(_J, _JS)) => false
  rule equalIntLists(cons(_I, _IS), nil) => false
  rule equalIntLists(cons(I, IS), cons(J, JS))
    => (I ==Int J) andBool equalIntLists(IS, JS)
endmodule
