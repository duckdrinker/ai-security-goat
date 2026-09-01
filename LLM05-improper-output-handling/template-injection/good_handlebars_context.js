/**
 * Mitigated: the template string is a static literal owned by the codebase --
 * only the render context (second call's argument) is untrusted.
 */
const Handlebars = require("handlebars");

async function callLlm(prompt) {
  // returns raw, untrusted model output
}

const template = Handlebars.compile("Ticket summary: {{summary}}");

async function renderSummary(ticket) {
  const summary = await callLlm("Summarize the ticket for the customer");
  return template({ summary });
}
