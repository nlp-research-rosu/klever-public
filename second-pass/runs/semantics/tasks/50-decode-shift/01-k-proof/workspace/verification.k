requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The mathematical character transform implemented by decode_shift.
  syntax Int ::= decodeChar(Int) [function, total]
  rule decodeChar(C:Int) => pyMod(C -Int 5 -Int 97, 26) +Int 97

  // Tail-recursive specification matching the program's left-to-right loop.
  syntax IntSeq ::= decodeAcc(IntSeq, IntSeq) [function, total]
                  | decodeCodes(IntSeq) [function, total]
  rule decodeAcc(ACC:IntSeq, .IntSeq) => ACC
  rule decodeAcc(ACC:IntSeq, iCons(C:Int, CS:IntSeq))
    => decodeAcc(seqConcat(ACC, iCons(decodeChar(C), .IntSeq)), CS)
  rule decodeCodes(CS:IntSeq) => decodeAcc(.IntSeq, CS)

  syntax Val ::= loopLast(Val, IntSeq) [function, total]
  rule loopLast(V:Val, .IntSeq) => V
  rule loopLast(_:Val, iCons(C:Int, CS:IntSeq))
    => loopLast(str(iCons(C, .IntSeq)), CS)

  syntax Int ::= encodeChar(Int) [function, total]
  rule encodeChar(C:Int) => pyMod(C +Int 5 -Int 97, 26) +Int 97

  syntax Bool ::= lowerCodes(IntSeq) [function, total]
  rule lowerCodes(.IntSeq) => true
  rule lowerCodes(iCons(C:Int, CS:IntSeq))
    => (97 <=Int C andBool C <=Int 122) andBool lowerCodes(CS)

  // Macros reproduce the translated decode_shift body from solution.mpy.
  syntax Stmt ::= "decodeStep" [macro]
  rule decodeStep
    => AugAssign(
         Name("result"),
         "+",
         Call(
           Name("chr"),
           BinOp(
             "+",
             BinOp(
               "%",
               BinOp(
                 "-",
                 BinOp("-", Call(Name("ord"), Name("ch")), Int(5)),
                 Call(Name("ord"), Str("a"))),
               Int(26)),
             Call(Name("ord"), Str("a")))))

  syntax Stmts ::= "decodeBody" [macro]
  rule decodeBody
    => Expr(Str(
         "\n    takes as input string encoded with encode_shift function. Returns decoded string.\n    "))
       Assign(Name("result"), Str(""))
       Assign(Name("ch"), Str(""))
       For(Name("ch"), Name("s"), decodeStep)
       Return(Name("result"))

  syntax Val ::= "decodeClosure" [macro]
  rule decodeClosure
    => closureVal(("s", .ParamNames), decodeBody, 0)
endmodule

// This module promotes the independently proved decode-loop claim to a
// high-priority lemma for the top-level function proof.
module VERIFICATION-WITH-LOOP
  imports VERIFICATION

  rule [decode-loop-lemma]:
    <k>
      #loop(str(CS:IntSeq), Name("ch"), decodeStep)
      ~> KONT:K
    =>
      KONT
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(ORIGINAL:IntSeq)
        "result" |-> str(ACC:IntSeq)
        "ch" |-> CH:Val,
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> BUILTINS:Scope
    =>
      1 |-> scope(
        "s" |-> str(ORIGINAL)
        "result" |-> str(decodeAcc(ACC, CS))
        "ch" |-> loopLast(CH, CS),
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires lowerCodes(CS)
    [priority(40)]
endmodule
