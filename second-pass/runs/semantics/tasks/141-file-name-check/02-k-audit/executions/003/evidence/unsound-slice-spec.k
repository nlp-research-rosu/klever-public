requires "unsound-interpretation.k"

module UNSOUND-SLICE-SPEC
  imports UNSOUND-INTERPRETATION

  // The real fixed [-4:] slice of c.txt is .txt.  The proof-local bridge plus
  // an admissible interpretation of suffix4 instead reaches .bin.
  claim
    <k> Subscript(
          str(cTxt),
          Slice(UnaryOp("-", Int(4)), NoBound, NoBound))
      => str(iCons(46, iCons(98, iCons(105, iCons(110, .IntSeq))))) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
