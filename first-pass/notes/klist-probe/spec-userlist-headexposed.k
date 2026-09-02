// PARSE ERROR — on verif-userlist-notags: without [overload], the head-exposed cons pattern
// (I:Int, IS:IntsP) is a genuine parsing ambiguity between the IntsP cons and the ValsP cons.
requires "verif-userlist-notags.k"
module USERLIST-HEADEXPOSED-SPEC
  imports VERIF-USERLIST-NOTAGS
  claim <k> floopP(listP((I:Int, IS:IntsP))) => .K </k>
        <acc> A:Int => sumP((I, IS), A) </acc> [all-path]
endmodule
