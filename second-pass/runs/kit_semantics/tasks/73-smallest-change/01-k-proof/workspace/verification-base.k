requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Exact syntax of the submitted program.  These macros only avoid repeating
  // the AST term in the reachability claims; macro expansion leaves the fixed
  // MPY execution rules in control.
  syntax Stmts ::= "smallestLoopBody" [macro]
  rule smallestLoopBody
    => If(
         Compare(
           Subscript(Name("arr"), Name("i")),
           CmpOp(
             "!=",
             Subscript(
               Name("arr"),
               BinOp(
                 "-",
                 BinOp("-", Call(Name("len"), Name("arr")), Name("i")),
                 Int(1))))),
         AugAssign(Name("changes"), "+", Int(1)),
         .Stmts)
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= "smallestBody" [macro]
  rule smallestBody
    => Assign(Name("changes"), Int(0))
       Assign(Name("i"), Int(0))
       While(
         Compare(
           Name("i"),
           CmpOp(
             "<",
             BinOp(
               "//",
               Call(Name("len"), Name("arr")),
               Int(2)))),
         smallestLoopBody)
       Return(Name("changes"))

  syntax Stmt ::= "smallestDef" [macro]
  rule smallestDef
    => FuncDef("smallest_change", Params("arr"), smallestBody)

  // Constructor-only expansion of MPY-CORE's builtinsScope.  Ordinary rule
  // left-hand sides cannot contain the builtinsScope function symbol.
  syntax Scope ::= "fixedBuiltins" [macro]
  rule fixedBuiltins
    => scope("len" |-> builtinV("len")
             "set" |-> builtinV("set")
             "sum" |-> builtinV("sum")
             "abs" |-> builtinV("abs")
             "min" |-> builtinV("min")
             "max" |-> builtinV("max")
             "ord" |-> builtinV("ord")
             "chr" |-> builtinV("chr")
             "range" |-> builtinV("range")
             "all" |-> builtinV("all")
             "any" |-> builtinV("any")
             "zip" |-> builtinV("zip")
             "isinstance" |-> builtinV("isinstance")
             "sorted" |-> builtinV("sorted")
             "list" |-> builtinV("list")
             "round" |-> builtinV("round")
             "bin" |-> builtinV("bin")
             "enumerate" |-> builtinV("enumerate")
             "map" |-> builtinV("map")
             "eval" |-> builtinV("eval")
             "int" |-> typeV("int")
             "str" |-> typeV("str")
             "float" |-> typeV("float"),
             root)

  // The source contract says arr is a list of integers.  This predicate is a
  // total structural characterization of precisely those MPY ValSeq values.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq)                => true
  rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)

  // Exact value of the submitted `len(arr) // 2` under MPY-INT.
  syntax Int ::= halfLen(ValSeq) [function, total]
  rule halfLen(VS:ValSeq)
    => (vsLen(VS)
        -Int (((vsLen(VS) %Int 2) +Int 2) %Int 2))
       /Int 2
    [simplification]

  // MPY's symbolic subscript result has dynamic sort Val even under allInts.
  // Structural induction on VS establishes that both in-bounds values are
  // Ints, so the supplied MPY-INT comparison is defined.  This lemma exposes
  // no result value and leaves applyCmp itself uninterpreted until its actual
  // Int operands are known.
  rule #Ceil(
         applyCmp(
           "!=",
           valSeqAt(VS:ValSeq, I:Int),
           valSeqAt(VS, vsLen(VS) -Int I +Int -1)))
    => #Top
    requires allInts(VS)
      andBool 0 <=Int I
      andBool I <Int halfLen(VS)
    [simplification]

  // Exact operational bridge justified by count-branch-true/false in the
  // bridge-free branch-connection-spec.k.  It summarizes only the fixed
  // branch plus its one AugAssign and preserves the arbitrary continuation.
  rule <k>
         #branch(
           B:Bool,
           AugAssign(Name("changes"), "+", Int(1)),
           .Stmts)
         =>
         .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         1 |-> scope(
                "arr" |-> list(VS:ValSeq)
                "changes"
                  |-> (C:Int
                       => C +Int (#if B #then 1 #else 0 #fi))
                "i" |-> I:Int,
                parent(0))
         REST:Map
       </scopes>

  // pairDiff uses the supplied comparison operation itself.  It is 1 exactly
  // when the program's integer comparison at mirrored index I is true.
  syntax Int ::= pairDiff(ValSeq, Int) [function]
  rule pairDiff(VS:ValSeq, I:Int)
    => #if applyCmp(
              "!=",
              valSeqAt(VS, I),
              valSeqAt(VS, vsLen(VS) -Int I -Int 1))
       #then 1
       #else 0
       #fi

  // Number of unequal mirrored pairs for indices I .. STOP-1.
  syntax Int ::= mismatchCount(ValSeq, Int, Int) [function]
  rule mismatchCount(_VS:ValSeq, I:Int, STOP:Int) => 0
    requires I >=Int STOP
  rule mismatchCount(VS:ValSeq, I:Int, STOP:Int)
    => pairDiff(VS, I) +Int mismatchCount(VS, I +Int 1, STOP)
    requires I <Int STOP

  rule (A:Int +Int B:Int) +Int C:Int
    => A +Int (B +Int C)
    [simplification]
endmodule
