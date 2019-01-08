from orator.migrations import Migration


class CreateSummariesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("summaries") as table:
            # openBD original
            table.string("isbn", 13)
            table.string("title")
            table.string("volume")
            table.string("series")
            table.string("author")
            table.string("publisher")
            table.string("pubdate")
            table.string("cover")
            # Librarian original
            table.date("published_at")

            table.primary("isbn")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("summaries")
