/**
 * bad_handlebars.js
 * Triggers template-injection: the *first* argument to Handlebars.compile()
 * (the template string) is untrusted LLM output, so an attacker-controlled
 * helper/expression executes at compile+render time.
 */
const Handlebars = require("handlebars");

async function callLlm(prompt) {
  // returns raw, untrusted model output
}

async function renderSummary(ticket) {
  const llmTemplate = await callLlm("Draft a Handlebars summary template");
  const compiled = Handlebars.compile(llmTemplate);
  return compiled({ ticket });
}
