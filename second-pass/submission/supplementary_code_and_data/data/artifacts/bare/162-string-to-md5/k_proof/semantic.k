module MPY-SYNTAX
  imports DOMAINS
  imports BYTES

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt  ::= "Import" "(" String ")"
                 | "FuncDef" "(" String "," Params "," Stmts ")"
                 | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "NoneVal"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "IfExp" "(" Expr "," Expr "," Expr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," ")"
                | "Call" "(" Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX

  syntax PyValue ::= "pyNone"
                   | "pyBool" "(" Bool ")"
                   | "pyString" "(" String ")"
                   | "pyBytes" "(" Bytes ")"
                   | "pyModule" "(" String ")"
                   | "pyBuiltin" "(" String ")"
                   | "pyMethod" "(" String "," PyValue ")"

  syntax Function ::= "fn" "(" String "," Stmts ")"
  syntax Result ::= "noResult" | PyValue

  syntax KItem ::= "#load" "(" Program ")"
                 | "#loadStmts" "(" Stmts ")"
                 | "#start"
                 | "#invoke" "(" String "," PyValue ")"
                 | "#functionEnd"
                 | "#eval" "(" Expr ")"
                 | "#compareLeft" "(" String "," Expr ")"
                 | "#compareRight" "(" String "," PyValue ")"
                 | "#ifExp" "(" Expr "," Expr ")"
                 | "#attribute" "(" String ")"
                 | "#call0"
                 | "#call1" "(" Expr ")"
                 | "#apply1" "(" PyValue ")"

  configuration
    <py>
      <k> #load($PGM:Program) </k>
      <input> $TEXT:String </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  // Module loading records function syntax without executing its body.
  rule <k> #load(Module(SS)) => #loadStmts(SS) ~> #start ... </k>
  rule <k> #loadStmts(.Stmts) => .K ... </k>
  rule <k> #loadStmts(Import(_) REST) => #loadStmts(REST) ... </k>
  rule <k> #loadStmts(FuncDef(F, Params(P), BODY) REST)
        => #loadStmts(REST) ... </k>
       <functions> FS => FS [ F <- fn(P, BODY) ] </functions>

  // The configured input is passed to the HumanEval entry point.
  rule <k> #start => #invoke("string_to_md5", pyString(S)) ... </k>
       <input> S </input>

  rule <k> #invoke(F, V) => BODY ~> #functionEnd ... </k>
       <functions> F |-> fn(P, BODY) </functions>
       <env> _ => P |-> V </env>

  rule <k> (Return(E) _REST) ~> #functionEnd
        => #eval(E) ~> #functionEnd ... </k>

  rule <k> V:PyValue ~> #functionEnd => .K ... </k>
       <result> _ => V </result>

  // Expression evaluation is explicit: the AST translator performs no
  // desugaring and each constructor gets its meaning here.
  rule <k> #eval(NoneVal) => pyNone ... </k>
  rule <k> #eval(Str(S)) => pyString(S) ... </k>
  rule <k> #eval(Name("hashlib")) => pyModule("hashlib") ... </k>
  rule <k> #eval(Name(N)) => V ... </k>
       <env> N |-> V </env>

  rule <k> #eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => #eval(LEFT) ~> #compareLeft(OP, RIGHT) ... </k>
  rule <k> V:PyValue ~> #compareLeft(OP, RIGHT)
        => #eval(RIGHT) ~> #compareRight(OP, V) ... </k>
  rule <k> pyString(S2) ~> #compareRight("==", pyString(S1))
        => pyBool(S1 ==String S2) ... </k>

  rule <k> #eval(IfExp(TEST, YES, NO))
        => #eval(TEST) ~> #ifExp(YES, NO) ... </k>
  rule <k> pyBool(true) ~> #ifExp(YES, _NO) => #eval(YES) ... </k>
  rule <k> pyBool(false) ~> #ifExp(_YES, NO) => #eval(NO) ... </k>

  rule <k> #eval(Attribute(RECEIVER, ATTR))
        => #eval(RECEIVER) ~> #attribute(ATTR) ... </k>
  rule <k> pyModule("hashlib") ~> #attribute("md5")
        => pyBuiltin("hashlib.md5") ... </k>
  rule <k> pyString(S) ~> #attribute("encode")
        => pyMethod("str.encode", pyString(S)) ... </k>
  rule <k> pyBytes(B) ~> #attribute("hexdigest")
        => pyMethod("md5.hexdigest", pyBytes(B)) ... </k>

  rule <k> #eval(Call(F, )) => #eval(F) ~> #call0 ... </k>
  rule <k> FUN:PyValue ~> #call0 => #apply0(FUN) ... </k>
  syntax KItem ::= "#apply0" "(" PyValue ")"
  rule <k> #apply0(pyMethod("str.encode", pyString(S)))
        => pyBytes(utf8Bytes(S)) ... </k>
  rule <k> #apply0(pyMethod("md5.hexdigest", pyBytes(B)))
        => pyString(md5Bytes(B)) ... </k>

  rule <k> #eval(Call(F, ARG))
        => #eval(F) ~> #call1(ARG) ... </k>
  rule <k> FUN:PyValue ~> #call1(ARG)
        => #eval(ARG) ~> #apply1(FUN) ... </k>
  rule <k> pyBytes(B) ~> #apply1(pyBuiltin("hashlib.md5"))
        => pyBytes(B) ... </k>

  // -----------------------------------------------------------------------
  // A self-contained RFC 1321 MD5 implementation over K's byte primitives.
  // Python's str.encode() defaults to UTF-8, captured by the rule above.
  // -----------------------------------------------------------------------

  syntax String ::= "md5String" "(" String ")" [function]
  syntax String ::= "md5Bytes" "(" Bytes ")" [function]
  syntax Bytes ::= "utf8Bytes" "(" String ")" [function]
                 | "utf8CodePoint" "(" Int ")" [function]
  syntax Bytes ::= "md5Pad" "(" Bytes ")" [function]
  syntax Md5State ::= "md5State" "(" Int "," Int "," Int "," Int ")"
  syntax Md5State ::= "md5Blocks" "(" Bytes "," Int "," Md5State ")" [function]
  syntax Md5State ::= "md5Rounds"
      "(" Bytes "," Int "," Int "," Md5State "," Md5State ")" [function]
  syntax Md5State ::= "md5AddState" "(" Md5State "," Md5State ")" [function]
  syntax String ::= "md5StateHex" "(" Md5State ")" [function]
                  | "hexWordLE" "(" Int ")" [function]
                  | "hexByte" "(" Int ")" [function]
                  | "hexNibble" "(" Int ")" [function]
  syntax Int ::= "md5F" "(" Int "," Int "," Int "," Int ")" [function]
               | "md5G" "(" Int ")" [function]
               | "md5Shift" "(" Int ")" [function]
               | "md5K" "(" Int ")" [function]
               | "md5Word" "(" Bytes "," Int "," Int ")" [function]
               | "add32" "(" Int "," Int ")" [function]
               | "add32" "(" Int "," Int "," Int "," Int ")" [function]
               | "rotl32" "(" Int "," Int ")" [function]

  rule md5String(S) => md5Bytes(utf8Bytes(S))
  rule utf8Bytes("") => .Bytes [simplification]
  rule utf8Bytes(S) =>
    utf8CodePoint(ordChar(substrString(S, 0, 1)))
    +Bytes utf8Bytes(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
    [concrete(S), simplification]

  rule utf8CodePoint(C) => Int2Bytes(1, C, BE)
    requires C >=Int 0 andBool C <=Int 127
  rule utf8CodePoint(C) =>
    Int2Bytes(1, 192 |Int (C >>Int 6), BE)
    +Bytes Int2Bytes(1, 128 |Int (C &Int 63), BE)
    requires C >=Int 128 andBool C <=Int 2047
  rule utf8CodePoint(C) =>
    Int2Bytes(1, 224 |Int (C >>Int 12), BE)
    +Bytes Int2Bytes(1, 128 |Int ((C >>Int 6) &Int 63), BE)
    +Bytes Int2Bytes(1, 128 |Int (C &Int 63), BE)
    requires C >=Int 2048 andBool C <=Int 65535
  rule utf8CodePoint(C) =>
    Int2Bytes(1, 240 |Int (C >>Int 18), BE)
    +Bytes Int2Bytes(1, 128 |Int ((C >>Int 12) &Int 63), BE)
    +Bytes Int2Bytes(1, 128 |Int ((C >>Int 6) &Int 63), BE)
    +Bytes Int2Bytes(1, 128 |Int (C &Int 63), BE)
    requires C >=Int 65536 andBool C <=Int 1114111
  rule md5Bytes(B) =>
    md5StateHex(md5Blocks(
      md5Pad(B),
      0,
      md5State(1732584193, 4023233417, 2562383102, 271733878)))
    [concrete(B), simplification]

  rule md5Pad(B) =>
    padRightBytes(
      B +Bytes b"\x80",
      (((lengthBytes(B) +Int 72) divInt 64) *Int 64) -Int 8,
      0)
    +Bytes Int2Bytes(8, lengthBytes(B) *Int 8, LE)

  rule md5Blocks(P, OFFSET, STATE) => STATE
    requires OFFSET >=Int lengthBytes(P)
  rule md5Blocks(P, OFFSET, STATE) =>
    md5Blocks(P, OFFSET +Int 64, md5Rounds(P, OFFSET, 0, STATE, STATE))
    requires OFFSET <Int lengthBytes(P)

  rule md5Rounds(_P, _OFFSET, 64, STATE, ORIGINAL) =>
    md5AddState(STATE, ORIGINAL)
  rule md5Rounds(P, OFFSET, I, md5State(A, B, C, D), ORIGINAL) =>
    md5Rounds(
      P,
      OFFSET,
      I +Int 1,
      md5State(
        D,
        add32(B,
          rotl32(
            add32(A, md5F(I, B, C, D), md5K(I), md5Word(P, OFFSET, md5G(I))),
            md5Shift(I))),
        B,
        C),
      ORIGINAL)
    requires I >=Int 0 andBool I <Int 64

  rule md5AddState(
      md5State(A, B, C, D),
      md5State(A0, B0, C0, D0)) =>
    md5State(add32(A, A0), add32(B, B0), add32(C, C0), add32(D, D0))

  rule md5StateHex(md5State(A, B, C, D)) =>
    hexWordLE(A) +String hexWordLE(B) +String
    hexWordLE(C) +String hexWordLE(D)

  rule hexWordLE(W) =>
    hexByte(W &Int 255) +String
    hexByte((W >>Int 8) &Int 255) +String
    hexByte((W >>Int 16) &Int 255) +String
    hexByte((W >>Int 24) &Int 255)
  rule hexByte(B) =>
    hexNibble(B divInt 16) +String hexNibble(B modInt 16)
  rule hexNibble(0)  => "0"
  rule hexNibble(1)  => "1"
  rule hexNibble(2)  => "2"
  rule hexNibble(3)  => "3"
  rule hexNibble(4)  => "4"
  rule hexNibble(5)  => "5"
  rule hexNibble(6)  => "6"
  rule hexNibble(7)  => "7"
  rule hexNibble(8)  => "8"
  rule hexNibble(9)  => "9"
  rule hexNibble(10) => "a"
  rule hexNibble(11) => "b"
  rule hexNibble(12) => "c"
  rule hexNibble(13) => "d"
  rule hexNibble(14) => "e"
  rule hexNibble(15) => "f"

  rule md5Word(P, OFFSET, G) =>
    Bytes2Int(
      substrBytes(
        P,
        OFFSET +Int (4 *Int G),
        OFFSET +Int (4 *Int G) +Int 4),
      LE,
      Unsigned)

  rule add32(X, Y) => (X +Int Y) modInt 4294967296
  rule add32(W, X, Y, Z) =>
    (W +Int X +Int Y +Int Z) modInt 4294967296
  rule rotl32(X, S) =>
    ((X <<Int S) |Int (X >>Int (32 -Int S))) &Int 4294967295

  rule md5F(I, B, C, D) => (B &Int C) |Int ((~Int B) &Int D)
    requires I >=Int 0 andBool I <Int 16
  rule md5F(I, B, C, D) => (D &Int B) |Int ((~Int D) &Int C)
    requires I >=Int 16 andBool I <Int 32
  rule md5F(I, B, C, D) => B xorInt C xorInt D
    requires I >=Int 32 andBool I <Int 48
  rule md5F(I, B, C, D) => C xorInt (B |Int (~Int D))
    requires I >=Int 48 andBool I <Int 64

  rule md5G(I) => I requires I >=Int 0 andBool I <Int 16
  rule md5G(I) => (5 *Int I +Int 1) modInt 16
    requires I >=Int 16 andBool I <Int 32
  rule md5G(I) => (3 *Int I +Int 5) modInt 16
    requires I >=Int 32 andBool I <Int 48
  rule md5G(I) => (7 *Int I) modInt 16
    requires I >=Int 48 andBool I <Int 64

  rule md5Shift(I) => 7  requires I >=Int 0  andBool I <Int 16 andBool I modInt 4 ==Int 0
  rule md5Shift(I) => 12 requires I >=Int 0  andBool I <Int 16 andBool I modInt 4 ==Int 1
  rule md5Shift(I) => 17 requires I >=Int 0  andBool I <Int 16 andBool I modInt 4 ==Int 2
  rule md5Shift(I) => 22 requires I >=Int 0  andBool I <Int 16 andBool I modInt 4 ==Int 3
  rule md5Shift(I) => 5  requires I >=Int 16 andBool I <Int 32 andBool I modInt 4 ==Int 0
  rule md5Shift(I) => 9  requires I >=Int 16 andBool I <Int 32 andBool I modInt 4 ==Int 1
  rule md5Shift(I) => 14 requires I >=Int 16 andBool I <Int 32 andBool I modInt 4 ==Int 2
  rule md5Shift(I) => 20 requires I >=Int 16 andBool I <Int 32 andBool I modInt 4 ==Int 3
  rule md5Shift(I) => 4  requires I >=Int 32 andBool I <Int 48 andBool I modInt 4 ==Int 0
  rule md5Shift(I) => 11 requires I >=Int 32 andBool I <Int 48 andBool I modInt 4 ==Int 1
  rule md5Shift(I) => 16 requires I >=Int 32 andBool I <Int 48 andBool I modInt 4 ==Int 2
  rule md5Shift(I) => 23 requires I >=Int 32 andBool I <Int 48 andBool I modInt 4 ==Int 3
  rule md5Shift(I) => 6  requires I >=Int 48 andBool I <Int 64 andBool I modInt 4 ==Int 0
  rule md5Shift(I) => 10 requires I >=Int 48 andBool I <Int 64 andBool I modInt 4 ==Int 1
  rule md5Shift(I) => 15 requires I >=Int 48 andBool I <Int 64 andBool I modInt 4 ==Int 2
  rule md5Shift(I) => 21 requires I >=Int 48 andBool I <Int 64 andBool I modInt 4 ==Int 3

  rule md5K(0)  => 3614090360
  rule md5K(1)  => 3905402710
  rule md5K(2)  => 606105819
  rule md5K(3)  => 3250441966
  rule md5K(4)  => 4118548399
  rule md5K(5)  => 1200080426
  rule md5K(6)  => 2821735955
  rule md5K(7)  => 4249261313
  rule md5K(8)  => 1770035416
  rule md5K(9)  => 2336552879
  rule md5K(10) => 4294925233
  rule md5K(11) => 2304563134
  rule md5K(12) => 1804603682
  rule md5K(13) => 4254626195
  rule md5K(14) => 2792965006
  rule md5K(15) => 1236535329
  rule md5K(16) => 4129170786
  rule md5K(17) => 3225465664
  rule md5K(18) => 643717713
  rule md5K(19) => 3921069994
  rule md5K(20) => 3593408605
  rule md5K(21) => 38016083
  rule md5K(22) => 3634488961
  rule md5K(23) => 3889429448
  rule md5K(24) => 568446438
  rule md5K(25) => 3275163606
  rule md5K(26) => 4107603335
  rule md5K(27) => 1163531501
  rule md5K(28) => 2850285829
  rule md5K(29) => 4243563512
  rule md5K(30) => 1735328473
  rule md5K(31) => 2368359562
  rule md5K(32) => 4294588738
  rule md5K(33) => 2272392833
  rule md5K(34) => 1839030562
  rule md5K(35) => 4259657740
  rule md5K(36) => 2763975236
  rule md5K(37) => 1272893353
  rule md5K(38) => 4139469664
  rule md5K(39) => 3200236656
  rule md5K(40) => 681279174
  rule md5K(41) => 3936430074
  rule md5K(42) => 3572445317
  rule md5K(43) => 76029189
  rule md5K(44) => 3654602809
  rule md5K(45) => 3873151461
  rule md5K(46) => 530742520
  rule md5K(47) => 3299628645
  rule md5K(48) => 4096336452
  rule md5K(49) => 1126891415
  rule md5K(50) => 2878612391
  rule md5K(51) => 4237533241
  rule md5K(52) => 1700485571
  rule md5K(53) => 2399980690
  rule md5K(54) => 4293915773
  rule md5K(55) => 2240044497
  rule md5K(56) => 1873313359
  rule md5K(57) => 4264355552
  rule md5K(58) => 2734768916
  rule md5K(59) => 1309151649
  rule md5K(60) => 4149444226
  rule md5K(61) => 3174756917
  rule md5K(62) => 718787259
  rule md5K(63) => 3951481745
endmodule
