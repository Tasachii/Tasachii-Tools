<!--
STYLE EXEMPLAR (archetype: npm / language library).
Shows the house style adapted to a LIBRARY: quickstart-first, API table front and
centre, no screenshots, a plain English title (the Japanese flavour is NOT forced here
because the project has none). Copy the SHAPE and voice, never the facts.
-->

# ndjson-stream

A streaming NDJSON (newline-delimited JSON) parser and serializer for Node.js. Reads and
writes one JSON object per line over backpressure-aware streams, so a 10 GB log file moves
through constant memory. Zero dependencies, TypeScript types included, ESM and CommonJS.

[![npm](https://img.shields.io/npm/v/ndjson-stream)](https://www.npmjs.com/package/ndjson-stream)
[![CI](https://img.shields.io/github/actions/workflow/status/Tasachii/ndjson-stream/ci.yml)](https://github.com/Tasachii/ndjson-stream/actions)
[![types](https://img.shields.io/npm/types/ndjson-stream)](https://www.npmjs.com/package/ndjson-stream)

## Quickstart

```bash
npm install ndjson-stream
```

```ts
import { parse, serialize } from "ndjson-stream";
import { createReadStream, createWriteStream } from "node:fs";

// Read a .ndjson file, keep only errors, write them back out.
createReadStream("events.ndjson")
  .pipe(parse())
  .filter((event) => event.level === "error")
  .pipe(serialize())
  .pipe(createWriteStream("errors.ndjson"));
```

That is the whole API surface for the common case: `parse()` turns a byte stream into an
object stream, `serialize()` does the reverse.

## Why this exists

`JSON.parse` needs the whole document in memory and chokes on a file that does not fit.
NDJSON sidesteps that — one object per line — but the line-splitting, partial-chunk
buffering, and backpressure are fiddly to get right by hand. `ndjson-stream` is that
buffering, done once and tested, exposed as two standard Node streams you can `.pipe()`
into anything.

## API

| Export | Signature | Description |
|---|---|---|
| `parse` | `parse(opts?) => Transform` | Bytes/string chunks in, parsed objects out. One object per `\n`. |
| `serialize` | `serialize(opts?) => Transform` | Objects in, newline-terminated JSON strings out. |
| `parseLines` | `parseLines(iterable) => AsyncIterable` | Async-iterator form, for `for await` loops. |

### Options

| Option | Type | Default | Applies to | Description |
|---|---|---|---|---|
| `strict` | `boolean` | `true` | `parse` | Throw on a malformed line. When `false`, the line is skipped and emitted on the `skip` event. |
| `maxLineBytes` | `number` | `1_048_576` | `parse` | Guard against an unbounded line; exceeding it errors the stream. |
| `replacer` | `(k, v) => unknown` | — | `serialize` | Passed straight to `JSON.stringify`. |

## Error handling

`parse()` emits standard stream `error` events; in non-strict mode it emits `skip` with
`{ line, error }` instead of throwing, so one bad line never kills a batch job:

```ts
parse({ strict: false }).on("skip", ({ line }) => log.warn("dropped line", line));
```

## Compatibility

- Node.js 18 or newer (uses Web Streams interop and `node:stream`)
- Ships ESM and CommonJS builds plus `.d.ts` types — works in both `import` and `require`
- No runtime dependencies

## Testing

```bash
npm test
```

Runs the unit suite (line splitting across chunk boundaries, multi-byte UTF-8 on the
boundary, strict vs non-strict, backpressure) and a memory-ceiling test that streams a
1 GB fixture under a 64 MB heap cap.

## License

MIT © Phasathat Jaruchitsophon
