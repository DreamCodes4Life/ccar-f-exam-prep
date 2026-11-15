# Domain 5: Context Management & Reliability (15%)

Keeping what the model sees useful, affordable and reliable. Points are tagged with the step and lesson they come from.

## The stateless API

- The Messages API keeps nothing between calls. Your code holds the conversation and resends all of it each time, so every turn costs more as the history grows, until it fills the context window. Managing that list is this domain. (2.1)
- Read text from blocks of type `text`; current models can start a response with a `thinking` block. Check `stop_reason` (`end_turn`, `max_tokens`, `tool_use`, `refusal`) before using the content. (2.1)

## Retrieval

- RAG: when the source is too big for the prompt, retrieve the relevant chunks and answer from them. Chunk by size (with overlap), by structure (headings) or by meaning. (2.7)
- Semantic search (embeddings, cosine similarity) finds meaning; BM25 keyword search finds exact terms (codes, names). Hybrid search merges both rankings, for example with reciprocal rank fusion. (2.7)
- Agentic search: give Claude a search tool and let it search repeatedly, instead of one retrieval up front. (2.7)

## Caching and cost

- Prompt caching: mark a long, stable prefix (tools, system prompt, documents) with `cache_control`. The first call writes the cache, later calls read it at a fraction of the price. It is a **prefix match** in the order tools → system → messages: any change early in the request invalidates everything after it, so stable content goes first and varying content (a timestamp, the question) after the marker. Verify with `usage.cache_read_input_tokens`. Default lifetime 5 minutes, refreshed on each hit (a 1-hour option costs more to write); at most 4 markers; minimum cacheable length 512 tokens on Sonnet 5.5. (2.8)
- Caching vs batches: caching fits a repeated prefix while a user waits; Message Batches (half price, results within 24 hours) fit work that can wait. (2.8)
- Message Batches cost half the normal price, for work that can wait. (Domain 4 topic too; later steps.)

## Reliability

- Thinking on current models is adaptive, with `output_config.effort` (`low` … `max`) as the depth and cost knob; `budget_tokens` returns a 400 on current models. (2.8)
- Citations tie each claim to the exact passage in a source document. (2.8)
- A high overall accuracy can hide weak segments. Before cutting human review, measure each document type and field, keep sampling, and reduce review only where each segment meets the bar. A confidence score the model reports about itself isn't calibrated. (2.3)
- When sources disagree, keep both values with their sources and flag the conflict, instead of silently picking one. (2.6)
- Check `stop_reason == "max_tokens"`: a truncated answer looks like a normal one unless the code checks. State a length each step can meet. (2.11)
- In RAG, keep the source label with every chunk, and give the model an explicit way to say the excerpts don't answer the question. (2.7)

## Scenario patterns

- "Every request repeats the same long document and costs too much": prompt caching, document first, kept byte-identical.
- "Answers miss facts that are in a big manual": retrieval (RAG), not a bigger prompt.
