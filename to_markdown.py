table1 = [
  ['Branch', 'Commit'],
  ['master', '0123456789abcdef'],
  ['staging', 'fedcba9876543210']
]


def add_dividers(row):
    content = " | ".join(row) 
    return "| {} |".format(content)

    
assert add_dividers(['Branch', 'Commit']) == '| Branch | Commit |'


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

md = to_markdown(table1)
assert md.startswith("|")
assert 'Branch' in md
assert 'fedcba9876543210' in md