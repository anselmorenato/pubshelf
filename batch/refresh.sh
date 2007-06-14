#!/bin/bash
rm ../db.test/pubshelf.db
sqlite3 ../db.test/pubshelf.db < ../etc/pubshelf_sqlite3.sql
#rm -rf ../db.test/????
