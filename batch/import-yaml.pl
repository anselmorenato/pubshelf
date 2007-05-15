#!/usr/bin/perl -w
use lib './';
use PubShelf;
use YAML;
use strict;

unless($ARGV[0] && -e $ARGV[0] ) {
  die "Usage : ./import-via-yaml.pl {YAML file}\n";
}

print STDERR "Loading $ARGV[0] ...\n";
my $data = YAML::LoadFile( $ARGV[0] );

my $ps = new PubShelf('test');
$ps->insert_yaml($data);
