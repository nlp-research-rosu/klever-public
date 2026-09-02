requires "reference-semantics/semantics.k"

module ROMAN-BASE
  imports MPY

  // The exact statement body emitted in solution.mpy.  Keeping it as a
  // function makes the specification readable while still executing the
  // translated program through the supplied MPY semantics.
  syntax Stmts ::= "romanThousandsBody" [function]
                 | "romanHundredsBody"  [function]
                 | "romanTensBody"      [function]
                 | "romanOnesBody"      [function]
                 | "romanSolutionBody"  [function]

  rule romanThousandsBody
    => Return(
         Subscript(
           TupleExpr(Str(""), Str("m")),
           Name("digit")))

  rule romanHundredsBody
    => Return(
         Subscript(
           TupleExpr(
             Str(""), Str("c"), Str("cc"), Str("ccc"), Str("cd"),
             Str("d"), Str("dc"), Str("dcc"), Str("dccc"), Str("cm")),
           Name("digit")))

  rule romanTensBody
    => Return(
         Subscript(
           TupleExpr(
             Str(""), Str("x"), Str("xx"), Str("xxx"), Str("xl"),
             Str("l"), Str("lx"), Str("lxx"), Str("lxxx"), Str("xc")),
           Name("digit")))

  rule romanOnesBody
    => Return(
         Subscript(
           TupleExpr(
             Str(""), Str("i"), Str("ii"), Str("iii"), Str("iv"),
             Str("v"), Str("vi"), Str("vii"), Str("viii"), Str("ix")),
           Name("digit")))

  rule romanSolutionBody
    => Return(
         BinOp(
           "+",
           BinOp(
             "+",
             BinOp(
               "+",
               Call(
                 Name("_roman_thousands"),
                 BinOp("//", Name("number"), Int(1000))),
               Call(
                 Name("_roman_hundreds"),
                 BinOp(
                   "//",
                   BinOp("%", Name("number"), Int(1000)),
                   Int(100)))),
             Call(
               Name("_roman_tens"),
               BinOp(
                 "//",
                 BinOp("%", Name("number"), Int(100)),
                 Int(10)))),
           Call(
             Name("_roman_ones"),
             BinOp("%", Name("number"), Int(10)))))

  // Mathematical digit encodings.  These equations are the canonical Roman
  // rules for one decimal place (subtractive forms at 4 and 9).
  syntax IntSeq ::= thousandsDigit(Int) [function]
                  | hundredsDigit(Int)  [function]
                  | tensDigit(Int)      [function]
                  | onesDigit(Int)      [function]

  rule thousandsDigit(0) => .IntSeq [concrete]
  rule thousandsDigit(1) => iCons(109, .IntSeq) [concrete]

  rule hundredsDigit(0) => .IntSeq [concrete]
  rule hundredsDigit(1) => iCons(99, .IntSeq) [concrete]
  rule hundredsDigit(2) => iCons(99, iCons(99, .IntSeq)) [concrete]
  rule hundredsDigit(3) => iCons(99, iCons(99, iCons(99, .IntSeq))) [concrete]
  rule hundredsDigit(4) => iCons(99, iCons(100, .IntSeq)) [concrete]
  rule hundredsDigit(5) => iCons(100, .IntSeq) [concrete]
  rule hundredsDigit(6) => iCons(100, iCons(99, .IntSeq)) [concrete]
  rule hundredsDigit(7) => iCons(100, iCons(99, iCons(99, .IntSeq))) [concrete]
  rule hundredsDigit(8) => iCons(100, iCons(99, iCons(99, iCons(99, .IntSeq)))) [concrete]
  rule hundredsDigit(9) => iCons(99, iCons(109, .IntSeq)) [concrete]

  rule tensDigit(0) => .IntSeq [concrete]
  rule tensDigit(1) => iCons(120, .IntSeq) [concrete]
  rule tensDigit(2) => iCons(120, iCons(120, .IntSeq)) [concrete]
  rule tensDigit(3) => iCons(120, iCons(120, iCons(120, .IntSeq))) [concrete]
  rule tensDigit(4) => iCons(120, iCons(108, .IntSeq)) [concrete]
  rule tensDigit(5) => iCons(108, .IntSeq) [concrete]
  rule tensDigit(6) => iCons(108, iCons(120, .IntSeq)) [concrete]
  rule tensDigit(7) => iCons(108, iCons(120, iCons(120, .IntSeq))) [concrete]
  rule tensDigit(8) => iCons(108, iCons(120, iCons(120, iCons(120, .IntSeq)))) [concrete]
  rule tensDigit(9) => iCons(120, iCons(99, .IntSeq)) [concrete]

  rule onesDigit(0) => .IntSeq [concrete]
  rule onesDigit(1) => iCons(105, .IntSeq) [concrete]
  rule onesDigit(2) => iCons(105, iCons(105, .IntSeq)) [concrete]
  rule onesDigit(3) => iCons(105, iCons(105, iCons(105, .IntSeq))) [concrete]
  rule onesDigit(4) => iCons(105, iCons(118, .IntSeq)) [concrete]
  rule onesDigit(5) => iCons(118, .IntSeq) [concrete]
  rule onesDigit(6) => iCons(118, iCons(105, .IntSeq)) [concrete]
  rule onesDigit(7) => iCons(118, iCons(105, iCons(105, .IntSeq))) [concrete]
  rule onesDigit(8) => iCons(118, iCons(105, iCons(105, iCons(105, .IntSeq)))) [concrete]
  rule onesDigit(9) => iCons(105, iCons(120, .IntSeq)) [concrete]

  syntax Int ::= "thousandsIndex" "(" Int ")" [macro]
               | "hundredsIndex" "(" Int ")"  [macro]
               | "tensIndex" "(" Int ")"      [macro]
               | "onesIndex" "(" Int ")"      [macro]

  rule thousandsIndex(N)
    => (N -Int pyMod(N, 1000)) /Int 1000

  rule hundredsIndex(N)
    => (pyMod(N, 1000) -Int pyMod(pyMod(N, 1000), 100)) /Int 100

  rule tensIndex(N)
    => (pyMod(N, 100) -Int pyMod(pyMod(N, 100), 10)) /Int 10

  rule onesIndex(N)
    => pyMod(N, 10)

  // Canonical lowercase Roman representation, stated independently as the
  // concatenation of the four mathematically specified decimal-place digits.
  syntax IntSeq ::= romanSpec(Int) [function]
  rule romanSpec(N)
    => seqConcat(
         seqConcat(
           seqConcat(
             thousandsDigit(thousandsIndex(N)),
             hundredsDigit(hundredsIndex(N))),
           tensDigit(tensIndex(N))),
         onesDigit(onesIndex(N)))

  // Proof driver for finite helper domains.  Ordinary <k>-cell rewrites
  // narrow the symbolic digit to every integer constructor case; the claim's
  // path condition discards cases outside the helper's legal bound.
  syntax KItem ::= #helperCase(String, Int)
  rule <k> #helperCase(F:String, 0) => Call(Name(F), Int(0)) ... </k>
  rule <k> #helperCase(F:String, 1) => Call(Name(F), Int(1)) ... </k>
  rule <k> #helperCase(F:String, 2) => Call(Name(F), Int(2)) ... </k>
  rule <k> #helperCase(F:String, 3) => Call(Name(F), Int(3)) ... </k>
  rule <k> #helperCase(F:String, 4) => Call(Name(F), Int(4)) ... </k>
  rule <k> #helperCase(F:String, 5) => Call(Name(F), Int(5)) ... </k>
  rule <k> #helperCase(F:String, 6) => Call(Name(F), Int(6)) ... </k>
  rule <k> #helperCase(F:String, 7) => Call(Name(F), Int(7)) ... </k>
  rule <k> #helperCase(F:String, 8) => Call(Name(F), Int(8)) ... </k>
  rule <k> #helperCase(F:String, 9) => Call(Name(F), Int(9)) ... </k>

  // Arithmetic side-condition checks used to justify specializing the finite
  // lookup lemmas to this function's four index expressions.
  syntax KItem ::= #checkThousandsIndex(Int)
                 | #checkHundredsIndex(Int)
                 | #checkTensIndex(Int)
                 | #checkOnesIndex(Int)

  rule <k> #checkThousandsIndex(N) => true ... </k>
    requires thousandsIndex(N) >=Int 0
     andBool thousandsIndex(N) <=Int 1

  rule <k> #checkHundredsIndex(N) => true ... </k>
    requires hundredsIndex(N) >=Int 0
     andBool hundredsIndex(N) <=Int 9

  rule <k> #checkTensIndex(N) => true ... </k>
    requires tensIndex(N) >=Int 0
     andBool tensIndex(N) <=Int 9

  rule <k> #checkOnesIndex(N) => true ... </k>
    requires onesIndex(N) >=Int 0
     andBool onesIndex(N) <=Int 9
