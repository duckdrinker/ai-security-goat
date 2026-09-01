/**
 * Mitigated: the template string is a static literal owned by the codebase --
 * only the render data (second argument) is untrusted.
 */
const ejs = require("ejs");

const TEMPLATE = "Ticket summary: <%= summary %>";

async function callLlm(prompt) {
  // returns raw, untrusted model output
}

async function renderSummary(ticket) {
  const summary = await callLlm("Summarize the ticket for the customer");
  return ejs.render(TEMPLATE, { summary });
}
