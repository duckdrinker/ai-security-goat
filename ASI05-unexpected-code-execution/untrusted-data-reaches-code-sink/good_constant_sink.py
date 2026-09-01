"""
Mitigated: eval() is called, but on a hardcoded literal, not a tainted
variable -- constantSink_isNotFlagged.
"""
result = eval("2 + 2")
