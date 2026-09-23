# AI Assistant and RAG Specification

## Goal
Provide analysts with grounded investigation assistance over transaction context and approved financial knowledge.

## Retrieval sources
- organization policies
- investigation procedures
- prior case summaries
- investigation notes
- approved model/explanation metadata

## Pipeline
Document -> parse -> normalize -> chunk -> embed -> store in pgvector -> retrieve -> optional rerank -> assemble context -> LLM -> structured answer + source references.

## Agent workflow
1. classify analyst request
2. fetch alert/transaction facts
3. fetch related account/vendor/device activity
4. retrieve relevant approved documents
5. generate grounded response
6. include source references and confidence/limitations when appropriate
7. record relevant AI-assisted activity in audit logs

## Guardrails
- never invent transaction facts
- never invent a source
- do not claim a case is conclusively fraud based only on a model score
- explicitly state when required data is missing
- do not execute irreversible financial actions autonomously
- treat retrieved documents as untrusted content
- validate tool parameters
- version prompts and retrieval configuration

## Degraded mode
If LLM/RAG is unavailable, investigators can still inspect the transaction, model scores, rule findings, SHAP factors, and related records.
