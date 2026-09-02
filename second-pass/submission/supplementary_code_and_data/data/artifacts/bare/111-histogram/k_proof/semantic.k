module MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports K-EQUAL
  imports MAP
  imports LIST

  syntax Program ::= Module(Stmts)

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Assign(Expr, Expr)
                | For(Expr, Expr, Stmts)
                | If(Expr, Stmts, Stmts)
                | Return(Expr)

  syntax Params ::= Params(String)

  syntax Exprs ::= List{Expr, ","}
  syntax Entries ::= List{Entry, ","}
  syntax Entry ::= Entry(Expr, Expr)
  syntax CmpOp ::= CmpOp(String, Expr)

  syntax Expr ::= Name(String)
                | Int(Int)
                | Str(String)
                | DictExpr(Entries)
                | Attribute(Expr, String)
                | Call(Expr, Exprs)
                | Subscript(Expr, Expr)
                | BinOp(String, Expr, Expr)
                | Compare(Expr, CmpOp)
endmodule

module SEMANTIC
  imports MPY-SYNTAX

  // Runtime values. Dictionaries retain an insertion-order key list because
  // Python iteration over a dictionary visits keys in insertion order.
  syntax PyVal ::= pyInt(Int)
                 | pyString(String)
                 | pyWords(List)
                 | pyList(List)
                 | pyDict(Map, List)
                 | pyBool(Bool)

  syntax ExecResult ::= normal(Map)
                      | returning(Map, PyVal)

  syntax KItem ::= execute(Program, String)
                 | executeWords(Program, List)

  configuration <k> execute($PGM:Program, $TEST:String) </k>

  // Entry-point setup. executeWords is a verification harness for an
  // arbitrary already-tokenized valid input; execute is the concrete runner.
  rule execute(Module(FuncDef("histogram", Params("test"), BODY)), S)
    => resultOf(exec(BODY, "test" |-> pyString(S)))

  rule executeWords(Module(FuncDef("histogram", Params("test"), BODY)), WORDS)
    => resultOf(exec(BODY, "test" |-> pyWords(WORDS)))

  syntax PyVal ::= resultOf(ExecResult) [function, total]
  rule resultOf(returning(_, VALUE)) => VALUE
  rule resultOf(normal(_)) => pyBool(false)

  // Python str.split() for the prompt's space-separated input language. Empty
  // fields are skipped, matching Python for one or several ASCII spaces.
  syntax List ::= splitWords(String) [function, total]
  rule splitWords("") => .List
  rule splitWords(S) => splitWords(substrString(S, 1, lengthString(S)))
    requires S =/=String "" andBool substrString(S, 0, 1) ==String " "
  rule splitWords(S) => ListItem(pyString(S))
    requires S =/=String "" andBool findString(S, " ", 0) ==Int -1
  rule splitWords(S) => ListItem(pyString(substrString(S, 0, findString(S, " ", 0))))
                          splitWords(substrString(S, findString(S, " ", 0) +Int 1,
                                                  lengthString(S)))
    requires findString(S, " ", 0) >Int 0

  syntax PyVal ::= splitValue(PyVal) [function, total]
  rule splitValue(pyString(S)) => pyList(splitWords(S))
  rule splitValue(pyWords(WORDS)) => pyList(WORDS)
  rule splitValue(_) => pyList(.List) [owise]

  // Expression evaluation for the constructors used by solution.mpy.
  syntax PyVal ::= eval(Expr, Map) [function, total]
  rule eval(Int(I), _) => pyInt(I)
  rule eval(Str(S), _) => pyString(S)
  rule eval(Name(X), ENV) => envGet(ENV, X)
  rule eval(DictExpr(.Entries), _) => pyDict(.Map, .List)
  rule eval(Call(Attribute(Name(X), "split"), .Exprs), ENV)
    => splitValue(envGet(ENV, X))
  rule eval(Subscript(DICT, KEY), ENV)
    => dictGet(eval(DICT, ENV), eval(KEY, ENV))
  rule eval(BinOp("+", LEFT, RIGHT), ENV)
    => addValues(eval(LEFT, ENV), eval(RIGHT, ENV))
  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)), ENV)
    => compareValues(OP, eval(LEFT, ENV), eval(RIGHT, ENV))
  rule eval(_, _) => pyBool(false) [owise]

  syntax PyVal ::= envGet(Map, String) [function, total]
  rule envGet(ENV[X <- VALUE:PyVal], X) => VALUE [simplification]
  rule envGet(ENV[X <- _], Y) => envGet(ENV, Y)
    requires X =/=String Y [simplification]
  rule envGet((X |-> VALUE:PyVal) REST, X) => VALUE

  syntax PyVal ::= dictGet(PyVal, PyVal) [function, total]
  rule dictGet(pyDict(DICT[KEY <- VALUE:PyVal], _), KEY) => VALUE [simplification]
  rule dictGet(pyDict(DICT[KEY1 <- _], KEYS), KEY2)
    => dictGet(pyDict(DICT, KEYS), KEY2)
    requires KEY1 =/=K KEY2 [simplification]
  rule dictGet(pyDict((KEY |-> VALUE:PyVal) REST, _), KEY) => VALUE
  rule dictGet(_, _) => pyBool(false) [owise]

  syntax PyVal ::= addValues(PyVal, PyVal) [function, total]
  rule addValues(pyInt(I), pyInt(J)) => pyInt(I +Int J)
  rule addValues(_, _) => pyBool(false) [owise]

  syntax PyVal ::= compareValues(String, PyVal, PyVal) [function, total]
  rule compareValues("in", KEY, pyDict(DICT, _)) => pyBool(KEY in_keys(DICT))
  rule compareValues(">", pyInt(I), pyInt(J)) => pyBool(I >Int J)
  rule compareValues("==", LEFT, RIGHT) => pyBool(LEFT ==K RIGHT)
  rule compareValues(_, _, _) => pyBool(false) [owise]

  syntax Bool ::= truth(PyVal) [function, total]
  rule truth(pyBool(B)) => B
  rule truth(pyInt(I)) => I =/=Int 0
  rule truth(_) => false [owise]

  // Assignment supports local names and dictionary subscripts, the two target
  // forms used by the implementation.
  syntax Map ::= assign(Expr, PyVal, Map) [function, total]
  rule assign(Name(X), VALUE, ENV) => ENV[X <- VALUE]
  rule assign(Subscript(Name(X), KEY), VALUE, ENV)
    => ENV[X <- dictSet(envGet(ENV, X), eval(KEY, ENV), VALUE)]
  rule assign(_, _, ENV) => ENV [owise]

  syntax PyVal ::= dictSet(PyVal, PyVal, PyVal) [function, total]
  rule dictSet(pyDict(DICT, KEYS), KEY, VALUE)
    => pyDict(DICT[KEY <- VALUE], KEYS)
    requires KEY in_keys(DICT)
  rule dictSet(pyDict(DICT, KEYS), KEY, VALUE)
    => pyDict(DICT[KEY <- VALUE], KEYS ListItem(KEY))
    requires notBool (KEY in_keys(DICT))
  rule dictSet(VALUE, _, _) => VALUE [owise]

  syntax List ::= iterable(PyVal) [function, total]
  rule iterable(pyList(ITEMS)) => ITEMS
  rule iterable(pyDict(_, KEYS)) => KEYS
  rule iterable(_) => .List [owise]

  // Deterministic big-step statement execution. execFor threads both normal
  // state and an early return, so it is usable beyond this particular body.
  syntax ExecResult ::= exec(Stmts, Map) [function, total]
                      | execNext(ExecResult, Stmts) [function, total]
                      | execStmt(Stmt, Map) [function, total]
                      | execIf(Bool, Stmts, Stmts, Map) [function, total]
                      | execFor(Expr, List, Stmts, Map) [function, total]
                      | execForNext(ExecResult, Expr, List, Stmts) [function, total]

  rule exec(.Stmts, ENV) => normal(ENV)
  rule exec(STMT REST, ENV) => execNext(execStmt(STMT, ENV), REST)

  rule execNext(normal(ENV), REST) => exec(REST, ENV)
  rule execNext(returning(ENV, VALUE), _) => returning(ENV, VALUE)

  rule execStmt(Assign(TARGET, VALUE), ENV)
    => normal(assign(TARGET, eval(VALUE, ENV), ENV))
  rule execStmt(If(TEST, YES, NO), ENV)
    => execIf(truth(eval(TEST, ENV)), YES, NO, ENV)
  rule execStmt(For(TARGET, SOURCE, BODY), ENV)
    => execFor(TARGET, iterable(eval(SOURCE, ENV)), BODY, ENV)
  rule execStmt(Return(VALUE), ENV) => returning(ENV, eval(VALUE, ENV))
  rule execStmt(_, ENV) => normal(ENV) [owise]

  rule execIf(CONDITION, YES, _, ENV) => exec(YES, ENV)
    requires CONDITION
  rule execIf(CONDITION, _, NO, ENV) => exec(NO, ENV)
    requires notBool CONDITION

  rule execFor(_, .List, _, ENV) => normal(ENV)
  rule execFor(TARGET, ListItem(ITEM) (REST:List), BODY, ENV)
    => execForNext(exec(BODY, assign(TARGET, ITEM, ENV)), TARGET, REST, BODY)

  rule execForNext(normal(ENV), TARGET, REST, BODY)
    => execFor(TARGET, REST, BODY, ENV)
  rule execForNext(returning(ENV, VALUE), _, _, _)
    => returning(ENV, VALUE)
endmodule
