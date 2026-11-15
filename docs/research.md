# Research & comparisons

**Research notebook:** includes Megan’s source-specific reading notes below, alongside AI-assisted explanations and proposed comparisons. Executed retrieval and structural chunking comparisons are now linked below; plans and personal reflections are distinguished from observed results.

## How content becomes evidence

Import permitted documents → extract text → clean and deduplicate → preserve document IDs and locations → represent content → retrieve relevant evidence → generate an answer → show source references and check support.

## Vector, graph, and baseline

| Approach | Representation and retrieval | Potential fit | Limitation to examine |
| --- | --- | --- | --- |
| Keyword baseline | Search text using matching terms | Simple, inspectable learning baseline | Paraphrases may miss matching words |
| Vector database | Embed chunks and the question; retrieve similar vectors with metadata | Questions phrased differently from source wording | Similarity does not prove support; model and database access required |
| Graph database | Entities, typed relationships and supporting passages; retrieve facts/paths | Questions involving explicit relationships | Requires a suitable schema and checked relationship extraction |
| Combined | Use graph and vector results for distinct evidence needs | A corpus with both passage and relationship questions | More components and evaluation work |

**Provisional choice: vector retrieval — November 14, 2026.** Megan confirmed this direction after comparing vector and graph approaches. The implemented prototype now uses Qdrant Cloud with MiniLM inference; [tool choices](./tools.md) and [executed comparisons](./comparisons.md) document the evidence and limits. Researching both approaches does not require implementing both.

### My decision and reason

I provisionally chose vector retrieval because my first questions concern explanations and guidance in a small document collection for the Canon EOS R1, focused on landscapes and low light, both handheld and with a tripod. Graph retrieval could explicitly represent relationships between shooting conditions, settings, and effects, but creating and verifying that graph adds work. I will test whether vector retrieval returns sufficient evidence before adding graph retrieval.

### What I compared

- **Vector:** retrieve passages by similarity to the question, retaining source locations and camera-model metadata. Candidate for the first version’s document questions.
- **Graph:** explicitly model entities and relationships so retrieval can follow connected facts. Worth investigating if questions require connections passage retrieval repeatedly misses.
- **Combined:** use both evidence paths, with additional setup and checking. Deferred until an observed need justifies it.

**Check before treating this choice as successful:** compare vector retrieval against a keyword baseline using the same questions. Preserve retrieved passages and inspect support, missing context, and citations. If repeated failures involve connecting facts across sources, investigate graph retrieval alongside simpler changes to chunking and retrieval. The [first paired comparison is now executed](./comparisons.md): the small test supports the provisional choice without establishing universal superiority.

**Contribution:** AI helped phrase this decision; Megan explicitly agreed with its reasoning. This is a confirmed planning decision, not an experimental result.

## Database, model and hosting comparisons

[Read the tool comparison and proposed architecture](./tools.md): Chroma, self-hosted and free-cloud Qdrant, embedding choices, Groq/Gemini generation options, and the course server’s documented limits. The hosted foundation and bounded access/resource checks are recorded there; broader capacity and reliability remain unverified.

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

**Provisional application decision confirmed by Megan:** start with vector retrieval over a small permitted source collection for EOS R1 landscape and low-light questions. A graph remains an alternative if actual checks show that passage retrieval misses required connections. Tool comparisons and limited prose-only permission assessments are recorded separately. Canon sources still await permission clearance.

### What I still need to check

The first keyword/vector comparison and local chunk-boundary comparison are complete. Extend them with independent questions, stronger baselines and retrieval on alternative chunkings; continue checking source support. Reading a comparison does not establish speed or accuracy for my app.

## Further learning notes

For each reading: concept in my own words; small illustrative example; source section; assumption; remaining question; decision it changes. Keep tutorials that teach the system separate from content that the app answers questions about.

## My takeaways from the technical research and checks

**Megan’s responses, recorded November 14, 2026.** These are Megan’s supplied answers to reflection questions about the earlier reading, tool choice, executed comparisons and answer failures. AI organized them and lightly edited wording. In the graph answer, “current graph” was clarified to “current vector approach” because the app does not implement a graph. These reflections do not claim that Megan independently read every photography document or personally executed the AI-labeled checks.

### Why vector retrieval fits my app

Users may ask the same photography question in different ways. Vector retrieval helps the RAG system work with the meaning behind a question rather than relying only on exact keyword matches.

### When I would reconsider graph retrieval

I would reconsider graph retrieval if the app needed to answer more complicated questions involving multiple connected photography concepts that the current vector approach could not easily retrieve.

### What the retrieval comparison tells me

Vector retrieval showed an advantage with differently worded questions, but five straightforward questions and one additional challenge are not enough evidence to say it is always the better option.

### Why I would keep related content together

Keeping related information together helps the app retrieve more complete evidence without losing important context. This supports keeping the current heading-associated passages for this small corpus; it does not establish that they are best for every document.

### What the answer failures taught me

Just because an answer has citations does not mean everything it says is true. We need to verify that the sources actually support the information being provided.

### What I want to test next

I would test whether the app is making things up. Even if it provides citations, I want to make sure the information actually comes from those sources before trusting its answers.

**Planned check, operationalized by AI from Megan’s goal:** use a new question not included in the current test set; compare every displayed claim, number and qualifier with its cited source evidence. Mark a failure if a claim is unsupported, attributed to the wrong passage, or more certain than the evidence. Check the original source when a paraphrase is unclear. This additional check has not been executed or independently verified by Megan. Earlier AI-executed failures and repairs are recorded in [Experiments & checks](./experiments.md).

### Links between sources, results and my decisions

- [My Meilisearch reading notes](#my-notes-vector-and-graph-rag): initial understanding of representations, retrieval and tradeoffs.
- [Executed comparison results](./comparisons.md): evidence supporting the current vector and passage-boundary choices, with explicit limits.
- [Tool comparisons](./tools.md): database, model and resource alternatives.
- [Observed answer failures and retests](./experiments.md): why valid citation IDs alone were not sufficient.

**Changed / checked / next:** added my own explanations of the choices and limits; linked them to source notes and actual results; kept my proposed trust check separate from executed tests. Remaining work includes independent verification of technical explanations and the new source-support check. AI-authored clarifications remain labeled as such.
