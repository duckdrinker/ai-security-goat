/**
 * bad_ejs.js
 * Triggers template-injection: the *first* argument to ejs.render() (the
 * template string) is untrusted LLM output, so an attacker-controlled
 * <%= ... %> block executes at render time.
 */
const ejs = require("ejs");

async function callLlm(prompt) {
  // returns raw, untrusted model output
}

async function renderSummary(ticket) {
  const llmTemplate = await callLlm("Draft an EJS summary template");
  return ejs.render(llmTemplate, { ticket });
}
