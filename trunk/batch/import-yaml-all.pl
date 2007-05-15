#!/usr/bin/perl -w
use lib '../scripts/';
use PubShelf;
use YAML;
use strict;

=rem
unless($ARGV[0] && -e $ARGV[0] ) {
  die "Usage : ./import-via-yaml.pl {YAML file}\n";
}

print STDERR "Loading $ARGV[0] ...\n";
my $data = YAML::LoadFile( $ARGV[0] );
=cut

my $ps = new PubShelf('test');
foreach my $yaml_file (`ls ../data/*.yaml`) {
  next if( $yaml_file =~ /template/ );
  chomp($yaml_file);
  print STDERR "Loading $yaml_file ...\n";
  my $data = YAML::LoadFile( $yaml_file );
  $ps->insert_yaml($data);
}
