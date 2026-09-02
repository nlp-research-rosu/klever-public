requires "verification.k"

module UNSOUND-INTERPRETATION
  imports VERIFICATION

  // Ground IntSeq macros for six filenames that the real program accepts.
  syntax IntSeq ::= "aTxt" [macro]
                  | "bTxt" [macro]
                  | "cTxt" [macro]
                  | "dTxt" [macro]
                  | "eExe" [macro]
                  | "fDll" [macro]
  rule aTxt => iCons(97, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))
  rule bTxt => iCons(98, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))
  rule cTxt => iCons(99, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))
  rule dTxt => iCons(100, iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))
  rule eExe => iCons(101, iCons(46, iCons(101, iCons(120, iCons(101, .IntSeq)))))
  rule fDll => iCons(102, iCons(46, iCons(100, iCons(108, iCons(108, .IntSeq)))))

  // W1: the count oracle is permitted to say a.txt contains zero dots.
  rule charCount(aTxt, 46) => 0

  // W2: keep b.txt's dot count correct, but permit the head oracle to say '1'.
  rule charCount(bTxt, 46) => 1
  rule headCode(bTxt) => 49

  // W3: keep c.txt's earlier observations correct, but permit a wrong suffix.
  rule charCount(cTxt, 46) => 1
  rule headCode(cTxt) => 99
  rule <k> str(suffix4(cTxt))
        => str(iCons(46, iCons(98, iCons(105, iCons(110, .IntSeq))))) ... </k>
       [priority(39)]

  // W4-W6: keep dot/head observations correct but negate the corresponding
  // true equality flag for .txt, .exe, and .dll.
  rule charCount(dTxt, 46) => 1
  rule headCode(dTxt) => 100
  rule suffixIs(dTxt, 0) => false
  rule suffixIs(dTxt, 1) => false
  rule suffixIs(dTxt, 2) => false

  rule charCount(eExe, 46) => 1
  rule headCode(eExe) => 101
  rule suffixIs(eExe, 0) => false
  rule suffixIs(eExe, 1) => false
  rule suffixIs(eExe, 2) => false

  rule charCount(fDll, 46) => 1
  rule headCode(fDll) => 102
  rule suffixIs(fDll, 0) => false
  rule suffixIs(fDll, 1) => false
  rule suffixIs(fDll, 2) => false
endmodule
