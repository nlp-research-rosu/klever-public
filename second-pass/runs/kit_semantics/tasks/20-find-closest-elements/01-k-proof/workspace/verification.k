requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports FLOAT-SYNTAX

  syntax Stmts ::= "innerBody" [macro]
                 | "outerBody" [macro]
                 | "findBody"  [macro]
  syntax Module ::= "solutionModule" [macro]

endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  syntax Bool ::= allFloatVS(ValSeq)    [function, total]
                | allFloatItems(ValSeq) [function, total]
                | candidateWins(Val, Val, Float, Float) [function, total]
  syntax Float ::= floatProjection(Val) [function, total, no-evaluators]
                 | itemFloat(Val)       [function, total, no-evaluators]
                 | orderedFirst(Float, Float) [function, total]
                 | orderedSecond(Float, Float) [function, total]
                 | stepFirst(Val, Val, Float, Float) [function, total]
                 | stepSecond(Val, Val, Float, Float) [function, total]
                 | innerFirst(Val, ValSeq, Float, Float) [function, total]
                 | innerSecond(Val, ValSeq, Float, Float) [function, total]
                 | outerFirst(ValSeq, ValSeq, Float, Float) [function, total]
                 | outerSecond(ValSeq, ValSeq, Float, Float) [function, total]
  syntax Int ::= itemIndex(Val) [function, total, no-evaluators]
  syntax Val ::= lastItem(ValSeq, Val) [function, total]

  rule innerBody
    => If(
         Compare(
           Subscript(Name("item1"), Int(0)),
           CmpOp("<", Subscript(Name("item2"), Int(0)))),
         If(
           Compare(
             Call(
               Name("abs"),
               (BinOp(
                 "-",
                 Subscript(Name("item2"), Int(1)),
                 Subscript(Name("item1"), Int(1))),
                .Exprs)),
             CmpOp(
               "<",
               Call(
                 Name("abs"),
                 (BinOp(
                   "-",
                   Subscript(Name("closest"), Int(1)),
                   Subscript(Name("closest"), Int(0))),
                  .Exprs)))),
           If(
             Compare(
               Subscript(Name("item1"), Int(1)),
               CmpOp("<", Subscript(Name("item2"), Int(1)))),
             (Assign(
                Name("closest"),
                TupleExpr(
                  (Subscript(Name("item1"), Int(1)),
                   Subscript(Name("item2"), Int(1)),
                   .Exprs)))
              .Stmts),
             (Assign(
                Name("closest"),
                TupleExpr(
                  (Subscript(Name("item2"), Int(1)),
                   Subscript(Name("item1"), Int(1)),
                   .Exprs)))
              .Stmts)),
           .Stmts),
         .Stmts)

  rule outerBody
    => (For(Name("item2"), Name("items"), innerBody) .Stmts)

  rule findBody
    => If(
         Compare(
           Subscript(Name("numbers"), Int(0)),
           CmpOp("<", Subscript(Name("numbers"), Int(1)))),
         (Assign(
            Name("closest"),
            TupleExpr(
              (Subscript(Name("numbers"), Int(0)),
               Subscript(Name("numbers"), Int(1)),
               .Exprs)))
          .Stmts),
         (Assign(
            Name("closest"),
            TupleExpr(
              (Subscript(Name("numbers"), Int(1)),
               Subscript(Name("numbers"), Int(0)),
               .Exprs)))
          .Stmts))
       Assign(
         Name("items"),
         Call(
           Name("list"),
           (Call(Name("enumerate"), (Name("numbers"), .Exprs)), .Exprs)))
       Assign(Name("item1"), Subscript(Name("items"), Int(0)))
       Assign(Name("item2"), Subscript(Name("items"), Int(0)))
       For(Name("item1"), Name("items"), outerBody)
       Return(Name("closest"))
       .Stmts

  rule solutionModule
    => Module(
         ImportFrom("typing", ("List", "Tuple", .ParamNames))
         FuncDef(
           "find_closest_elements",
           Params(("numbers", .ParamNames)),
           findBody)
         .Stmts)

  rule allFloatVS(.ValSeq) => true
  rule allFloatVS(vCons(V:Val, REST:ValSeq))
    => (V ==K floatProjection(V)) andBool allFloatVS(REST)
  rule floatProjection(F:Float) => F

  rule allFloatItems(.ValSeq) => true
  rule allFloatItems(vCons(V:Val, REST:ValSeq))
    => ( V
         ==K
         tuple(
           vCons(
             itemIndex(V),
             vCons(itemFloat(V), .ValSeq))) )
       andBool allFloatItems(REST)
  rule itemIndex(
         tuple(vCons(I:Int, vCons(_:Float, .ValSeq))))
    => I
  rule itemFloat(
         tuple(vCons(_:Int, vCons(F:Float, .ValSeq))))
    => F

  rule applyIndex(V:Val, 0) => itemIndex(V)
    requires V
      ==K tuple(
            vCons(
              itemIndex(V),
              vCons(itemFloat(V), .ValSeq)))
    [simplification]
  rule applyIndex(V:Val, 1) => itemFloat(V)
    requires V
      ==K tuple(
            vCons(
              itemIndex(V),
              vCons(itemFloat(V), .ValSeq)))
    [simplification]

  rule allFloatItems(enumVS(VS:ValSeq, _:Int))
    => true
    requires allFloatVS(VS)
    [simplification]

  rule orderedFirst(X:Float, Y:Float) => X
    requires floatLt(X, Y)
  rule orderedFirst(X:Float, Y:Float) => Y
    requires notBool floatLt(X, Y)
  rule orderedSecond(X:Float, Y:Float) => Y
    requires floatLt(X, Y)
  rule orderedSecond(X:Float, Y:Float) => X
    requires notBool floatLt(X, Y)
  rule candidateWins(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => itemIndex(ITEM1) <Int itemIndex(ITEM2)
       andBool floatLt(
                 absF(subF(itemFloat(ITEM2), itemFloat(ITEM1))),
                 absF(subF(B, A)))

  rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => A
    requires notBool candidateWins(ITEM1, ITEM2, A, B)
  rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => itemFloat(ITEM1)
    requires candidateWins(ITEM1, ITEM2, A, B)
     andBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))
  rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => itemFloat(ITEM2)
    requires candidateWins(ITEM1, ITEM2, A, B)
     andBool notBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))

  rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => B
    requires notBool candidateWins(ITEM1, ITEM2, A, B)
  rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => itemFloat(ITEM2)
    requires candidateWins(ITEM1, ITEM2, A, B)
     andBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))
  rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float)
    => itemFloat(ITEM1)
    requires candidateWins(ITEM1, ITEM2, A, B)
     andBool notBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))

  rule innerFirst(_ITEM1:Val, .ValSeq, A:Float, _B:Float) => A
  rule innerFirst(
         ITEM1:Val,
         vCons(ITEM2:Val, REST:ValSeq),
         A:Float,
         B:Float)
    => innerFirst(
         ITEM1,
         REST,
         stepFirst(ITEM1, ITEM2, A, B),
         stepSecond(ITEM1, ITEM2, A, B))

  rule innerSecond(_ITEM1:Val, .ValSeq, _A:Float, B:Float) => B
  rule innerSecond(
         ITEM1:Val,
         vCons(ITEM2:Val, REST:ValSeq),
         A:Float,
         B:Float)
    => innerSecond(
         ITEM1,
         REST,
         stepFirst(ITEM1, ITEM2, A, B),
         stepSecond(ITEM1, ITEM2, A, B))

  rule outerFirst(.ValSeq, _ALL:ValSeq, A:Float, _B:Float) => A
  rule outerFirst(
         vCons(ITEM1:Val, REST:ValSeq),
         ALL:ValSeq,
         A:Float,
         B:Float)
    => outerFirst(
         REST,
         ALL,
         innerFirst(ITEM1, ALL, A, B),
         innerSecond(ITEM1, ALL, A, B))

  rule outerSecond(.ValSeq, _ALL:ValSeq, _A:Float, B:Float) => B
  rule outerSecond(
         vCons(ITEM1:Val, REST:ValSeq),
         ALL:ValSeq,
         A:Float,
         B:Float)
    => outerSecond(
         REST,
         ALL,
         innerFirst(ITEM1, ALL, A, B),
         innerSecond(ITEM1, ALL, A, B))

  rule lastItem(.ValSeq, OLD:Val) => OLD
  rule lastItem(vCons(V:Val, REST:ValSeq), _OLD:Val)
    => lastItem(REST, V)
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  rule <k>
         #loop(list(REST:ValSeq), Name("item2"), innerBody)
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         -1 |-> scope(
                "len"        |-> builtinV("len")
                "set"        |-> builtinV("set")
                "sum"        |-> builtinV("sum")
                "abs"        |-> builtinV("abs")
                "min"        |-> builtinV("min")
                "max"        |-> builtinV("max")
                "ord"        |-> builtinV("ord")
                "chr"        |-> builtinV("chr")
                "range"      |-> builtinV("range")
                "all"        |-> builtinV("all")
                "any"        |-> builtinV("any")
                "zip"        |-> builtinV("zip")
                "isinstance" |-> builtinV("isinstance")
                "sorted"     |-> builtinV("sorted")
                "list"       |-> builtinV("list")
                "round"      |-> builtinV("round")
                "bin"        |-> builtinV("bin")
                "enumerate"  |-> builtinV("enumerate")
                "map"        |-> builtinV("map")
                "eval"       |-> builtinV("eval")
                "int"        |-> typeV("int")
                "str"        |-> typeV("str")
                "float"      |-> typeV("float"),
                root)
         0 |-> scope(
                "find_closest_elements"
                  |-> closureVal(
                        ("numbers", .ParamNames),
                        findBody,
                        0),
                parent(-1))
         1 |-> scope(
                "numbers" |-> _NUMBERS:Val
                "items"   |-> _ITEMSREF:Val
                "item1"   |-> ITEM1:Val
                "item2"   |-> (OLD2:Val => lastItem(REST, OLD2))
                "closest" |->
                  ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq)))
                    =>
                    tuple(
                      vCons(
                        innerFirst(ITEM1, REST, A, B),
                        vCons(
                          innerSecond(ITEM1, REST, A, B),
                          .ValSeq))) ),
                parent(0))
       </scopes>
    requires ITEM1
       ==K tuple(
             vCons(
               itemIndex(ITEM1),
               vCons(itemFloat(ITEM1), .ValSeq)))
     andBool allFloatItems(REST)
    [priority(40)]
endmodule
