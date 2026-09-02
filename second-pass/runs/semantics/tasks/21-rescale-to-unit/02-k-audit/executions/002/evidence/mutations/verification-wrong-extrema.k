requires "reference-semantics/semantics.k"

module VERIFICATION-WRONG-EXTREMA
  imports MPY

  // Opaque extrema are the symbolic counterparts of the concrete float folds.
  // The reference float semantics explicitly reserves these problem-local
  // summaries because Haskell has no useful symbolic IEEE-754 theory.
  syntax Float ::= minVF(ValSeq) [function, total, symbol(minVF), no-evaluators]
                 | maxVF(ValSeq) [function, total, symbol(maxVF), no-evaluators]
  // Adversarial interpretation admitted by the original opaque declarations.
  syntax Float ::= wrongLo() [function, total, symbol(wrongLo), no-evaluators]
                 | wrongHi() [function, total, symbol(wrongHi), no-evaluators]
  rule minVF(_:ValSeq) => wrongLo()
  rule maxVF(_:ValSeq) => wrongHi()

  rule <k> #applyK(toCall(builtinV("min")), (list(VS:ValSeq), .Vals))
        => minVF(VS) ... </k>
       [priority(40)]
  rule <k> #applyK(toCall(builtinV("max")), (list(VS:ValSeq), .Vals))
        => maxVF(VS) ... </k>
       [priority(40)]

  // A mathematical description of the returned list.  The accumulator form
  // mirrors the reference semantics' expansion of a list comprehension.
  syntax Float ::= asFloat(Val) [function, total, symbol(asFloat)]
  rule asFloat(F:Float) => F

  syntax Float ::= scaleF(Float, Float, Float) [function, total]
  rule scaleF(F:Float, LO:Float, HI:Float)
    => divF(subF(F, LO), subF(HI, LO))

  syntax ValSeq ::= scaleAcc(ValSeq, ValSeq, Float, Float) [function, total]
  rule scaleAcc(ACC:ValSeq, .ValSeq, _:Float, _:Float) => ACC
  rule scaleAcc(ACC:ValSeq, vCons(V:Val, REST:ValSeq), LO:Float, HI:Float)
    => scaleAcc(
         valSeqConcat(ACC, vCons(scaleF(asFloat(V), LO, HI), .ValSeq)),
         REST,
         LO,
         HI)

  syntax Bool ::= allFloats(ValSeq) [function, total]
  rule allFloats(.ValSeq) => true
  rule allFloats(vCons(V:Val, REST:ValSeq))
    => isFloat(V) andBool allFloats(REST)

  // A sort-safe symbolic generator for arbitrary tails of Float values.  This
  // avoids asking the prover to infer a K subsort from an isFloat predicate.
  syntax FloatSeq ::= ".FloatSeq" | fCons(Float, FloatSeq)
  syntax ValSeq ::= injectFloats(FloatSeq) [function, total]
  rule injectFloats(.FloatSeq) => .ValSeq
  rule injectFloats(fCons(F:Float, REST:FloatSeq))
    => vCons(F, injectFloats(REST))

  // The reference semantics expands a comprehension into an allocation-heavy
  // accumulator loop.  This observational summary preserves exactly the list
  // value that loop builds while abstracting its unreachable intermediate
  // heap objects.  Its left side is the exact comprehension in solution.mpy.
  rule <k>
         ListComp(
           BinOp(
             "/",
             BinOp("-", Name("number"), Name("min_number")),
             BinOp("-", Name("max_number"), Name("min_number"))),
           CompFor(
             Name("number"),
             Name("numbers"),
             Bool(true)))
         => #alloc(list(scaleAcc(.ValSeq, VS, LO, HI)))
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap>
         ...
         MINH:Int |-> cellV(LO:Float)
         MAXH:Int |-> cellV(HI:Float)
         ...
       </heap>
       requires "numbers" in_keys(M)
        andBool {M["numbers"]}:>Val ==K list(VS)
        andBool "min_number" in_keys(M)
        andBool {M["min_number"]}:>Val ==K cellRef(MINH)
        andBool "max_number" in_keys(M)
        andBool {M["max_number"]}:>Val ==K cellRef(MAXH)
       [priority(40)]

  // #observe turns the heap reference returned by the Python function into
  // its list value, keeping the functional claim independent of allocation.
  syntax KItem ::= "#observe"
  rule <k> ref(H:Int) ~> #observe => V ... </k>
       <heap> ... H |-> V:Val ... </heap>

  // Exact translated program followed by a symbolic call.  Keeping this term
  // identical to solution.mpy makes the proof exercise the submitted code.
  syntax KItem ::= #runRescale(ValSeq)
  rule <k> #runRescale(VS:ValSeq)
        => #loadAll(Module(
             ImportFrom("typing", "List")
             FuncDef(
               "rescale_to_unit",
               Params("numbers"),
               CellVars("max_number", "min_number"),
               FreeVars(.ParamNames),
               Assign(
                 Name("min_number"),
                 Call(Name("min"), Name("numbers")))
               Assign(
                 Name("max_number"),
                 Call(Name("max"), Name("numbers")))
               Return(
                 ListComp(
                   BinOp(
                     "/",
                     BinOp("-", Name("number"), Name("min_number")),
                     BinOp("-", Name("max_number"), Name("min_number"))),
                   CompFor(
                     Name("number"),
                     Name("numbers"),
                     Bool(true)))))))
           ~> Call(Name("rescale_to_unit"), list(VS))
           ~> #observe
           ...
       </k>
endmodule
