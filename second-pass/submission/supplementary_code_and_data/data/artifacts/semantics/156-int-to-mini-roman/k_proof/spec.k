requires "verification.k"

module ROMAN-LEMMA-SPEC
  imports ROMAN-BASE

  claim [thousandsHelper]:
    <k>
      #helperCase("_roman_thousands", D)
      => str(thousandsDigit(D))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", romanThousandsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 0 andBool D <=Int 1

  claim [hundredsHelper]:
    <k>
      #helperCase("_roman_hundreds", D)
      => str(hundredsDigit(D))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_hundreds"
          |-> closureVal("digit", romanHundredsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 0 andBool D <=Int 9

  claim [tensHelper]:
    <k>
      #helperCase("_roman_tens", D)
      => str(tensDigit(D))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_tens"
          |-> closureVal("digit", romanTensBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 0 andBool D <=Int 9

  claim [onesHelper]:
    <k>
      #helperCase("_roman_ones", D)
      => str(onesDigit(D))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_ones"
          |-> closureVal("digit", romanOnesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 0 andBool D <=Int 9

  claim [thousandsIndexRange]:
    <k> #checkThousandsIndex(N) => true </k>
    requires N >=Int 1 andBool N <=Int 1000

  claim [hundredsIndexRange]:
    <k> #checkHundredsIndex(N) => true </k>
    requires N >=Int 1 andBool N <=Int 1000

  claim [tensIndexRange]:
    <k> #checkTensIndex(N) => true </k>
    requires N >=Int 1 andBool N <=Int 1000

  claim [onesIndexRange]:
    <k> #checkOnesIndex(N) => true </k>
    requires N >=Int 1 andBool N <=Int 1000
endmodule

module ROMAN-SPEC
  imports ROMAN-VERIFICATION

  claim [romanCorrect]:
    <k>
      Call(Name("int_to_mini_roman"), Int(N))
      => str(romanSpec(N))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", romanThousandsBody, 0)
        "_roman_hundreds"
          |-> closureVal("digit", romanHundredsBody, 0)
        "_roman_tens"
          |-> closureVal("digit", romanTensBody, 0)
        "_roman_ones"
          |-> closureVal("digit", romanOnesBody, 0)
        "int_to_mini_roman"
          |-> closureVal("number", romanSolutionBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool N <=Int 1000
endmodule
