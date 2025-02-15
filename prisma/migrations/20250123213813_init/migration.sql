-- CreateTable
CREATE TABLE "Song" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "artists" TEXT NOT NULL,
    "album" TEXT NOT NULL,
    "genre" TEXT NOT NULL,
    "label" TEXT NOT NULL,
    "localy_stored" BOOLEAN NOT NULL DEFAULT false,
    "url" TEXT,
    "path" TEXT
);
