/**
 * bad_js_argv_confirms_eval.js
 * Generic source (process.argv) flows into eval(). The shipped SAST
 * code-injection rule already flags this eval() call; the taint chain from
 * process.argv upgrades that finding to flow-confirmed / high confidence
 * instead of creating a duplicate finding under this detector's own id
 * (jsArgvToEval_confirmsSinkPresent).
 */
const userExpression = process.argv[2];
const result = eval(userExpression);
