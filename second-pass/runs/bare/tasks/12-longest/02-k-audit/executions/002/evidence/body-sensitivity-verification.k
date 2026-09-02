requires "semantic.k"

module VERIFICATION-BODY-MUTANT
  imports MPY-SEMANTICS

  // These macros are an exact K rendering of solution.mpy.  Naming the
  // repeated loop body also makes the inductive proof claim readable.
  syntax Stmts ::= "longestLoopBody" [macro]
  rule longestLoopBody =>
    If(Compare(
         Call(Name("len"), Name("string")),
         CmpOp(">", Call(Name("len"), Name("result")))),
       .Stmts,
       .Stmts)

  syntax Stmt ::= "longestProgram" [macro]
  rule longestProgram =>
    Module(
      ImportFrom("typing", "List", "Optional")
      FuncDef("longest", Params("strings"),
        If(Compare(Call(Name("len"), Name("strings")),
                   CmpOp("==", Int(0))),
          Return(NoneVal),
          .Stmts)
        Assign(Name("result"), Subscript(Name("strings"), Int(0)))
        For(Name("string"), Name("strings"), longestLoopBody)
        Return(Name("result"))))

  // Convert a mathematical list of K strings to the corresponding runtime
  // list.  Restricting the input this way formalizes the List[str] precondition.
  syntax Value ::= stringList(Strings) [function]
  syntax Values ::= stringValues(Strings) [function]
  rule stringList(SS) => listVal(stringValues(SS))
  rule stringValues(.Strings) => .Values
  rule stringValues(S:String, SS:Strings)
       => strVal(S), stringValues(SS)

  // Independent contract model: keep the old string on equal lengths, hence
  // this returns the first string among all maximum-length strings.
  syntax Value ::= expectedLongest(Strings) [function]
  syntax String ::= firstLongest(String, Strings) [function]

  rule expectedLongest(.Strings) => noneVal
  rule expectedLongest(S:String, SS:Strings)
       => strVal(firstLongest(S, SS))

  rule firstLongest(BEST, .Strings) => BEST
  rule firstLongest(BEST, S:String, SS:Strings)
       => firstLongest(S, SS)
       requires lengthString(S) >Int lengthString(BEST)
  rule firstLongest(BEST, S:String, SS:Strings)
       => firstLongest(BEST, SS)
       requires lengthString(S) <=Int lengthString(BEST)

  // Symbolic finite sequences let kprove induct over an arbitrary input
  // length. stringAt(ID, I) denotes the unconstrained string at index I.
  syntax String ::= stringAt(String, Int) [function, total]
  syntax Value ::= seqVal(String, Int, Int)

  rule isEmpty(seqVal(_, _, N)) => boolVal(true)
       requires N ==Int 0
  rule isEmpty(seqVal(_, _, N)) => boolVal(false)
       requires N >Int 0
  rule head(seqVal(ID, I, N)) => strVal(stringAt(ID, I))
       requires N >Int 0

  rule forValues(_, seqVal(_, _, N), _) => .
       requires N ==Int 0
  rule <k> forValues(X, seqVal(ID, I, N), BODY)
            => exec(BODY)
               ~> forValues(X, seqVal(ID, I +Int 1, N -Int 1), BODY) ... </k>
       <env> (X |-> _OLD REST)
               => (X |-> strVal(stringAt(ID, I)) REST) </env>
       requires N >Int 0

  // Mathematical fold used as the loop invariant and postcondition.
  syntax String ::= firstInSeq(String, String, Int, Int) [function]
  rule firstInSeq(BEST, _ID, _I, N) => BEST
       requires N ==Int 0
  rule firstInSeq(BEST, ID, I, N)
       => firstInSeq(stringAt(ID, I), ID, I +Int 1, N -Int 1)
       requires N >Int 0
        andBool lengthString(stringAt(ID, I)) >Int lengthString(BEST)
  rule firstInSeq(BEST, ID, I, N)
       => firstInSeq(BEST, ID, I +Int 1, N -Int 1)
       requires N >Int 0
        andBool lengthString(stringAt(ID, I)) <=Int lengthString(BEST)
endmodule
