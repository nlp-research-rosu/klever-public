requires "domains.md"

module STRING-PROBE
  imports INT
  imports STRING

  syntax Probe ::= "probeLen"
                 | "probeIndex"
                 | "probeAlphaLen"
                 | "probeEmojiLen"
                 | "probeAlphaIndex"
                 | "probeExpectedOne"
                 | "probeExpectedTwo"
  configuration <k> $PGM:Probe </k>

  rule <k> probeLen => lengthString("\u00e9") </k>
  rule <k> probeIndex => substrString("\u00e9", 0, 1) </k>
  rule <k> probeAlphaLen => lengthString("\u03b1") </k>
  rule <k> probeEmojiLen => lengthString("\U0001f642") </k>
  rule <k> probeAlphaIndex => substrString("\u03b1", 0, 1) </k>
  rule <k> probeExpectedOne =>
           "\u4e2d\u00e9\u03b1\U0001f642\U0001d11e" </k>
  rule <k> probeExpectedTwo =>
           "\U0001f642e\u0301\u4e2dA" </k>
endmodule
