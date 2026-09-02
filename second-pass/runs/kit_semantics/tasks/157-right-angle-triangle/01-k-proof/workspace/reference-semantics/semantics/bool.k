// reference/src/semantics/bool.k — MPY-BOOL
// Bool operator cases + the truthy boolean operations (not / and / or; and-or are
// value-returning short-circuit over any Vals, per Python).

module MPY-BOOL
  imports MPY-CORE

  rule applyUn("not", V:Val) => notBool truthy(V)

  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // bool is a subtype of int: a Bool compared with an Int promotes to 0/1 and
  // re-dispatches to the Int comparison cases (True==1, False==0, True<2, ...).
  // The == / != Bool x Bool cases above are kept; only the four ordering ops are
  // promoted for Bool x Bool (to avoid duplicating the two rules above).
  rule applyCmp(OP:String, B:Bool, I:Int) => applyCmp(OP, boolAsInt(B), I)
       requires isEqOrdOp(OP)
  rule applyCmp(OP:String, I:Int, B:Bool) => applyCmp(OP, I, boolAsInt(B))
       requires isEqOrdOp(OP)
  rule applyCmp(OP:String, B1:Bool, B2:Bool) => applyCmp(OP, boolAsInt(B1), boolAsInt(B2))
       requires isOrdOp(OP)

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
  context BoolOp(_, (HOLE:Expr, _:Exprs))
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
endmodule
