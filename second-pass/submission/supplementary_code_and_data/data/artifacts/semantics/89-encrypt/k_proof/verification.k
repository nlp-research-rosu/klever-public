requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The mathematical specification: rotate every character code by four
  // positions in the 26-letter lowercase alphabet.
  syntax Int ::= encryptCode(Int) [function, total]
  rule encryptCode(C:Int) => pyMod(C -Int 97 +Int 4, 26) +Int 97

  syntax IntSeq ::= encryptCodes(IntSeq) [function, total]
                    | encryptAcc(IntSeq, IntSeq) [function, total]
  rule encryptCodes(CS:IntSeq) => encryptAcc(.IntSeq, CS)
  rule encryptAcc(A:IntSeq, .IntSeq) => A
  rule encryptAcc(A:IntSeq, iCons(C:Int, CS:IntSeq))
    => encryptAcc(
         seqConcat(A, iCons(encryptCode(C), .IntSeq)),
         CS)

  // The for-loop variable remains bound after a Python loop.  Tracking it in
  // the invariant makes the scope post-state exact, including the empty case.
  syntax Str ::= lastChar(IntSeq, Str) [function, total]
  rule lastChar(.IntSeq, OLD:Str) => OLD
  rule lastChar(iCons(C:Int, CS:IntSeq), _:Str)
    => lastChar(CS, str(iCons(C, .IntSeq)))

  syntax Stmts ::= "encryptLoopBody" [macro]
  rule encryptLoopBody
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
                 "+",
                 BinOp("-", Call(Name("ord"), Name("char")), Int(97)),
                 Int(4)),
               Int(26)),
             Int(97))))
       .Stmts

  syntax Stmts ::= "encryptFunctionBody" [macro]
  rule encryptFunctionBody
    => Assign(Name("result"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("s"), encryptLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Val ::= "encryptClosure" [macro]
  rule encryptClosure
    => closureVal("s", encryptFunctionBody, 0)
endmodule

// This module adds the loop summary only after the identical reachability
// claim in LOOP-SPEC has been proved against VERIFICATION (which imports only
// MPY).  FUNCTION-SPEC then composes that established lemma with real function
// lookup, argument binding, execution, return, and frame teardown.
module VERIFICATION-WITH-LOOP
  imports VERIFICATION

  rule <k>
         #loop(str(CS:IntSeq), Name("char"), encryptLoopBody)
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         ...
         (1 |-> scope(
            ("result" |-> str(A:IntSeq))
            ("char" |-> OLD:Str)
            ("s" |-> str(INPUT:IntSeq)),
            parent(0))
          =>
          1 |-> scope(
            ("result" |-> str(encryptAcc(A, CS)))
            ("char" |-> lastChar(CS, OLD))
            ("s" |-> str(INPUT)),
            parent(0)))
         ...
       </scopes>
       <heap> .Map </heap>
       [priority(40)]
endmodule
