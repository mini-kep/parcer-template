def add_dividers(row):
    content = " | ".join(row) 
    return "| {} |".format(content)

    
def to_markdown(table):
    """Translate *table* to markdown. Use first row in *table* as header.
       
       Args:
           row - list of strings
           
       Returns:
           string
    """    
    table = list(table)
    header = table[0]
    horiz = ["-" * len(x) for x in header]
    body = table[1:]

    table = [header, horiz]
    table.extend(body)
    
    table = [add_dividers(row) for row in table]    
    return '\n'.join(table)


def short_link(url, n=60):
    """Shorten *url* to *n* characters."""
    if len(url) > n:
        text = url[:n] + '...'
    else:
        text = url    
    return f'[{text}]({url})'


def interpret_frequencies(freqs):
    """Make a text description of frequencies based on *freqs* string."""
    mapper = dict(a='annual',
                  q='quarterly',
                  m='monthly',
                  w='weekly',
                  d='daily')
    freq_str = ", ".join([mapper[f] for f in freqs])
    return freq_str.capitalize() 


class Formatter:
    def __init__(self, cls):
        varname_str = ", ".join(cls.all_varnames)
        url_str = short_link(cls.source_url)        
        self.rows = [("Parser", cls.__name__),
            ("Description", cls.__doc__),
            ("URL", url_str),
            ("Frequency", interpret_frequencies(cls.freqs)),
            ("Variables", varname_str)]
        
    def as_markdown(self):
        return to_markdown(self.rows)
    
if __name__ == "__main__":
    from parsers import RosstatKEP, CBR_USD, BrentEIA
    for cls in  RosstatKEP, CBR_USD, BrentEIA:
        print(Formatter(cls).as_markdown())
        print()
