#!/bin/bash
TESTDB="../db.test/pubshelf.db"
if [ -e  $TESTDB ]; then
  rm $TESTDB
fi
sqlite3 $TESTDB < ../config/schema.sqlite3.sql
#rm -rf ../db.test/????
