requires "reference-semantics/semantics.k"

module SLICE-CONNECTION-SPEC
  imports MPY

  // Structural induction target for the fixed slicing implementation.
  claim buildIS(IS:IntSeq, 0, isLen(IS), 1) => IS

  // Bridge-free connection theorem over an arbitrary continuation and every
  // configuration cell: fixed semantics removes exactly the two prefix codes.
  claim
    <k>
      Subscript(
        str(iCons(48, iCons(98, REST:IntSeq))),
        Slice(Int(2), NoBound, NoBound)
      ) ~> CONT:K
      => str(REST) ~> CONT
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> HP:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> STK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
endmodule
