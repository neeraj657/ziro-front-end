# 📖 SkillProof AI — Complete Technical Glossary & Terms

> **Reference**: Comprehensive definitions of engineering, cryptographic, machine learning, and agentic concepts used across the SkillProof AI platform.

---

## 1. Agentic AI & Orchestration

### Agentic AI
An artificial intelligence paradigm where systems operate with autonomy to plan tasks, invoke tools, inspect environment feedback, reflect on outcomes, and dynamically adjust execution strategies without rigid hardcoded pipelines.

### LangGraph
A specialized library created by LangChain for orchestrating stateful, multi-actor LLM workflows using graph structures (nodes, directed edges, and conditional branches). Unlike linear chains, LangGraph natively supports cyclic workflows, human-in-the-loop checkpoints, and durable persistence.

### GraphState
The shared, immutable or append-only dictionary passed between all nodes in a LangGraph execution graph. In SkillProof AI, `GraphState` preserves the candidate session, discovered code files, AST metrics, test results, and audit traces.

### Adaptive Re-Planning
The agent's ability to evaluate intermediate observations (e.g., discovering unreached code branches or low unit test coverage) and automatically dispatch additional investigation sub-tasks before concluding an evaluation.

### Human-in-the-Loop (HITL)
A governance architecture where autonomous agents are intentionally prevented from executing irreversible actions (such as issuing a certified skill credential) until a designated human supervisor (Auditor) inspects the dossier and grants explicit approval.

---

## 2. Static Code Analysis & Repository Intelligence

### Abstract Syntax Tree (AST)
A tree representation of the syntactic structure of source code written in a programming language. In SkillProof AI, the Python `ast` module parses candidate code to inspect class definitions, method signatures, inheritance polymorphism, and docstrings without executing the code.

### Cyclomatic Complexity
A quantitative software engineering metric measuring the number of linearly independent paths through a program's source code (calculated from conditional branches like `if`, `for`, `while`). Lower complexity signifies modular, maintainable code.

### Code Provenance & Git Forensics
The chronological audit of repository commits, author signatures, commit intervals, and line addition/deletion patterns to evaluate whether code was developed incrementally over days/weeks or pasted as a single bulk dump.

### Bulk Commit Dump ("Paste Pattern")
A forensic anomaly where thousands of lines of complex code are introduced in a single commit immediately prior to submission, often indicating that the candidate copied an existing codebase rather than developing it organically.

---

## 3. Retrieval-Augmented Generation (RAG) & Vector Search

### Retrieval-Augmented Generation (RAG)
An architectural technique that enhances LLM generation by retrieving relevant domain documents or code snippets from an external knowledge base (vector database) and feeding them into the LLM context prompt to prevent hallucination.

### ChromaDB
An open-source, lightweight embedding and vector database used in SkillProof AI to store, index, and query candidate source code chunks using vector similarity.

### Semantic Code Chunking
Splitting source code along semantic syntax boundaries (functions, classes, modules) rather than arbitrary token lengths, ensuring that complete functions and their associated docstrings remain intact.

### Cosine Similarity
A mathematical metric that measures the cosine of the angle between two multi-dimensional vectors in inner product space:
$$\text{Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$
Used to identify code chunks semantically related to candidate skill claims.

---

## 4. Cryptography & Security

### HMAC-SHA256
Hash-based Message Authentication Code using the SHA-256 cryptographic hash function. Combines a secret cryptographic key with a message payload to provide both data integrity and data origin authenticity.

### Verifiable Credential
A tamper-evident digital certificate containing candidate metadata, verified skills, and scores, signed cryptographically so that employers can verify its authenticity without consulting a central authority.

### Canonical Serialization
The process of serializing a JSON object into a deterministic string (e.g. sorting dictionary keys alphabetically) so that two identical payloads always produce the exact same cryptographic hash.

### Server-Side Request Forgery (SSRF)
A web security vulnerability that allows an attacker to induce a server to make HTTP requests to an unintended destination (e.g. internal network services or loopback addresses).

---

## 5. Model Evaluation & Benchmarks

### Precision
The ratio of correctly verified candidates (True Positives) to all candidates predicted as verified (True Positives + False Positives):
$$\text{Precision} = \frac{TP}{TP + FP}$$

### Recall (Sensitivity)
The ratio of correctly verified candidates (True Positives) to all genuinely qualified candidates (True Positives + False Negatives):
$$\text{Recall} = \frac{TP}{TP + FN}$$

### F1-Score
The harmonic mean of precision and recall, providing a balanced metric when evaluating asymmetric verification datasets:
$$F1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### Confusion Matrix
A $2 \times 2$ table comparing actual ground truth against predicted outcomes across True Negatives ($TN$), False Positives ($FP$), False Negatives ($FN$), and True Positives ($TP$).
