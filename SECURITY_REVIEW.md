# 🔒 SkillProof AI — Complete Security Architecture & Threat Review

> **Audit Type**: Read-only structural security architecture review and threat model across both frontend and backend nodes.

---

## 1. Security Architecture & Threat Matrix

| Threat Description | Affected Module | Current Implemented Protection | Remaining Vulnerability | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **Server-Side Request Forgery (SSRF)** | `services/validators.py` & Backend Git Cloner | Strict HTTPS-only validation; whitelist hostname check (`github.com` only); rejection of deceptive domains. | DNS rebinding if backend uses low-level sockets instead of standard HTTP libraries. | **Medium** |
| **Path Traversal / Zip-Slip** | Backend Git / Archive Extractor | Target paths constrained within isolated scratch workspaces (`os.path.abspath` check). | Symbolic links inside cloned repositories pointing outside the sandbox directory. | **High** |
| **Remote Code Execution (RCE)** | Backend Pytest Test Runner | Tests executed in dedicated subprocesses with strict execution timeouts (15s). | Full OS-level container isolation (Docker / gVisor) required to prevent container breakouts. | **Critical** |
| **Tampered Credential Forgery** | `services/session_manager.py` & Credential Viewer | HMAC-SHA256 signature calculated over canonicalized JSON payload. | Symmetric secret key is shared with the issuer; third-party verification requires asymmetric cryptography. | **High** |
| **Approval Gate Bypass** | `components/reviewer_console.py` & API Router | Backend rejects `POST /api/credential/issue` if `approval_status != 'approved'`. | Direct manipulation of in-memory session state if backend authentication is omitted in development. | **High** |
| **Cross-Candidate Data Leakage**| Vector Database (ChromaDB) | Mandatory `$and` metadata filtering on `session_id` and `commit_sha`. | Accidental omission of session filter in custom ad-hoc RAG queries. | **Medium** |
| **Command Injection via Git** | Backend Git CLI wrapper | Git commands executed with parameterized arguments (no `shell=True`). | Passing untrusted branch names or flags without sanitization. | **High** |
| **Secret & Credential Exposure** | Git Repository & Environment | Secrets loaded via environment variables (`SKILLPROOF_*`); `.gitignore` excludes `.env`. | Hardcoded development fallback key in demo mode (`SECRET_KEY = "..."`). | **Medium** |

---

## 2. In-Depth Analysis of Critical Security Vectors

### 1. SSRF & URL Validation
The validation implemented in [validators.py](file:///c:/Users/K.R.NEERAJ/Downloads/ziro%20frontend/skillproof/frontend/services/validators.py) employs defensive safeguards:
- **HTTPS Enforcement**: Rejects unencrypted `http://` schemes.
- **Hostname Whitelisting**: Allows only exact `github.com` or `www.github.com`.
- **Rejection of Deceptive Domains**: Explicitly blocks domain spoofing techniques like `https://github.com.attacker.com/repo`.
- **Reserved Keyword Blacklisting**: Blocks internal administrative routes like `https://github.com/login/repo`.

### 2. Untrusted Code Execution Sandboxing
When a candidate submits a repository, its test suite (`pytest`) must be executed to verify implementation claims. **Executing untrusted code is the highest risk in the platform**:
- **Current Development Implementation**: Subprocess invocation with `timeout=15` and restricted working directory.
- **Production Architecture Requirement**: Pytest must run inside a stateless **Docker container** or **gVisor microVM** configured with:
  - `network_mode: none` (Zero outbound internet access to prevent data exfiltration).
  - `read_only: true` (Read-only root filesystem).
  - `cap_drop: ALL` (Drop all Linux kernel capabilities).
  - `memory: 512MB` and `cpus: 1.0` (Prevent resource exhaustion / DoS fork-bombs).

### 3. Cryptographic Verification: HMAC-SHA256 vs Asymmetric PKI

#### How HMAC-SHA256 Works Currently
SkillProof AI currently signs verifiable credentials using **HMAC-SHA256**:
$$\text{Signature} = \text{HMAC-SHA256}(K_{\text{secret}}, \text{CanonicalJSON}(\text{Payload}))$$

- **Verification**: The verifier recomputes the HMAC digest using the same secret key $K_{\text{secret}}$ and compares it via constant-time digest comparison (`hmac.compare_digest`).
- **Limitation**: HMAC uses a **symmetric secret key**. To independently verify a credential, the employer must possess the secret key. If the secret key is shared with employers, any employer could forge valid credentials for any candidate!

#### Production Upgrade: Asymmetric Cryptography (ECDSA / Ed25519)
In production (v2 roadmap), SkillProof AI will upgrade to **Asymmetric Digital Signatures**:
1. The **SkillProof Verification Authority** retains a private key ($SK$) stored in a secure Hardware Security Module (HSM).
2. The credential is signed with the private key:
   $$\text{Signature} = \text{Sign}_{SK}(\text{Hash}(\text{Payload}))$$
3. The **Public Key ($PK$)** is published globally (e.g., via DNS TXT record or `.well-known/pki/skillproof.pub`).
4. **Third-party employers can independently verify the credential using only the public key without any ability to forge signatures**:
   $$\text{Verify}_{PK}(\text{Payload}, \text{Signature}) \in \{\text{True}, \text{False}\}$$
