requires "verification-no-intof.k"

module REVIEWER-INTOF-TYPED-CONNECTION
  imports SUMMARY-DEFINITION

  claim [integer-branch]:
    <k> intOf(I:Int) => intLikeTotal(I) </k>

  claim [boolean-branch]:
    <k> intOf(B:Bool) => intLikeTotal(B) </k>
endmodule
