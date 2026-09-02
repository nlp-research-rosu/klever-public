requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax Bool ::= numericVals(ValSeq) [function, total]
                | definedProjectInt(Val) [function, total]
  syntax Val ::= lastNumber(ValSeq, Val) [function, total]
  syntax Int ::= dtd(ValSeq) [function, total]
               | oddIntSquare(Int) [function, total]
               | projectIntTotal(Val)
                   [function, total, symbol(projectIntTotal), no-evaluators]

  // Exact source-term abbreviations.  These expand at kompile time and do not
  // add execution rules.
  syntax Stmts ::= "dtdLoopBody" [macro]
                 | "dtdBody" [macro]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // Exact fixed-model form of the prompt's list-of-numbers domain.
  rule numericVals(.ValSeq) => true
  rule numericVals(vCons(V:Val, VS:ValSeq))
    => (isInt(V) orBool isFloat(V)) andBool numericVals(VS)

  // Mathematical summary of the arbitrary remaining numeric suffix.
  rule dtd(.ValSeq) => 0
  rule dtd(vCons(I:Int, VS:ValSeq))
    => oddIntSquare(I) +Int dtd(VS)
  rule dtd(vCons(_F:Float, VS:ValSeq)) => dtd(VS)
  rule dtd(vCons(_V:Val, VS:ValSeq)) => dtd(VS) [owise]
  rule dtd(vCons(V:Val, VS:ValSeq))
    => oddIntSquare(projectIntTotal(V)) +Int dtd(VS)
    requires isInt(V)
    [simplification]
  rule dtd(vCons(V:Val, VS:ValSeq)) => dtd(VS)
    requires isFloat(V)
    [simplification]

  rule oddIntSquare(I:Int)
    => #if I >Int 0 andBool pyMod(I, 2) ==Int 1
       #then I *Int I
       #else 0
       #fi

  // Exact final loop-target value.  It is local and later deallocated, but
  // retaining it makes the circularity describe the entire function scope.
  rule lastNumber(.ValSeq, OLD:Val) => OLD
  rule lastNumber(vCons(V:Val, VS:ValSeq), _OLD:Val)
    => lastNumber(VS, V)

  // Guarded dynamic-to-static refinement.  These equations are exact twins of
  // isIntV and the corresponding fixed MPY-INT dispatch equations.
  rule definedProjectInt(V:Val) => isInt(V)
  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]
  rule isIntV(V:Val) => isInt(V) [simplification]
  rule applyCmp(">", V:Val, I:Int)
    => projectIntTotal(V) >Int I
    requires isInt(V)
    [simplification]
  rule applyBin("%", V:Val, I:Int)
    => pyMod(projectIntTotal(V), I)
    requires isInt(V)
    [simplification]
  rule applyBin("*", V1:Val, V2:Val)
    => projectIntTotal(V1) *Int projectIntTotal(V2)
    requires isInt(V1) andBool isInt(V2)
    [simplification]

  rule dtdLoopBody
    => If(Call(Name("isinstance"),
               (Name("number"), Name("int"), .Exprs)),
         If(Compare(Name("number"), CmpOp(">", Int(0))),
           If(Compare(BinOp("%", Name("number"), Int(2)),
                      CmpOp("==", Int(1))),
             AugAssign(Name("result"), "+",
                       BinOp("*", Name("number"), Name("number"))),
             .Stmts),
           .Stmts),
         .Stmts)

  rule dtdBody
    => Assign(Name("result"), Int(0))
       Assign(Name("number"), Int(0))
       For(Name("number"), Name("lst"), dtdLoopBody)
       Return(Name("result"))
endmodule
