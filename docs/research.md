# Research & comparisons

**Initial draft explanations and proposed comparisons.** Add your own understanding and source-specific notes as you work through the readings.

## How content becomes evidence

Import permitted documents → extract text → clean and deduplicate → preserve document IDs and locations → represent content → retrieve relevant evidence → generate an answer → show source references and check support.

## Vector, graph, and baseline

| Approach | Representation and retrieval | Potential fit | Limitation to examine |
| --- | --- | --- | --- |
| Keyword baseline | Search text using matching terms | Simple, inspectable learning baseline | Paraphrases may miss matching words |
| Vector database | Embed chunks and the question; retrieve similar vectors with metadata | Questions phrased differently from source wording | Similarity does not prove support; model and database access required |
| Graph database | Entities, typed relationships and supporting passages; retrieve facts/paths | Questions involving explicit relationships | Requires a suitable schema and checked relationship extraction |
| Combined | Use graph and vector results for distinct evidence needs | A corpus with both passage and relationship questions | More components and evaluation work |

**Decision pending:** compare actual corpus questions before selecting a tool. No implementation approach has been chosen. Researching both approaches does not require implementing both.

## Chunking

Chunking divides extracted content into retrievable pieces. Compare paragraph/heading boundaries with a fixed-size rule on the same document. Preserve document ID, title, section, source URL and a stable passage identifier. Inspect whether evidence gets split or unrelated topics get combined. A word-count prototype must not be described as token-based chunking.

Learning source: [Weaviate’s chunking guide](https://weaviate.io/blog/chunking-strategies-for-rag). Add the section you read, your explanation, and a concrete example; reading completion is not recorded yet.

## Embeddings

An embedding is a numerical representation created by a model for similarity comparisons. In a vector path, record the real embedding model/version, dimensions, and configuration. Embed questions using a compatible model. Stored vectors are not proof that an answer is correct.

## Entities and relationships

A graph model represents entities as nodes and typed connections as relationships. Illustrative example: a document → cites → another document. Define what each relationship means and retain the supporting source location. This is a modeling example, not an extracted fact.

Learning source: [Neo4j’s graph database introduction](https://neo4j.com/docs/getting-started/graph-database/).

## Import and content management

Keep a source manifest, parse text, normalize formatting, detect duplicate documents, and retain source locations. Reimport should update stable document records rather than silently duplicate content. Import/admin permissions must be checked on the server.

## My learning notes — to complete

For each reading: concept in my own words; small illustrative example; source section; assumption; remaining question; decision it changes. Keep tutorials that teach the system separate from content that the app answers questions about.
