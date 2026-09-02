requires "domains.md"

module MAXIMUM-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports LIST
  imports MAP

  syntax Module ::= "Module" "(" Stmt ")" [symbol(Module)]
  syntax Params ::= "Params" "(" String "," String ")" [symbol(Params)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")"                         [symbol(Return)]

  syntax Expr ::= "Name" "(" String ")"                         [symbol(Name)]
                | "Call" "(" Expr "," Expr ")"                 [symbol(Call)]
                | "BinOp" "(" String "," Expr "," Expr ")"     [symbol(BinOp)]
                | "Subscript" "(" Expr "," Expr ")"             [symbol(Subscript)]
                | "Slice" "(" Bound "," Bound "," Bound ")"    [symbol(Slice)]
  syntax Bound ::= Expr | "NoBound" [symbol(NoBound)]

  syntax Val ::= "intVal" "(" Int ")"
               | "listVal" "(" List ")"
               | "noResult"
endmodule

module MAXIMUM
  imports MAXIMUM-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports LIST
  imports MAP

  configuration
    <maximum>
      <k> $PGM:Module ~> boot </k>
      <args> $ARGS:List </args>
      <env> .Map </env>
      <out> noResult </out>
    </maximum>

  syntax KItem ::= "boot" | "finish" "(" Val ")"

  rule <k> Module(FuncDef("maximum", Params("arr", "k"), BODY:Stmt)) ~> boot
         => BODY ...</k>
       <args> ListItem(listVal(L:List)) ListItem(intVal(K:Int)) </args>
       <env> .Map => ("arr" |-> listVal(L)) ("k" |-> intVal(K)) </env>

  rule <k> Return(E:Expr) => finish(eval(E, RHO)) </k>
       <env> RHO:Map </env>

  rule <k> finish(V:Val) => .K </k>
       <out> noResult => V </out>

  syntax Val ::= "eval" "(" Expr "," Map ")" [function]
  rule eval(Name(X:String), (X |-> V:Val) _REST:Map) => V
  rule eval(Call(Name("sorted"), E:Expr), RHO:Map)
    => sortedVal(eval(E, RHO))
  rule eval(Call(Name("len"), E:Expr), RHO:Map)
    => lengthVal(eval(E, RHO))
  rule eval(BinOp("-", LEFT:Expr, RIGHT:Expr), RHO:Map)
    => subtractVal(eval(LEFT, RHO), eval(RIGHT, RHO))
  rule eval(Subscript(BASE:Expr, Slice(START:Expr, NoBound, NoBound)), RHO:Map)
    => suffixVal(eval(BASE, RHO), eval(START, RHO))

  syntax Val ::= "sortedVal" "(" Val ")" [function]
               | "lengthVal" "(" Val ")" [function]
               | "subtractVal" "(" Val "," Val ")" [function]
               | "suffixVal" "(" Val "," Val ")" [function]
  rule sortedVal(listVal(L:List)) => listVal(sortInts(L))
  rule lengthVal(listVal(L:List)) => intVal(size(L))
  rule subtractVal(intVal(I:Int), intVal(J:Int)) => intVal(I -Int J)
  rule suffixVal(listVal(L:List), intVal(N:Int)) => listVal(dropInts(N, L))

  syntax List ::= "sortInts" "(" List ")" [function]
                | "insertInt" "(" Int "," List ")" [function]
                | "dropInts" "(" Int "," List ")" [function]
  rule sortInts(.List) => .List
  rule sortInts(ListItem(I:Int) REST:List)
    => insertInt(I, sortInts(REST))

  rule insertInt(I:Int, .List) => ListItem(I)
  rule insertInt(I:Int, ListItem(J:Int) REST:List)
    => ListItem(I) ListItem(J) REST
    requires I <=Int J
  rule insertInt(I:Int, ListItem(J:Int) REST:List)
    => ListItem(J) insertInt(I, REST)
    requires I >Int J

  rule dropInts(0, L:List) => L
  rule dropInts(N:Int, ListItem(_:Int) REST:List)
    => dropInts(N -Int 1, REST)
    requires N >Int 0
endmodule
