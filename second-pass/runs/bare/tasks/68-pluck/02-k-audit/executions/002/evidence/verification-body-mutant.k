requires "semantic.k"

module VERIFICATION-BODY-MUTANT
  imports SEMANTIC

  // Independent contract over an arbitrary finite integer array.  ID names
  // an unconstrained element oracle, OFFSET is its current position, and
  // LENGTH is the remaining length.  FOUND = 0 means no even value has been
  // seen; otherwise BEST/BESTINDEX retain the smallest value and first index.
  syntax Val ::= "specScanArray" "(" Int "," Int "," Int "," Int "," Int "," Int "," Int ")"
                   [function, total]
               | "specFinish" "(" Int "," Int "," Int ")"
                   [function, total]
               | "specConsiderArray" "(" Int "," Int "," Int "," Int "," Int "," Int "," Int "," Int ")"
                   [function, total]
               | "specEvenArray" "(" Int "," Int "," Int "," Int "," Int "," Int "," Int "," Int ")"
                   [function, total]

  rule specScanArray(_ID, _OFFSET, LENGTH, _INDEX, BEST, BESTINDEX, FOUND)
       => specFinish(BEST, BESTINDEX, FOUND)
       requires LENGTH ==Int 0
  rule specScanArray(ID, OFFSET, LENGTH, INDEX, BEST, BESTINDEX, FOUND)
       => specConsiderArray(arrayAt(ID, OFFSET), ID, OFFSET, LENGTH,
                            INDEX, BEST, BESTINDEX, FOUND)
       requires LENGTH >Int 0

  rule specFinish(_BEST, _BESTINDEX, FOUND) => VList(.Ints)
       requires FOUND ==Int 0
  rule specFinish(BEST, BESTINDEX, FOUND) => VList(BEST, BESTINDEX)
       requires FOUND =/=Int 0

  rule specConsiderArray(HEAD, ID, OFFSET, LENGTH,
                         INDEX, BEST, BESTINDEX, FOUND)
       => specScanArray(ID, OFFSET +Int 1, LENGTH -Int 1,
                        INDEX +Int 1, BEST, BESTINDEX, FOUND)
       requires HEAD modInt 2 =/=Int 0
  rule specConsiderArray(HEAD, ID, OFFSET, LENGTH,
                         INDEX, BEST, BESTINDEX, FOUND)
       => specEvenArray(HEAD, ID, OFFSET, LENGTH,
                        INDEX, BEST, BESTINDEX, FOUND)
       requires HEAD modInt 2 ==Int 0

  rule specEvenArray(HEAD, ID, OFFSET, LENGTH,
                     INDEX, _BEST, _BESTINDEX, FOUND)
       => specScanArray(ID, OFFSET +Int 1, LENGTH -Int 1,
                        INDEX +Int 1, HEAD, INDEX, 1)
       requires FOUND ==Int 0
  rule specEvenArray(HEAD, ID, OFFSET, LENGTH,
                     INDEX, BEST, _BESTINDEX, FOUND)
       => specScanArray(ID, OFFSET +Int 1, LENGTH -Int 1,
                        INDEX +Int 1, HEAD, INDEX, FOUND)
       requires FOUND =/=Int 0 andBool HEAD <Int BEST
  rule specEvenArray(HEAD, ID, OFFSET, LENGTH,
                     INDEX, BEST, BESTINDEX, FOUND)
       => specScanArray(ID, OFFSET +Int 1, LENGTH -Int 1,
                        INDEX +Int 1, BEST, BESTINDEX, FOUND)
       requires FOUND =/=Int 0 andBool HEAD >=Int BEST

  // The abstract result of Python's enumerate/filter/min composition is tied
  // to the same scan contract.  arrayAt is uninterpreted, so this equation
  // makes no assumptions about the array's elements.
  rule minEvenArray(ID, OFFSET, LENGTH)
       => specScanArray(ID, OFFSET, LENGTH, 0, 0, 0, 0)

  // Exact constructor form generated in solution.mpy.
  syntax Stmts ::= "pluckBody" [function, total]
  syntax Program ::= "solutionProgram" [function, total]
  syntax Map ::= "solutionFunctions" [function, total]

  rule pluckBody =>
    Return(Call(
      Name("min"),
      ListComp(
        ListExpr(Name("value"), Name("index")),
        CompFor(
          TupleExpr(Name("index"), Name("value")),
          Call(Name("enumerate"), Name("arr")),
          Compare(
            BinOp("%", Name("value"), Int(2)),
            CmpOp("==", Int(1))))),
      KwArg("default", ListExpr(.Exprs))))

  rule solutionProgram =>
    Module(FuncDef("pluck", Params("arr"), pluckBody))

  rule solutionFunctions =>
    "pluck" |-> fun(Params("arr"), pluckBody)
endmodule
