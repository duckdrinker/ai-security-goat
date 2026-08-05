/**
 * Triggers inference-call-without-timeout-or-token-cap: same pattern as the
 * Python OpenAI SDK case, ported to the JS/TS ecosystem. No `max_tokens`,
 * no per-request `timeout`, and no wrapping rate-limiter/circuit-breaker
 * around the call — a long or adversarial prompt can generate an unbounded
 * response and there is nothing here to cut it off.
 */
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function reply(userMsg: string): Promise<string> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "You are a helpful support assistant." },
      { role: "user", content: userMsg },
    ],
  });
  return response.choices[0].message.content ?? "";
}
