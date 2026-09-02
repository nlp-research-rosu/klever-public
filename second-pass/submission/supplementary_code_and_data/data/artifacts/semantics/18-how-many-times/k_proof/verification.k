requires "reference-semantics/semantics.k"

module HOW-MANY-TIMES-VERIFICATION
  imports MPY

  // The exact body emitted in solution.mpy, named so the proof claim can
  // quantify over the surrounding machine state without duplicating the AST.
  syntax Stmts ::= "howManyTimesBody" [macro]
  rule howManyTimesBody
    => If(Compare(Name("substring"), CmpOp("==", Str(""))),
          Return(BinOp("+", Call(Name("len"), Name("string")), Int(1))),
          .Stmts)
       If(Compare(Name("string"), CmpOp("==", Str(""))),
          Return(Int(0)),
          .Stmts)
       Return(
         BinOp(
           "+",
           IfExp(
             Call(Attribute(Name("string"), "startswith"), Name("substring")),
             Int(1),
             Int(0)),
           Call(
             Name("how_many_times"),
             Subscript(Name("string"), Slice(Int(1), NoBound, NoBound)),
             Name("substring"))))
       .Stmts

  // Mathematical contract: count a match at every starting position.  The
  // empty pattern occurs at every boundary, including after the final code.
  syntax Int ::= overlapCount(IntSeq, IntSeq) [function, total]
  rule overlapCount(S:IntSeq, .IntSeq) => isLen(S) +Int 1
  rule overlapCount(.IntSeq, iCons(_:Int, _:IntSeq)) => 0
  rule overlapCount(
         iCons(C:Int, CS:IntSeq),
         iCons(PC:Int, PS:IntSeq))
    => (#if startsWith(iCons(PC, PS), iCons(C, CS))
         #then 1
         #else 0
         #fi)
       +Int overlapCount(CS, iCons(PC, PS))

  // A proof machine for the exact recurrence implemented by the Python body.
  // #overlapEval handles the two guards; #overlapAcc scans a nonempty
  // pattern in tail-recursive form so its invariant can be proved separately.
  syntax KItem ::= #overlapEval(IntSeq, IntSeq)
                 | #overlapAcc(IntSeq, IntSeq, Int)

  rule
    <k> #overlapEval(S:IntSeq, .IntSeq)
      => isLen(S) +Int 1
      ...
    </k>

  rule
    <k> #overlapEval(.IntSeq, iCons(_:Int, _:IntSeq))
      => 0
      ...
    </k>

  rule
    <k>
      #overlapEval(
        iCons(C:Int, CS:IntSeq),
        iCons(PC:Int, PS:IntSeq))
      => #overlapAcc(
           CS,
           iCons(PC, PS),
           #if startsWith(
                 iCons(PC, PS),
                 iCons(C, CS))
             #then 1
             #else 0
             #fi)
      ...
    </k>

  rule
    <k> #overlapAcc(.IntSeq, _:IntSeq, A:Int)
      => A
      ...
    </k>

  rule
    <k>
      #overlapAcc(
        iCons(C:Int, CS:IntSeq),
        iCons(PC:Int, PS:IntSeq),
        A:Int)
      => #overlapAcc(
           CS,
           iCons(PC, PS),
           A +Int
             (#if startsWith(
                    iCons(PC, PS),
                    iCons(C, CS))
                #then 1
                #else 0
                #fi))
      ...
    </k>

  // Verification abstraction: frame administration, fixed-name lookup, and
  // s[1:] are deterministic for this pure closure.  Matching the complete
  // body keeps this bridge syntactically tied to solution.mpy.
  rule
    <k>
      #applyK(
        toCall(
          closureVal(
            ("string", "substring"),
            howManyTimesBody,
            0)),
        (str(S:IntSeq), str(P:IntSeq), .Vals))
      ~> CONT:K
      => #overlapEval(S, P) ~> CONT
    </k>
    [priority(30)]
endmodule
