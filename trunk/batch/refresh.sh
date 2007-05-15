#!/bin/bash
rm ../db.test/pubshelf.db
sqlite3 ../db.test/pubshelf.db < ../schema/pubshelf.sqlite3
rm -rf ../db.test/????
