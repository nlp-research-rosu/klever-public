#!/usr/bin/env perl
use strict;
use warnings;
use JSON::PP qw(decode_json);

binmode STDOUT, ":encoding(UTF-8)";

my $trace =
  "/generation-evidence/codex-trace/2026/07/25/"
  . "rollout-2026-07-25T00-33-15-019f97c3-7059-7723-a2dd-413798611f73.jsonl";

open my $fh, "<", $trace or die "open $trace: $!";
my (%count, @commands, @final_messages);
my $lines = 0;
while (my $line = <$fh>) {
  ++$lines;
  my $event = decode_json($line);
  my $payload = $event->{payload} // {};
  my $key = join(
    "\t",
    $event->{type} // "-",
    $payload->{type} // "-",
    $payload->{role} // "-",
    $payload->{name} // "-"
  );
  ++$count{$key};

  if (($payload->{type} // "") eq "function_call"
      && ($payload->{name} // "") eq "exec_command") {
    my $args = decode_json($payload->{arguments});
    push @commands, $args->{cmd} // "";
  }
  if (($payload->{type} // "") eq "message"
      && ($payload->{role} // "") eq "assistant"
      && ($payload->{phase} // "") eq "final_answer") {
    my $text = join(
      "\n",
      map { $_->{text} // "" } @{$payload->{content} // []}
    );
    push @final_messages, $text;
  }
}
close $fh;

print "json_lines_valid=$lines\n";
print "EVENT_COUNTS\n";
print "$count{$_}\t$_\n" for sort keys %count;
print "EXEC_COMMANDS\n";
for my $index (0 .. $#commands) {
  my $command = $commands[$index];
  $command =~ s/\n/\\n/g;
  print (($index + 1) . "\t" . $command . "\n");
}
print "FINAL_MESSAGES=", scalar(@final_messages), "\n";
for my $message (@final_messages) {
  $message =~ s/\n/\\n/g;
  print "$message\n";
}

open my $log, "<", "/generation-evidence/codex-output.log"
  or die "open codex-output.log: $!";
my ($output_lines, $tops, $stuck, $validated, $result_markers) = (0, 0, 0, 0, 0);
while (my $line = <$log>) {
  ++$output_lines;
  ++$tops if $line =~ /^\#Top\s*$/;
  ++$stuck if $line =~ /WarnStuckClaimState/;
  ++$validated if $line =~ /\bVALIDATED\b/;
  ++$result_markers if $line =~ /^RESULT:/;
}
close $log;
print "CODEX_OUTPUT lines=$output_lines top_lines=$tops stuck_mentions=$stuck ",
  "validated_mentions=$validated result_markers=$result_markers\n";
