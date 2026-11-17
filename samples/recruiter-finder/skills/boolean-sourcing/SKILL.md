---
name: boolean-sourcing
description: How to build Boolean search strings to find recruiters on LinkedIn, Google, and job boards when the directory search is too narrow.
---

# Boolean Sourcing

Use when the user wants to find recruiters beyond what `search_recruiters` returns, or asks for search strings they can paste into LinkedIn or Google.

## Steps

1. **Anchor on the role.** Start with the exact title and common variants:
   `("backend engineer" OR "platform engineer" OR "distributed systems")`

2. **Add the target industry or domain** as keywords:
   `("fintech" OR "payments" OR "financial services")`

3. **Add recruiter signals** so you match people, not job posts:
   `(recruiter OR talent OR sourcing OR "talent acquisition")`

4. **Scope by location** only if the user has a location constraint:
   `(London OR "United Kingdom")`

5. **Assemble and offer** the final string to the user, e.g.:
   `site:linkedin.com/in ("backend engineer" OR "platform") (fintech OR payments) (recruiter OR "talent acquisition")`

## Important Notes
- Prefer `search_recruiters` first; only produce Boolean strings when the directory has no good matches or the user asks for them.
- Keep strings copy-paste ready and explain each clause in one line.
- Do not invent metrics about how many results a string will return.
