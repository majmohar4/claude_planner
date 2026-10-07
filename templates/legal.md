# legal.md — privacy, legal, cookies, GDPR. Not legal advice; EU/Slovenia default. Tick or mark `n/a · why` per line. Any `[lawyer]` item that applies → lawyer before public launch.
Researched 2026-10. `[verify]` = uncertain/changing law: re-check at launch. Digital Omnibus (Nov 2025 proposal: cookie rules → GDPR, AI Act delays) — check if adopted.

## Planning (decide in P, log in decisions.md)
- [ ] Audience: B2C / B2B · paid / free · EU / US · minors possible? · AI features? · special-category data (health, biometrics…)? → picks which sections apply.
- [ ] Data inventory in data-model.md: each field · purpose · lawful basis (contract / legit interest + short LIA / consent / legal obligation) · retention · processor.
- [ ] Privacy by design: minimum fields, optional data only when needed, private defaults, encryption, PII separated, EU hosting regions preferred.
- [ ] Analytics choice: cookieless self-hosted (Plausible, Umami, Matomo anonymous) or consent-gated. GA4 = consent required.

## Documents (every public app; reachable from every page + in-app)
- [ ] **Privacy Policy** (GDPR Art.13/14): controller identity + contact · purposes + lawful basis each · legitimate interests · recipients/processors · non-EU transfers + safeguard (DPF/SCCs) · retention · rights (access, rectify, erase, restrict, port, object) · withdraw consent · complain to supervisory authority (SI: Informacijski pooblaščenec) · statutory/contractual need + consequence · automated decisions/profiling · data source (if not from user) · AI providers used + where prompts go.
- [ ] **Terms of Service**: scope, accounts, acceptable use, IP, termination, governing law, warranty disclaimer ("as is", no guarantee of availability/fitness), limitation of liability.
  - B2C limits: cannot exclude liability for death/injury, intent, gross negligence, fraud; cannot waive consumer rights (digital-content conformity Dir. 2019/770, 14-day withdrawal); unfair terms void (Dir. 93/13). Cap at fees paid = B2B only.
- [ ] **Cookie Policy**: every cookie/storage/SDK — name · purpose · duration · first/third party.
- [ ] **Imprint / legal notice** (e-commerce Dir. Art.5; SI ZEPT) for any commercial service incl. s.p.: name, address, email, register no., VAT ID, regulator.
- [ ] **Open-source notices** page (license texts/attributions; automated license check; GPL/AGPL obligations reviewed).
- [ ] Mobile: Apple standard EULA (or custom) · Play: none required.
- [ ] Paid B2C `[lawyer]`: pre-contract info · 14-day withdrawal (digital: lost only with express consent + acknowledgement + started) · "pay now" button label · total price + renewal terms · cancel as easy as sign-up · withdrawal function `[verify]` (Dir. 2023/2673, ~Jun 2026).

## Cookies / ePrivacy (Art.5(3): covers cookies, localStorage, SDK IDs, fingerprinting)
- [ ] Nothing non-essential loads before consent (verify in network tab + Playwright test).
- [ ] Banner: Reject all as prominent as Accept all on first layer · granular per purpose · no pre-ticks, no cookie wall, no dark patterns · persistent "cookie settings" link · withdraw as easy as grant.
- [ ] Consent log: timestamp · policy version · choices · ID; re-ask on change / ~6–12 months. Use an established CMP.
- [ ] Exempt (no consent): session/auth, CSRF, load balancing, cart, consent cookie, user-set language. NOT exempt: analytics (default), ads, A/B tests, social/YouTube/Maps embeds (use click-to-load).

## GDPR operations
- [ ] Art.30 records (1-page sheet: purpose · data · basis · processors · retention).
- [ ] DPA (Art.28) accepted + filed for EVERY processor: hosting, DB, email, auth, analytics, error monitoring, payments, CDN, AI APIs. Subprocessor list kept.
- [ ] US processors: on EU-US DPF list, else SCCs + transfer impact assessment `[verify]` (DPF upheld Sep 2025, appeal possible).
- [ ] Rights flows built in-app: export (JSON) · delete account · rectify · object. Respond ≤1 month; verify identity; keep legally required data (SI accounting: 10 years).
- [ ] Retention automated: inactive accounts, logs, backups.
- [ ] Breach runbook (1 page): notify authority ≤72h unless unlikely risk · users if high risk · breach log.
- [ ] DPIA if large-scale sensitive data, systematic monitoring, significant profiling, novel tech `[lawyer]`.
- [ ] DPO needed? (usually no for solo dev) — decision recorded.
- [ ] Minors: SI digital consent age 15 (ZVOP-2; other states 13–16). Under-age → parental consent, no profiling/targeted ads (DSA Art.28). Minors as target audience `[lawyer]`.
- [ ] Security = legal duty (Art.32): HTTPS, encryption at rest, proper password hashing, MFA on admin, least-privilege DB, access logs, patching, tested backups — documented. Audit per process rule 16.

## App stores
- [ ] Apple: privacy nutrition labels · privacy policy URL · `PrivacyInfo.xcprivacy` (data types + required-reason APIs; SDK manifests) · in-app account deletion if accounts exist (5.1.1(v); "email us" not enough) · Sign in with Apple rules `[verify]`.
- [ ] Google Play: Data safety form · in-app deletion + web deletion URL · privacy policy link · target API level.
- [ ] Labels/forms match actual SDKs + policy (mismatch = rejection).

## Other
- [ ] Accessibility: European Accessibility Act (since 28 Jun 2025) for consumer e-commerce, banking, e-books, ticketing… Micro-enterprise exemption (<10 staff AND ≤€2M) = services only, document it. Build WCAG 2.2 AA anyway.
- [ ] AI features: tell users they talk to AI; label AI-generated content (AI Act Art.50, ~Aug 2026 `[verify]`); no prohibited practices; AI that profiles/decides about people `[lawyer]`.
- [ ] Email marketing: opt-in (double opt-in best) · proof of consent · unsubscribe in every mail · soft opt-in only for existing customers + similar products. Transactional mail needs no marketing consent.
- [ ] US users: CCPA/CPRA only above thresholds; COPPA if knowingly <13.
- [ ] Cyber Resilience Act for distributed products with digital elements (reporting Sep 2026, full Dec 2027) `[verify]`.

## Generator vs lawyer
Generator/template OK: privacy + cookie policy for standard stack, ToS skeleton, imprint, AUP, OSS notices, CMP banner, Art.30 sheet, breach runbook, vendor DPAs — always checked against the Art.13 list and the real stack.
`[lawyer]`: paid B2C flows, special-category data, minors as audience, DPIA, AI profiling, marketplaces/UGC (DSA), regulated sectors, B2B liability caps, a breach, SI-specific employment/CCTV/consumer law.
