# Next steps

## Working foundation

[Fieldlight is hosted](https://fieldlight.megan373lab.xyz) separately from this VitePress notebook. Its bounded corpus has two NPS prose sources and seven paraphrase passages. The app answers typed questions with checked checklist wording, expandable source evidence and explicit insufficient-evidence behavior. Public HTTPS and two public answer cases have been checked; wider reliability is not established.

## 1. Compare retrieval with a baseline

Run the same exact-term and paraphrased questions against a simple keyword baseline and Qdrant. Save rankings, returned IDs and expected evidence. Four-of-seven retrieval is selective, but a small successful set alone does not show the vector approach is better. Explain tradeoffs and failures before adding a graph.

## 2. Compare chunk boundaries

Compare heading-based passages with a bounded alternative using the same authorized prose and question set. Verify actual tokenizer lengths rather than assuming word counts are token counts. Preserve source URLs, sections, representation labels and conditional context. The current hand-prepared chunks are not evidence that the best strategy has been found.

## 3. Broaden answer and scope checks

Repeat supported, ambiguous, compound, paraphrased and unanswerable questions. Check whether the fact selector chooses too much, too little or the wrong topic. The conservative waterfall rule can omit secondary topics in a compound question; document that behavior. Test quota/timeouts, restart recovery, public narrow-screen behavior and citation links with actual results.

## 4. Resolve corpus gaps

The Canon R1 manual and original supplementary Canon guides remain candidates, not permission-cleared indexed content. Verify edition and reuse terms before import. Current general NPS guidance must not be relabeled as tested R1 instructions. The contributor night-sky article remains excluded until reuse is established. Expand handheld/low-light coverage only with supporting evidence.

## 5. Finish the research explanation

Read the course handout and student guides, verify AI-prepared claims independently, and record personal takeaways and decision reasons. Keep source facts, assumptions, plans and observations separate. Private career reflection belongs in Canvas. This RAG notebook links into section 2 of the existing combined individual record; group work stays in its separate record.

## Hosting and maintenance

The app runs on the existing course server in a separate Compose project. The static research site remains on GitHub Pages. Provider quotas, Qdrant inactivity behavior, domain renewal, certificate renewal and shared server resources still need monitoring. No new paid provider plan was selected. A foundation deployment does not establish production hardening, sustained uptime or load capacity.

[Review the actual check history](./experiments.md) · [Sources and permissions](./sources.md) · [Tool comparisons](./tools.md)
