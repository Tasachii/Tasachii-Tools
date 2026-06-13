<!--
STYLE EXEMPLAR (archetype: backend service / API).
Shows the house style adapted to a SERVICE: run-it-first (docker compose), env-var and
endpoint tables, architecture, deployment, health/observability, and a status section
for what is and isn't wired up. No marketing screenshots. Copy the SHAPE, not the facts.
-->

# linkrelay

A small webhook relay service. It receives a provider webhook on one HTTPS endpoint,
verifies the signature, normalizes the payload, and fans it out to your own subscribers
with retries and a dead-letter queue. Stateless app tier, PostgreSQL for delivery state,
one container to run.

## Status

The full receive → verify → normalize → deliver → retry pipeline is **implemented and
tested** (unit, integration against a real Postgres, and an end-to-end test that drives a
stubbed subscriber). What is **not** done for you, because it needs your own secrets and a
public URL: registering the webhook with a real provider and pointing it at a live
deployment. The checklist under [Going live](#going-live) covers that.

## Quickstart

```bash
git clone https://github.com/Tasachii/linkrelay.git
cd linkrelay
cp .env.example .env
docker compose up -d
```

The API and a Postgres come up together; the app waits for the database, runs migrations
on start, and serves on `http://localhost:8080`. Confirm it is healthy:

```bash
curl localhost:8080/health
```

## Why this exists

Every integration re-implements the same webhook plumbing — signature checks, idempotency
on retried deliveries, exponential backoff, a place for payloads that never succeed.
`linkrelay` is that plumbing as a standalone hop: providers point at it, your services
subscribe to it, and the retry/dead-letter logic lives in exactly one place instead of
being copy-pasted into every consumer.

## Architecture

```
Provider --(signed webhook)--> linkrelay API --> Postgres (delivery log + DLQ)
                                    |
                                    +--(POST, with retries)--> your subscribers
```

| Component | Role | Technology |
|---|---|---|
| `api` | HTTP ingress, signature verify, enqueue | Fastify 5, Node 20 |
| `worker` | Drains the delivery queue, retries with backoff | same image, `WORKER=1` |
| `db` | Delivery state, idempotency keys, dead-letter rows | PostgreSQL 16 |

Design decisions worth noting:

- **Idempotency on the provider's event id.** A retried webhook with a seen id is
  acknowledged but not re-fanned-out, so providers can retry safely.
- **At-least-once, not exactly-once.** Subscribers must be idempotent; the delivery id is
  sent in a header so they can dedupe. This keeps the relay simple and crash-safe.
- **Dead-letter over infinite retry.** After `MAX_ATTEMPTS` a delivery moves to the DLQ
  and stops consuming worker time; it can be replayed from there.

## Configuration

Set these in `.env` before exposing the service publicly.

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SIGNING_SECRET` | Yes | — | Shared secret used to verify inbound webhook signatures |
| `PORT` | No | `8080` | HTTP listen port |
| `MAX_ATTEMPTS` | No | `8` | Delivery attempts before a payload moves to the dead-letter queue |
| `RETRY_BASE_MS` | No | `500` | Base for exponential backoff between attempts |
| `LOG_LEVEL` | No | `info` | `debug` · `info` · `warn` · `error` |

## API

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/hooks/:provider` | Signature | Receives a provider webhook; verifies and enqueues it |
| GET | `/health` | None | Liveness + database connectivity, for load balancers |
| GET | `/deliveries/:id` | API key | Delivery status, attempt count, last error |
| POST | `/dlq/:id/replay` | API key | Re-enqueue a dead-lettered delivery |

## Going live

- [ ] Set a strong `SIGNING_SECRET` and a real `DATABASE_URL` in `.env`.
- [ ] Deploy behind HTTPS — a managed container host, or `ngrok http 8080` for testing.
- [ ] Register the public `https://<your-domain>/hooks/<provider>` URL in the provider's
      dashboard and send a test event; it should appear via `GET /deliveries/:id`.
- [ ] Point your subscribers' URLs at the relay's subscriber config.

## Testing

```bash
npm test                 # unit: signature verify, backoff schedule, payload normalize
npm run test:integration # against a real Postgres: idempotency, DLQ transitions
```

CI runs both on every push with a Postgres service container.

## Observability

- Structured JSON logs at `LOG_LEVEL`; each line carries the delivery id for tracing.
- `GET /health` reports database connectivity for load-balancer checks.
- Dead-letter depth is the metric to alert on — a rising DLQ means a subscriber is down.

## License

MIT © Phasathat Jaruchitsophon
