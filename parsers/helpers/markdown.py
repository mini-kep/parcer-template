class Markdown:
    def interpret_frequency(freq):
        """Make a text description of frequency based on *freq* string."""
        mapper = dict(a='annual',
                      q='quarterly',
                      m='monthly',
                      w='weekly',
                      d='daily')
        return mapper[freq].capitalize()

    def _add_dividers(row):
        content = " | ".join(row)
        return "| {} |".format(content)

    def table(rows):
        """Translate *rows* to markdown table. Use first row as header.

           Args:
               rows(list) - list of strings, each sting is table column element

           Returns:
               string with markdown table.
        """
        table = list(rows)
        header = table[0]
        horiz = ["-" * len(x) for x in header]
        body = table[1:]

        table = [header, horiz]
        table.extend(body)

        table = [Markdown._add_dividers(row) for row in table]
        return '\n'.join(table)
