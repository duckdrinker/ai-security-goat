/**
 * Mitigated: eval() is called on a hardcoded literal, not tainted input --
 * jsEvalOfConstant_isNotFlagged.
 */
const result = eval("2 + 2");
