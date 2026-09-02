const fs = require("fs");

if (process.argv.length !== 3) {
  console.error("usage: node trace_summary.js TRACE.jsonl");
  process.exit(2);
}

const lines = fs.readFileSync(process.argv[2], "utf8").trimEnd().split("\n");
const counts = new Map();
const calls = [];
const customCalls = [];
const messages = [];

for (let index = 0; index < lines.length; index += 1) {
  const row = JSON.parse(lines[index]);
  const payloadType = row.payload && row.payload.type ? row.payload.type : "";
  const key = `${row.type}:${payloadType}`;
  counts.set(key, (counts.get(key) || 0) + 1);

  if (row.type === "response_item" && payloadType === "function_call") {
    calls.push({
      line: index + 1,
      name: row.payload.name,
      arguments: row.payload.arguments,
    });
  }
  if (row.type === "response_item" && payloadType === "custom_tool_call") {
    customCalls.push({
      line: index + 1,
      name: row.payload.name,
      input: row.payload.input,
    });
  }
  if (
    row.type === "response_item" &&
    payloadType === "message" &&
    row.payload.role === "assistant"
  ) {
    const text = (row.payload.content || [])
      .filter((item) => item.type === "output_text")
      .map((item) => item.text)
      .join("\n");
    messages.push({ line: index + 1, text });
  }
}

console.log(`lines=${lines.length}`);
for (const [key, value] of [...counts.entries()].sort()) {
  console.log(`event_count ${key} ${value}`);
}
for (const call of calls) {
  console.log(`tool_call line=${call.line} name=${call.name}`);
  console.log(call.arguments);
}
for (const call of customCalls) {
  console.log(`custom_tool_call line=${call.line} name=${call.name}`);
  console.log(call.input);
}
for (const message of messages) {
  console.log(`assistant_message line=${message.line}`);
  console.log(message.text);
}
