CREATE TABLE pubitems (
  id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  nickname      TEXT NOT NULL DEFAULT '',
  pub_type      TEXT NOT NULL DEFAULT 'paper',
  title         TEXT NOT NULL DEFAULT '',
  authors       TEXT NOT NULL DEFAULT '',
  journal       TEXT DEFAULT '',
  publisher     TEXT DEFAULT '',
  volume        TEXT DEFAULT '',
  page          TEXT DEFAULT '',
  pub_year      INTEGER NOT NULL DEFAULT 0,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE links (
  id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  pubitem_id  INTEGER NOT NULL,
  name        TEXT NOT NULL DEFAULT '',
  uri         TEXT NOT NULL DEFAULT '',
  uri_type    TEXT NOT NULL DEFAULT 'pdf',
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
  id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  pubitem_id  INTEGER NOT NULL,
  title       TEXT NOT NULL DEFAULT '',
  textbody    TEXT NOT NULL DEFAULT '',
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
  id                INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  category          TEXT NOT NULL DEFAULT '',
  name              TEXT NOT NULL DEFAULT '',
  created_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX tags_idx ON tags (category, name);

CREATE TABLE tags_pubitems (
  id                INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  pubitem_id        INTEGER NOT NULL,
  tag_id            INTEGER NOT NULL,
  created_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX tags_pubitems_idx ON tags_pubitems (pubitem_id, tag_id);
