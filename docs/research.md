# Research & comparisons

**Research notebook:** includes Megan’s source-specific reading notes below, alongside AI-assisted explanations and proposed comparisons. No retrieval experiments have been executed.

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

## My notes: vector and graph RAG

**Recorded November 14, 2026.** Megan supplied the notes; AI organized them and separated technical clarifications. Source: [Meilisearch’s comparison guide](https://www.meilisearch.com/blog/graph-rag-vs-vector-rag), especially its definitions, pipeline descriptions, and comparison sections. These notes document reading, not a tested implementation.

### My understanding from the reading

- **Vector:** chunks are represented numerically as embeddings. A question is also embedded, similar representations help locate relevant passages, and those passages provide context for an LLM answer. I think of this as the “math of meaning.”
- **Graph:** nodes represent entities, edges describe connections, and nodes can carry several properties. A schema defines allowed types and relationships; entity recognition and resolution can help organize imported information. Connected facts and their sources can provide answer context.
- **Main difference:** vector retrieval searches by similarity, while graph retrieval follows explicit relationships. I see vector retrieval as a candidate for unstructured text and graph retrieval as a candidate when questions require connecting facts.

### Technical clarifications to my original notes

1. **Chunking and embedding are separate steps.** A chunker splits text; an embedding model produces numerical representations. Store the text and source metadata alongside vectors.
2. **Graph distance is not automatically semantic similarity.** A hop counts a relationship traversed. What that connection means depends on the relationship type; nearby nodes are not necessarily similar in meaning.
3. **Graph retrieval does not inherently require query embeddings.** The article illustrates a pipeline that includes embeddings, entity linking, bounded traversal, ranking, and compression. This is one design, not a required sequence for every graph system.
4. **Neither approach guarantees correct answers.** Source quality, extraction, retrieval, and generation still require checks. Claims that vector setup is simpler or graph retrieval supports more complex connections need evaluation against this project’s questions.

Graph-model cross-check: [Neo4j’s graph database introduction](https://neo4j.com/docs/getting-started/graph-database/) describes nodes, relationships, and properties. AI supplied these clarifications; Megan’s confirmation of the revised explanation is pending.

### What this suggests for my photography project

**AI-assisted interpretation, awaiting Megan’s decision:** EOS R1 manual passages may suit vector retrieval for differently worded questions about landscapes and low light. A graph could explicitly connect settings, effects, and shooting conditions, but would require a checked schema and supporting passages. Neither architecture nor database has been chosen; compare tools and actual questions before deciding.

### What I still need to check

Try the same questions with a keyword baseline and the selected approach; inspect retrieved source locations, missing context, and unsupported claims. Reading a comparison does not establish speed or accuracy for my app.

## Further learning notes

For each reading: concept in my own words; small illustrative example; source section; assumption; remaining question; decision it changes. Keep tutorials that teach the system separate from content that the app answers questions about.
