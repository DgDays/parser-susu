BEGIN TRANSACTION;

DROP TABLE IF EXISTS "Directions";
DROP TABLE IF EXISTS "Disciplines";

CREATE TABLE "Directions" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT NOT NULL
);
CREATE TABLE "Disciplines" (
	"name"	TEXT NOT NULL,
	"semesters"	TEXT NOT NULL,
	"id_direction"	INTEGER NOT NULL,
	"hours"	INTEGER NOT NULL,
	FOREIGN KEY ("id_direction") REFERENCES Directions("id")
);
COMMIT;
