from orator.migrations import Migration


class CreateSummariesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("summaries") as table:
            # openBD original
            table.string("isbn")
            table.long_text("title")
            table.string("volume")
            table.string("series")
            table.long_text("author")
            table.string("publisher")
            table.string("pubdate")
            table.long_text("cover")
            # Librarian original
            table.date("published_at").nullable()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("summaries")
