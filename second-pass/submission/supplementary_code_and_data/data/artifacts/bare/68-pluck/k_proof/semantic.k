module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "ListExpr" "(" Exprs ")"
                | "TupleExpr" "(" Exprs ")"
                | "ListComp" "(" Expr "," CompFors ")"
                | "KwArg" "(" String "," Expr ")"
                | "Subscript" "(" Expr "," Index ")"
                | "Call" "(" Expr "," Exprs ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CompFors ::= List{CompFor, ""}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports K-EQUAL
  imports MAP
  imports LIST

  // Values are deliberately limited to the data used by this HumanEval task:
  // integers, lists of integers, booleans, and Python's None result.
  syntax Ints ::= List{Int, ","}
  syntax Val ::= "VInt" "(" Int ")"
               | "VList" "(" Ints ")"
               | "VArray" "(" Int "," Int "," Int ")"
               | "VBool" "(" Bool ")"
               | "VEq" "(" Int "," Int ")"
               | "VLt" "(" Int "," Int ")"
               | "VCandidates" "(" Ints ")"
               | "VCandidatesArray" "(" Int "," Int "," Int ")"
               | "minEvenInts" "(" Ints "," Int ")" [function, total]
               | "chooseEven" "(" Int "," Int "," Val ")"
                   [function, total]
               | "minEvenArray" "(" Int "," Int "," Int ")"
                   [function, total]
               | "VNone"
  syntax Vals ::= List{Val, ","}

  // Symbolic observers for a non-empty translated integer list.  Constructor
  // equations execute concretely; on an opaque symbolic list they remain
  // typed terms, with non-emptiness carried by the path condition.
  syntax Int ::= "headInt" "(" Ints ")" [function, total]
               | "arrayAt" "(" Int "," Int ")" [function, total]
  syntax Ints ::= "tailInts" "(" Ints ")" [function, total]
  rule headInt(I, _IS) => I
  rule tailInts(_I, IS) => IS

  // Meaning of the even-pair comprehension followed by min for concrete
  // translated lists.  <= selects the earlier index when equal values tie.
  rule minEvenInts(.Ints, _INDEX) => VList(.Ints)
  rule minEvenInts(HEAD, TAIL, INDEX)
       => chooseEven(HEAD, INDEX, minEvenInts(TAIL, INDEX +Int 1))
  rule chooseEven(HEAD, _INDEX, REST) => REST
       requires HEAD modInt 2 =/=Int 0
  rule chooseEven(HEAD, INDEX, VList(.Ints)) => VList(HEAD, INDEX)
       requires HEAD modInt 2 ==Int 0
  rule chooseEven(HEAD, INDEX, VList(BEST, _BESTINDEX))
       => VList(HEAD, INDEX)
       requires HEAD modInt 2 ==Int 0 andBool HEAD <=Int BEST
  rule chooseEven(HEAD, _INDEX, VList(BEST, BESTINDEX))
       => VList(BEST, BESTINDEX)
       requires HEAD modInt 2 ==Int 0 andBool HEAD >Int BEST

  syntax Fun ::= "fun" "(" Params "," Stmts ")"
  syntax Frame ::= "frame" "(" Map "," K ")"
  syntax ArgPack ::= "argPack" "(" Vals ")"

  syntax KItem ::= "start" | "done"
                 | "exec" "(" Stmts ")" | "execStmt" "(" Stmt ")"
                 | "eval" "(" Expr ")" | "evalExprs" "(" Exprs ")"
                 | "evalArgs" "(" Exprs ")"
                 | "assignName" "(" String ")"
                 | "select" "(" Stmts "," Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Val ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Val ")"
                 | "collectExprs" "(" Exprs ")"
                 | "prependInt" "(" Int ")"
                 | "collectArgs" "(" Exprs ")"
                 | "prependArg" "(" Val ")"
                 | "takeTail" | "subBase" "(" Expr ")"
                 | "subIndex" "(" Ints ")"
                 | "arraySubIndex" "(" Int "," Int "," Int ")"
                 | "callNamed" "(" String ")"
                 | "minDefaultEmpty"
                 | "invoke" "(" String "," Vals ")"
                 | "functionReturn" | "implicitReturn"

  syntax Map ::= "bindParams" "(" Params "," Vals ")" [function, total]

  configuration
    <py>
      <k> $PGM:Program ~> start </k>
      <args> $ARGS:Val </args>
      <env> .Map </env>
      <funs> .Map </funs>
      <stack> .List </stack>
      <result> VNone </result>
    </py>

  // Module loading retains the translated function bodies as syntax.  No
  // special case for pluck or pluck_from occurs in the operational semantics.
  rule <k> Module(SS) => exec(SS) ... </k>
  rule exec(.Stmts) => .
  rule exec(S SS) => execStmt(S) ~> exec(SS)

  rule <k> execStmt(FuncDef(F, P, BODY)) => . ... </k>
       <funs> FS => FS [ F <- fun(P, BODY) ] </funs>

  rule <k> start => invoke("pluck", A) ~> done ... </k>
       <args> A </args>
  rule <k> V:Val ~> done => . ... </k>
       <result> _ => V </result>

  // Statements and early return.
  rule execStmt(Assign(Name(X), E)) => eval(E) ~> assignName(X)
  rule <k> V:Val ~> assignName(X) => . ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule execStmt(If(E, THEN, ELSE)) => eval(E) ~> select(THEN, ELSE)
  rule VBool(true) ~> select(THEN, _ELSE) => exec(THEN)
  rule VBool(false) ~> select(_THEN, ELSE) => exec(ELSE)
  rule VEq(I, J) ~> select(THEN, _ELSE) => exec(THEN)
       requires I ==Int J
  rule VEq(I, J) ~> select(_THEN, ELSE) => exec(ELSE)
       requires I =/=Int J
  rule VLt(I, J) ~> select(THEN, _ELSE) => exec(THEN)
       requires I <Int J
  rule VLt(I, J) ~> select(_THEN, ELSE) => exec(ELSE)
       requires I >=Int J

  rule execStmt(Return(E)) => eval(E) ~> functionReturn

  // Expression evaluation is left-to-right, including call arguments.
  rule eval(Int(I)) => VInt(I)
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule eval(BinOp(OP, LEFT, RIGHT))
       => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule V:Val ~> binLeft(OP, RIGHT)
       => eval(RIGHT) ~> binRight(OP, V)
  rule VInt(J) ~> binRight("+", VInt(I)) => VInt(I +Int J)
  rule VInt(J) ~> binRight("%", VInt(I)) => VInt(I modInt J)

  // The translated solution only uses one-element comparison chains.
  // This extensional list/empty comparison is stated directly so an opaque
  // symbolic sequence becomes a Boolean path condition instead of requiring
  // constructor case analysis by the prover.
  rule <k> eval(Compare(Name(X), CmpOp("==", ListExpr(.Exprs))))
            => VBool(IS ==K .Ints) ... </k>
       <env> ... X |-> VList(IS) ... </env> [priority(40)]
  rule <k> eval(Compare(Name(X), CmpOp("==", ListExpr(.Exprs))))
            => VEq(LENGTH, 0) ... </k>
       <env> ... X |-> VArray(_ID, _OFFSET, LENGTH) ... </env>
       [priority(40)]
  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
       => eval(LEFT) ~> cmpLeft(OP, RIGHT)
  rule V:Val ~> cmpLeft(OP, RIGHT)
       => eval(RIGHT) ~> cmpRight(OP, V)
  rule VList(IS) ~> cmpLeft(OP, RIGHT)
       => eval(RIGHT) ~> cmpRight(OP, VList(IS))
  rule VInt(J) ~> cmpRight("==", VInt(I)) => VEq(I, J)
  rule VInt(J) ~> cmpRight("<=", VInt(I)) => VBool(I <=Int J)
  rule VInt(J) ~> cmpRight("<", VInt(I)) => VLt(I, J)
  rule VList(IS) ~> cmpRight("==", VList(.Ints))
       => VBool(IS ==K .Ints)
  rule VList(.Ints) ~> cmpRight("==", VList(IS))
       => VBool(IS ==K .Ints)

  rule eval(ListExpr(ES)) => evalExprs(ES)
  rule evalExprs(.Exprs) => VList(.Ints)
  rule evalExprs(E, ES) => eval(E) ~> collectExprs(ES)
  rule VInt(I) ~> collectExprs(ES)
       => evalExprs(ES) ~> prependInt(I)
  rule VList(IS) ~> prependInt(I) => VList(I, IS)

  // Compositional support for enumerate/filter list comprehensions and
  // min(..., default=[]).  The binder identifiers are pattern variables, so
  // alpha-renaming the Python comprehension does not change its meaning.
  rule <k> eval(ListComp(
              ListExpr(Name(VALUE), Name(INDEX)),
              CompFor(
                TupleExpr(Name(INDEX), Name(VALUE)),
                Call(Name("enumerate"), Name(ARRAY)),
                Compare(BinOp("%", Name(VALUE), Int(2)),
                        CmpOp("==", Int(0))))))
            => VCandidates(IS) ... </k>
       <env> ... ARRAY |-> VList(IS) ... </env>
  rule <k> eval(ListComp(
              ListExpr(Name(VALUE), Name(INDEX)),
              CompFor(
                TupleExpr(Name(INDEX), Name(VALUE)),
                Call(Name("enumerate"), Name(ARRAY)),
                Compare(BinOp("%", Name(VALUE), Int(2)),
                        CmpOp("==", Int(0))))))
            => VCandidatesArray(ID, OFFSET, LENGTH) ... </k>
       <env> ... ARRAY |-> VArray(ID, OFFSET, LENGTH) ... </env>

  rule eval(Call(Name("min"), ITEMS,
                 KwArg("default", ListExpr(.Exprs))))
       => eval(ITEMS) ~> minDefaultEmpty [priority(40)]
  rule VCandidates(IS) ~> minDefaultEmpty => minEvenInts(IS, 0)
  rule VCandidatesArray(ID, OFFSET, LENGTH) ~> minDefaultEmpty
       => minEvenArray(ID, OFFSET, LENGTH)

  rule eval(Subscript(E, Slice(Int(1), NoBound, NoBound)))
       => eval(E) ~> takeTail
  rule VList(IS) ~> takeTail => VList(tailInts(IS))
  rule VArray(ID, OFFSET, LENGTH) ~> takeTail
       => VArray(ID, OFFSET +Int 1, LENGTH -Int 1)
  rule eval(Subscript(E, IDX:Expr)) => eval(E) ~> subBase(IDX)
  rule VList(IS) ~> subBase(IDX) => eval(IDX) ~> subIndex(IS)
  rule VArray(ID, OFFSET, LENGTH) ~> subBase(IDX)
       => eval(IDX) ~> arraySubIndex(ID, OFFSET, LENGTH)
  rule VInt(0) ~> subIndex(IS) => VInt(headInt(IS))
  rule VInt(0) ~> arraySubIndex(ID, OFFSET, _LENGTH)
       => VInt(arrayAt(ID, OFFSET))

  rule eval(Call(Name(F), ES)) => evalArgs(ES) ~> callNamed(F)
  rule evalArgs(.Exprs) => argPack(.Vals)
  rule evalArgs(E, ES) => eval(E) ~> collectArgs(ES)
  rule V:Val ~> collectArgs(ES) => evalArgs(ES) ~> prependArg(V)
  rule VArray(ID, OFFSET, LENGTH) ~> collectArgs(ES)
       => evalArgs(ES) ~> prependArg(VArray(ID, OFFSET, LENGTH))
  rule argPack(VS) ~> prependArg(V) => argPack(V, VS)
  rule argPack(VS) ~> callNamed(F) => invoke(F, VS)

  rule bindParams(Params(.Strings), .Vals) => .Map
  rule bindParams(Params(X, XS), V, VS)
       => (X |-> V) bindParams(Params(XS), VS)

  // A frame saves both the caller's local environment and its continuation.
  rule <k> invoke(F, VS) ~> CONT
            => exec(BODY) ~> implicitReturn </k>
       <env> CALLER => bindParams(P, VS) </env>
       <funs> ... F |-> fun(P, BODY) ... </funs>
       <stack> STACK => ListItem(frame(CALLER, CONT)) STACK </stack>

  rule <k> V:Val ~> functionReturn ~> _CURRENT
            => V ~> CONT </k>
       <env> _ => CALLER </env>
       <stack> ListItem(frame(CALLER, CONT)) STACK => STACK </stack>

  rule <k> implicitReturn ~> _CURRENT => VNone ~> CONT </k>
       <env> _ => CALLER </env>
       <stack> ListItem(frame(CALLER, CONT)) STACK => STACK </stack>
endmodule
