#!/usr/bin/env perl
use strict;
use warnings;
use Digest::SHA qw(sha256_hex);
use JSON::PP qw(decode_json);

my $trace = "/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-31-25-019f8c99-51a5-7a12-811f-3c0052ef1541.jsonl";
open my $tfh, "<", $trace or die "open $trace: $!";
my (%top_types, %payload_types);
my ($trace_lines, $trace_bad_json, $tool_calls, $tool_outputs, $top_mentions) = (0, 0, 0, 0, 0);
while (my $line = <$tfh>) {
    ++$trace_lines;
    my $obj = eval { decode_json($line) };
    if (!$obj) {
        ++$trace_bad_json;
        next;
    }
    ++$top_types{$obj->{type} // "<missing>"};
    if (ref($obj->{payload}) eq "HASH") {
        ++$payload_types{$obj->{payload}{type} // "<missing>"};
    }
    ++$tool_calls if ($obj->{type} // "") eq "response_item"
                    && ref($obj->{payload}) eq "HASH"
                    && ($obj->{payload}{type} // "") =~ /tool_call$/;
    ++$tool_outputs if ($obj->{type} // "") eq "response_item"
                      && ref($obj->{payload}) eq "HASH"
                      && ($obj->{payload}{type} // "") =~ /tool_call_output$/;
    ++$top_mentions if $line =~ /\#Top/;
}
close $tfh;

my $log = "/generation-evidence/codex-output.log";
open my $lfh, "<", $log or die "open $log: $!";
binmode $lfh;
my $sha = Digest::SHA->new(256);
my ($log_lines, $log_top, $log_kprove, $log_stuck, $log_final) = (0, 0, 0, 0, 0);
while (my $line = <$lfh>) {
    $sha->add($line);
    ++$log_lines;
    ++$log_top if $line =~ /\#Top/;
    ++$log_kprove if $line =~ /\bkprove\b/;
    ++$log_stuck if $line =~ /WarnStuckClaimState/;
    ++$log_final if $line =~ /RESULT:\s*KPROVE_PASSED/;
}
close $lfh;

print "trace_path=$trace\n";
print "trace_lines=$trace_lines bad_json=$trace_bad_json tool_calls=$tool_calls tool_outputs=$tool_outputs lines_containing_Top=$top_mentions\n";
print "trace_top_types:\n";
print "  $_=$top_types{$_}\n" for sort keys %top_types;
print "trace_payload_types:\n";
print "  $_=$payload_types{$_}\n" for sort keys %payload_types;
print "codex_output_path=$log\n";
print "codex_output_sha256=", $sha->hexdigest, "\n";
print "codex_output_lines=$log_lines lines_containing_Top=$log_top lines_containing_kprove=$log_kprove lines_containing_stuck=$log_stuck lines_containing_final_marker=$log_final\n";
