# Evidence — Social Media Studio

## Ingestion
- **Test:** `curl -X POST http://localhost:8000/campaigns/ -H "Content-Type: application/json" -d '{"title":"Test","source_text":"Content"}'`
- **Result:** Campaign created with `id`, `status: draft`

## Variant Generation
- **Test:** `curl http://localhost:8000/campaigns/1/variants`
- **Result:** 3 variants (Instagram, X, LinkedIn) with different captions

## Review Workflow
- **Test:** `curl -X POST http://localhost:8000/variants/1/approve`
- **Result:** Status changed to `approved`

## Schedule
- **Test:** `curl -X POST http://localhost:8000/variants/1/schedule -H "Content-Type: application/json" -d '{"scheduled_at":"2026-08-27T10:00:00"}'`
- **Result:** `scheduled_at` set

## Publish
- **Test:** `curl -X POST http://localhost:8000/variants/1/publish`
- **Result:** Published to Discord

## Idempotency
- **Test:** Publish twice
- **Result:** First attempt success, second returns "already published"

## Discord
- **Test:** Published message appears in Discord channel
- **Result:** ✅ Verified

## Scheduler
- **Test:** Scheduled variant publishes automatically
- **Result:** `status: published`, `published_at` set