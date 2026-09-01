"""
bad_argv_confirms_eval.py
A generic source (sys.argv, not AI-specific) flows into eval(). The shipped
python.code_injection SAST rule already flags this eval() call on its own;
the taint chain from sys.argv upgrades that finding to flow-confirmed / high
confidence -- it does NOT create a second, separate finding under
untrusted-data-reaches-code-sink's own id (see genericChainWithoutAiSinkPresent_isNotFlagged
in bad_generic_source_no_sast_finding.py for the contrast case).
"""
import sys

user_expression = sys.argv[1]
result = eval(user_expression)
