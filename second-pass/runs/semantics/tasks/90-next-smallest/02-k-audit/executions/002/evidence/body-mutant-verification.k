requires "reference-semantics/semantics.k"

module NEXT-SMALLEST-BODY-MUTANT
  imports MPY

  // This is the constructor term generated from solution.py, factored into
  // named pieces so that the proof claims remain readable.
  syntax Stmts ::= "nextSmallestLoopBody" [macro]
  rule nextSmallestLoopBody =>
    If(Compare(Name("count"), CmpOp("==", Int(0))),
       Assign(Name("smallest"), Name("value"))
       Assign(Name("count"), Int(1)),
       If(Compare(Name("value"), CmpOp("<", Name("smallest"))),
          Assign(Name("second"), Name("smallest"))
          Assign(Name("count"), Int(2))
          Assign(Name("smallest"), Name("value")),
          If(Compare(Name("value"), CmpOp("!=", Name("smallest"))),
             If(BoolOp("or",
                       (Compare(Name("count"), CmpOp("==", Int(1))),
                        Compare(Name("value"), CmpOp("<", Name("second"))),
                        .Exprs)),
                Assign(Name("second"), Int(999))
                Assign(Name("count"), Int(2)),
                .Stmts) .Stmts,
             .Stmts) .Stmts))

  syntax Stmts ::= "nextSmallestReturn" [macro]
  rule nextSmallestReturn =>
    If(Compare(Name("count"), CmpOp("==", Int(2))),
       Return(Name("second")) .Stmts,
       .Stmts)
    Return(NoneVal)

  syntax Stmts ::= "nextSmallestBody" [macro]
  rule nextSmallestBody =>
    Assign(Name("smallest"), Int(0))
    Assign(Name("second"), Int(0))
    Assign(Name("count"), Int(0))
    Assign(Name("value"), Int(0))
    For(Name("value"), Name("lst"), nextSmallestLoopBody)
    nextSmallestReturn

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule =>
    Module(FuncDef("next_smallest", Params("lst"), nextSmallestBody))

  // An inductive carrier keeps every symbolic head in the Int sort.  It is a
  // ValSeq inhabitant whose iterator rules are isomorphic to .ValSeq/vCons.
  syntax Ints ::= "nilInts" | consInts(Int, Ints)
  syntax ValSeq ::= intVals(Ints)
  syntax Bool ::= intsEmpty(Ints) [function, total]
  syntax Int ::= intsHead(Ints) [function, total]
  syntax Ints ::= intsTail(Ints) [function, total]
  rule intsEmpty(nilInts) => true
  rule intsEmpty(consInts(_:Int, _:Ints)) => false
  rule intsHead(consInts(X:Int, _:Ints)) => X
  rule intsTail(consInts(_:Int, XS:Ints)) => XS
  rule <k> #iterNext(list(intVals(IS:Ints))) => #iterDone ... </k>
    requires intsEmpty(IS)
  rule <k> #iterNext(list(intVals(IS:Ints)))
        => #iterYield(intsHead(IS), list(intVals(intsTail(IS)))) ... </k>
    requires notBool intsEmpty(IS)

  // Independent executable specification: COUNT is 0 before any distinct
  // value, 1 after the minimum, and 2 after the second distinct minimum.
  syntax Val ::= nsScan(Ints, Int, Int, Int) [function, total]
  rule nsScan(IS:Ints, _:Int, N:Int, C:Int) => N
    requires intsEmpty(IS) andBool C ==Int 2
  rule nsScan(IS:Ints, _:Int, _:Int, C:Int) => noneV
    requires intsEmpty(IS) andBool notBool (C ==Int 2)
  rule nsScan(IS:Ints, _:Int, N:Int, C:Int)
    => nsScan(intsTail(IS), intsHead(IS), N, 1)
    requires notBool intsEmpty(IS) andBool C ==Int 0
  rule nsScan(IS:Ints, S:Int, _:Int, C:Int)
    => nsScan(intsTail(IS), intsHead(IS), S, 2)
    requires notBool intsEmpty(IS) andBool notBool (C ==Int 0)
     andBool intsHead(IS) <Int S
  rule nsScan(IS:Ints, S:Int, N:Int, C:Int)
    => nsScan(intsTail(IS), S, N, C)
    requires notBool intsEmpty(IS) andBool notBool (C ==Int 0)
     andBool intsHead(IS) ==Int S
  rule nsScan(IS:Ints, S:Int, _:Int, C:Int)
    => nsScan(intsTail(IS), S, intsHead(IS), 2)
    requires notBool intsEmpty(IS) andBool C ==Int 1
     andBool intsHead(IS) >Int S
  rule nsScan(IS:Ints, S:Int, N:Int, C:Int)
    => nsScan(intsTail(IS), S, intsHead(IS), 2)
    requires notBool intsEmpty(IS) andBool notBool (C ==Int 0)
     andBool notBool (C ==Int 1)
     andBool intsHead(IS) >Int S andBool intsHead(IS) <Int N
  rule nsScan(IS:Ints, S:Int, N:Int, C:Int)
    => nsScan(intsTail(IS), S, N, C)
    requires notBool intsEmpty(IS) andBool notBool (C ==Int 0)
     andBool notBool (C ==Int 1)
     andBool intsHead(IS) >Int S andBool intsHead(IS) >=Int N
endmodule

// This module installs the separately proved loop theorem as a reusable lemma
// for the entry-point proof.  prove.sh first proves NEXT-SMALLEST-LOOP-SPEC
// against the base module, then compiles this module and proves the call claim.
module NEXT-SMALLEST-BODY-MUTANT-WITH-LOOP-LEMMA
  imports NEXT-SMALLEST-BODY-MUTANT

  rule
    <k>
      #loop(list(intVals(INPUT:Ints)),
            Name("value"),
            nextSmallestLoopBody)
      ~> nextSmallestReturn
      ~> #endcall
    =>
      nsScan(INPUT, SMALLEST:Int, SECOND:Int, COUNT:Int)
      ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(("value" |-> OLD_VALUE:Int
                    "lst" |-> LST:Val
                    "smallest" |-> SMALLEST
                    "second" |-> SECOND
                    "count" |-> COUNT),
                   parent(0)))
    =>
      ((SC
        1 |-> scope(("value" |-> OLD_VALUE
                     "lst" |-> LST
                     "smallest" |-> SMALLEST
                     "second" |-> SECOND
                     "count" |-> COUNT),
                    parent(0))) [1 <- undef])
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) REST:List
    =>
      REST
    </stack>
    <ret> noRet </ret>
    <exc> EXC:Exc </exc>
    <exit-code> CODE:Int </exit-code>
    requires notBool (1 in_keys(SC))
    [priority(40)]
endmodule
