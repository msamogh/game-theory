drop table if exists scores;
create table scores (
	id integer primary key autoincrement,
	name text not null,
	g1 integer,
	g2 integer, 
	g3 integer,
	g4 integer
);