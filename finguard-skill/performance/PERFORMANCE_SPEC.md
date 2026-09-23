# Performance Specification

## Goals
- fast first meaningful paint on landing page
- responsive dashboard interactions
- bounded API latency for common reads
- low-latency ML inference for single transactions
- asynchronous processing for batch workloads

## Practices
- paginate transaction/alert tables
- cache immutable/reference data
- index frequent queries
- avoid N+1 database access
- lazy-load heavy analytics modules
- stream or batch large datasets rather than loading all rows into memory
- apply timeouts to external AI calls
- use background jobs for long-running ingestion or document indexing

## Performance verification
Record measured values in benchmark docs; do not invent target attainment.
