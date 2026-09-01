"""
Mitigated (by absence, not by sanitization): a generic source (decoded_input)
flows into a sink, but nothing in this file trips an existing shipped SAST
rule first -- genericChainWithoutAiSinkPresent_isNotFlagged. Generic sources
only ever UPGRADE an existing sink-present finding; with no finding to
upgrade, this detector reports nothing on its own.

NOTE (assumption, unconfirmed against source): built with yaml.load() as the
sink on the theory that it isn't already covered by the SAST rules the dev
named (python.code_injection/command_injection/sql_injection). If yaml.load()
turns out to be covered by some other shipped SAST rule, pick a different
sink here instead of treating a finding as a bug.
"""
import base64
import yaml

encoded_config = "cGF5bG9hZDogeyFweXRob24vb2JqZWN0OmFwcGx5On...=="  # decoded_input source
raw_config = base64.b64decode(encoded_config)
config = yaml.load(raw_config)
