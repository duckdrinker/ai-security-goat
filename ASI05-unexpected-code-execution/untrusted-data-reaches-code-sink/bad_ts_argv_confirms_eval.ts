/**
 * bad_ts_argv_confirms_eval.ts
 * Same chain as bad_js_argv_confirms_eval.js, in TypeScript
 * (typescriptArgvToEval_confirmsSinkPresent).
 */
const userExpression: string = process.argv[2];
const result: unknown = eval(userExpression);
