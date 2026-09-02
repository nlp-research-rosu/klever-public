requires "reference-semantics/semantics.k"

module SPECIALFILTER-VERIFICATION-SYNTAX
  imports MPY

  // The exact function body emitted in solution.mpy.
  syntax Stmts ::= "#specialElementBody" [macro]
  rule #specialElementBody =>
    If(Compare(Name("num"), CmpOp(">", Int(100))),
      Assign(Name("digits"), Call(Name("str"), Name("num")))
      If(BoolOp("and",
          Compare(Subscript(Name("digits"), Int(0)),
                  CmpOp("in", Str("13579"))),
          Compare(Subscript(Name("digits"), UnaryOp("-", Int(1))),
                  CmpOp("in", Str("13579")))),
        AugAssign(Name("count"), "+", Int(1)),
        .Stmts),
      .Stmts)

  syntax Stmts ::= "#specialFunctionBody" [macro]
  rule #specialFunctionBody =>
    Assign(Name("count"), Int(0))
    Assign(Name("num"), Int(0))
    Assign(Name("digits"), Str(""))
    For(Name("num"), Name("nums"), #specialElementBody)
    Return(Name("count"))

  syntax Module ::= "#specialModule" [macro]
  rule #specialModule =>
    Module(FuncDef("specialFilter", Params("nums"), #specialFunctionBody))

  // The Haskell backend cannot symbolically evaluate K's Int2String hook.
  // Give that exact reference term a total symbolic name, together with total
  // names for its length and positional projection.  Both the program and the
  // contract below reduce through these same equations.
  syntax IntSeq ::= decimalCodes(Int)
    [function, total, symbol(decimalCodes), no-evaluators]
  syntax Int ::= decimalLength(Int)
    [function, total, symbol(decimalLength), no-evaluators]
  syntax Int ::= decimalCodeAt(Int, Int)
    [function, total, symbol(decimalCodeAt), no-evaluators]

  rule strToCodes(Int2String(N:Int)) => decimalCodes(N)
    [simplification]
  rule isLen(decimalCodes(N:Int)) => decimalLength(N)
    [simplification]
  rule intSeqAt(decimalCodes(N:Int), I:Int) => decimalCodeAt(N, I)
    [simplification]

  // str(int) in the reference semantics is the standard decimal rendering.
  syntax Str ::= decimalString(Int) [function, total]
  rule decimalString(N:Int) => str(strToCodes(Int2String(N)))

  // These are exactly the two one-character membership tests executed by the
  // program after num > 10 has established a positive, multi-digit integer.
  syntax Bool ::= hasOddEndDigits(Int) [function, total]
  rule hasOddEndDigits(N:Int) =>
    strContains(
      iCons(intSeqAt(strToCodes(Int2String(N)), 0), .IntSeq),
      strToCodes("13579"))
    andBool
    strContains(
      iCons(intSeqAt(strToCodes(Int2String(N)),
                     -1 +Int isLen(strToCodes(Int2String(N)))),
            .IntSeq),
      strToCodes("13579"))

  syntax Int ::= boolAsInt(Bool) [function, total]
  rule boolAsInt(true)  => 1
  rule boolAsInt(false) => 0

  // Mathematical contribution of one input element.
  syntax Int ::= specialBit(Int) [function, total]
  rule specialBit(N:Int) =>
    #if N >Int 10
    #then boolAsInt(hasOddEndDigits(N))
    #else 0
    #fi

  // A proof-only, typed representation of an arbitrary finite Python list of
  // integers.  Its two iterator rules are the base/cons cases of MPY-LIST,
  // while retaining the Int sort of a symbolic head.
  syntax ValSeq ::= intVals(IntSeq)
  rule <k> #iterNext(list(intVals(.IntSeq)))
        => #iterDone ... </k>
  rule <k> #iterNext(list(intVals(iCons(N:Int, REST:IntSeq))))
        => #iterYield(N, list(intVals(REST))) ... </k>

  // Contract result over the corresponding integer sequence.
  syntax Int ::= specialCount(IntSeq) [function, total]
  rule specialCount(.IntSeq) => 0
  rule specialCount(iCons(N:Int, REST:IntSeq)) =>
    specialBit(N) +Int specialCount(REST)

  syntax Int ::= finalNum(Int, IntSeq) [function, total]
  rule finalNum(OLD:Int, .IntSeq) => OLD
  rule finalNum(_:Int, iCons(N:Int, REST:IntSeq)) =>
    finalNum(N, REST)

  syntax Str ::= finalDigits(Str, IntSeq) [function, total]
  rule finalDigits(OLD:Str, .IntSeq) => OLD
  rule finalDigits(OLD:Str, iCons(N:Int, REST:IntSeq)) =>
    finalDigits(
      #if N >Int 10 #then decimalString(N) #else OLD #fi,
      REST)
endmodule

// This module contains no loop summary: its claim is proved directly from MPY.
module SPECIALFILTER-VERIFICATION-LOOP
  imports SPECIALFILTER-VERIFICATION-SYNTAX
endmodule

// The summary below is the exact reachability claim proved separately by the
// SPECIALFILTER-LOOP-SPEC command.  It is then available as a derived rule for
// the end-to-end source-level claim.
module SPECIALFILTER-VERIFICATION
  imports SPECIALFILTER-VERIFICATION-SYNTAX

  rule
    <k> #loop(list(intVals(NS:IntSeq)), Name("num"), #specialElementBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL:IntSeq))
        "count"  |-> C:Int
        "num"    |-> OLDNUM:Int
        "digits" |-> OLDDIGITS:Str,
        parent(0))
      0  |-> scope(GLOBAL:Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
      =>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL))
        "count"  |-> C +Int specialCount(NS)
        "num"    |-> finalNum(OLDNUM, NS)
        "digits" |-> finalDigits(OLDDIGITS, NS),
        parent(0))
      0  |-> scope(GLOBAL, parent(-1))
      -1 |-> scope(BUILTINMAP, root)
    </scopes>
    requires notBool ("str" in_keys(GLOBAL))
      andBool "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
    [priority(40)]
endmodule