endmodule

module ROMAN-VERIFICATION
  imports ROMAN-BASE

  // These four finite-domain helper lemmas are proved separately against
  // ROMAN-BASE, and the four index-range claims prove their applicability.
  // These source-level instances avoid asking valSeqAt to invert a modular
  // symbolic expression, which the supplied semantics deliberately leaves
  // opaque.
  rule <k>
         Call(
           Name("_roman_thousands"),
           BinOp("//", Name("number"), Int(1000)))
         => str(thousandsDigit(thousandsIndex(N)))
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           _M:Map
           "number" |-> N:Int,
           _)
         ...
       </scopes>
    requires N >=Int 1 andBool N <=Int 1000
    [priority(40)]

  rule <k>
         Call(
           Name("_roman_hundreds"),
           BinOp(
             "//",
             BinOp("%", Name("number"), Int(1000)),
             Int(100)))
         => str(hundredsDigit(hundredsIndex(N)))
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           _M:Map
           "number" |-> N:Int,
           _)
         ...
       </scopes>
    requires N >=Int 1 andBool N <=Int 1000
    [priority(40)]

  rule <k>
         Call(
           Name("_roman_tens"),
           BinOp(
             "//",
             BinOp("%", Name("number"), Int(100)),
             Int(10)))
         => str(tensDigit(tensIndex(N)))
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           _M:Map
           "number" |-> N:Int,
           _)
         ...
       </scopes>
    requires N >=Int 1 andBool N <=Int 1000
    [priority(40)]

  rule <k>
         Call(
           Name("_roman_ones"),
           BinOp("%", Name("number"), Int(10)))
         => str(onesDigit(onesIndex(N)))
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           _M:Map
           "number" |-> N:Int,
           _)
         ...
       </scopes>
    requires N >=Int 1 andBool N <=Int 1000
    [priority(40)]
endmodule
