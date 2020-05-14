-- sqlite3 urls.db < schema.sql


drop table if exists urls;
create table urls (
	id integer primary key autoincrement,
	original_url text not null,
	visited integer default 0,
	unique(original_url)
);