package PubShelf;

use DBI;
use strict;

sub new {
  my $class = shift;
  my $db_type = shift;
  my $self = {  test_db => '../db.test/pubshelf.db', 
                db => '../db/pubshelf.db',
                db_type => $db_type };
  if( $db_type eq 'test' ) {
    print STDERR 'Connectiong ',$self->{test_db}," ...\n";
    $self->{dbh} = DBI->connect('dbi:SQLite:dbname='.$self->{test_db},'','')
      || die "DBI connection error\n";
    $self->{file_dir} = '/home/linusben/pubshelf/db.test/';
  } else {
    print STDERR 'Connecting ',$self->{db}," ...\n";
    $self->{dbh} = DBI->connect('dbi:SQLite:dbname='.$self->{db},'','')
      || die "DBI connection error\n";
    $self->{file_dir} = '/home/linusben/pubshelf/db/';
  }
  bless $self, $class;
}

sub DESTROY {
  my $self = shift;
  $self->{dbh}->disconnect();
}

sub insert_yaml {
  my ($self, $data) = @_;
  
  my $sth_pubitem = $self->{dbh}->prepare('INSERT INTO pubitems
                      (nickname, title, authors, journal, volume, page, 
                       pub_year) VALUES (?,?,?,?,?,?,?)');
  my $sth_link = $self->{dbh}->prepare('INSERT INTO links
                      (pubitem_id, name, uri, uri_type) VALUES (?,?,?,?)');
  my $sth_new_tag = $self->{dbh}->prepare('INSERT INTO tags
                      (category, name) VALUES (?,?)');
  my $sth_tag_pubitem = $self->{dbh}->prepare('INSERT INTO tags_pubitems
                          (pubitem_id, tag_id) VALUES (?,?)');
 
  ## Pubitems
  my ($pubitem_nickname) = split(/\,/, $data->{authors});
  $pubitem_nickname =~ s/[A-Z\-]+$//;
  $pubitem_nickname =~ s/\s+//g;
  $pubitem_nickname .= $data->{pub_year};
  my $rv_pubitem_nickname 
    = $self->{dbh}->selectall_arrayref( 'SELECT * FROM pubitems
                              WHERE nickname like ?', {Slice => {}},
                              ($pubitem_nickname.'%') );
  $pubitem_nickname .= '.'.($#{$rv_pubitem_nickname}+2);
  $sth_pubitem->execute( $pubitem_nickname, $data->{title}, $data->{authors},
                        $data->{journal}, $data->{volume}, $data->{page},
                        $data->{pub_year} );
  $sth_pubitem->finish();
  my $pubitem_id = $self->{dbh}->last_insert_id(undef, undef, 'pubitems', 'id');

  ## Links
  my $file_dir = $self->{file_dir}.$data->{pub_year};

  unless(-d $file_dir) { mkdir $file_dir; }
  my $filename = "$file_dir/$pubitem_nickname".'_'.$data->{file}->{name}
                .'.'.$data->{file}->{uri_type};
  $filename =~ s/\s+//g;
  rename($data->{file}->{path}, $filename) if(-e $data->{file}->{path});
  $sth_link->execute($pubitem_id, $data->{file}->{name},
                     'file://'.$filename, $data->{file}->{uri_type});
  $sth_link->finish();

  ## Tags
  foreach my $tmp_tag (@{$data->{tags}}) {
    my ($category, $name) = split(/\:/, $tmp_tag);
    my $rv = $self->{dbh}->selectall_arrayref('SELECT id FROM tags
                                WHERE category=? AND name=?', { Slice=>{} },
                                ($category, $name));
    my $tag_id = 0;
    if( $#{$rv} < 0 ) {
      $sth_new_tag->execute($category, $name);
      $tag_id = $self->{dbh}->last_insert_id(undef, undef, 'tags', 'id');
    } else {
      $tag_id = $rv->[0]->{id};
    }

    $sth_tag_pubitem->execute($pubitem_id, $tag_id);
  }
  $sth_new_tag->finish();
  $sth_tag_pubitem->finish();
}

1;
