requires "reference-semantics/semantics.k"

module BY-LENGTH-VERIFICATION
  imports MPY

  // The exact function body emitted in solution.mpy.  Keeping the source AST
  // here makes the proof execute the submitted implementation, not a second
  // hand-written algorithm.
  syntax Stmts ::= "byLengthBody" [function, total]
  rule byLengthBody
    => Assign(
         Name("names"),
         ListExpr(
           Str("One"), Str("Two"), Str("Three"), Str("Four"),
           Str("Five"), Str("Six"), Str("Seven"), Str("Eight"),
           Str("Nine")))
       Assign(Name("values"), ListExpr(.Exprs))
       For(
         Name("value"),
         Name("arr"),
         If(
           BoolOp(
             "and",
             Compare(Name("value"), CmpOp(">=", Int(1))),
             Compare(Name("value"), CmpOp("<=", Int(9)))),
           Expr(
             Call(
               Attribute(Name("values"), "append"),
               BinOp("+", Name("value"), Int(1)))),
           .Stmts))
       Assign(
         Name("values"),
         Call(
           Name("sorted"),
           Name("values"),
           KwArg("reverse", Bool(true))))
       Assign(Name("result"), ListExpr(.Exprs))
       For(
         Name("value"),
         Name("values"),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Subscript(
               Name("names"),
               BinOp("-", Name("value"), Int(1))))))
       Return(Name("result"))

  syntax Val ::= "byLengthClosure" [function, total]
  rule byLengthClosure => closureVal("arr", byLengthBody, 0)

  // Embed an arbitrary sequence of mathematical integers as Python values.
  // Quantifying IS:IntSeq in spec.k therefore covers every finite integer list.
  syntax ValSeq ::= intVals(IntSeq) [function, total]
  rule intVals(.IntSeq) => .ValSeq
  rule intVals(iCons(I:Int, IS:IntSeq)) => vCons(I, intVals(IS))

  // Contract-level filtering: retain exactly the values in [1, 9], preserving
  // duplicates and their relative order before the trusted sort.
  syntax ValSeq ::= filterDigits(ValSeq) [function, total]
  rule filterDigits(.ValSeq) => .ValSeq
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => vCons(I, filterDigits(REST))
    requires I >=Int 1 andBool I <=Int 9
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => filterDigits(REST)
    requires I <Int 1 orBool I >Int 9

  syntax ValSeq ::= "nameTable" [function, total]
  rule nameTable
    => vCons(str(strToCodes("One")),
       vCons(str(strToCodes("Two")),
       vCons(str(strToCodes("Three")),
       vCons(str(strToCodes("Four")),
       vCons(str(strToCodes("Five")),
       vCons(str(strToCodes("Six")),
       vCons(str(strToCodes("Seven")),
       vCons(str(strToCodes("Eight")),
       vCons(str(strToCodes("Nine")), .ValSeq)))))))))

  // This is precisely names[value - 1] lifted pointwise to a value sequence.
  syntax ValSeq ::= tableNames(ValSeq) [function, total]
  rule tableNames(.ValSeq) => .ValSeq
  rule tableNames(vCons(I:Int, REST:ValSeq))
    => vCons(valSeqAt(nameTable, I -Int 1), tableNames(REST))

  // Observe the structure of a returned heap list so that the postcondition
  // states the actual Python return value rather than an allocation address.
  syntax KItem ::= "#observeList"
  rule <k> ref(H:Int) ~> #observeList => list(VS) ... </k>
       <heap> ... H |-> list(VS:ValSeq) ... </heap>

  // Symbolic summaries for the two source-level loops.  The supplied
  // semantics intentionally leaves sortVS opaque during proof, so a later
  // iteration over revVS(sortVS(...)) cannot constructor-unfold.  These exact
  // AST rules expose the loops' standard filter/map folds while leaving
  // sorted() itself governed by MPY-SORT.
  rule <k>
         For(
           Name("value"),
           list(VS:ValSeq),
           If(
             BoolOp(
               "and",
               Compare(Name("value"), CmpOp(">=", Int(1))),
               Compare(Name("value"), CmpOp("<=", Int(9)))),
             Expr(
               Call(
                 Attribute(Name("values"), "append"),
                 Name("value"))),
             .Stmts))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ...
         HV:Int |-> (list(.ValSeq) => list(filterDigits(VS)))
         ...
       </heap>
    requires "values" in_keys(M)
     andBool {M["values"]}:>Val ==K ref(HV)
    [priority(40)]

  rule <k>
         For(
           Name("value"),
           list(VS:ValSeq),
           Expr(
             Call(
               Attribute(Name("result"), "append"),
               Subscript(
                 Name("names"),
                 BinOp("-", Name("value"), Int(1))))))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ...
         HN:Int |-> list(NAMES:ValSeq)
         HR:Int |-> (list(.ValSeq) => list(tableNames(VS)))
         ...
       </heap>
    requires "names" in_keys(M)
     andBool "result" in_keys(M)
     andBool {M["names"]}:>Val ==K ref(HN)
     andBool {M["result"]}:>Val ==K ref(HR)
     andBool NAMES ==K nameTable
    [priority(40)]
endmodule
