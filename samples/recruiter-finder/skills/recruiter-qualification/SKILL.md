---
name: recruiter-qualification
description: How to qualify recruiters before shortlisting them - niche focus, placement volume, response rate, and red flags - with a 1-5 fit score.
---

# Recruiter Qualification

Follow these steps before adding a recruiter to the shortlist:

1. **Check the niche.** A strong recruiter has a specific specialty or industry focus. Generalists ("anything and everything") are a red flag.

2. **Check placement volume.** Use `get_placements` to see recent roles. More than ~8 placements in 12 months with relevant titles is a good sign. Recent placements (last 3 months) count more than old ones.

3. **Check responsiveness.** Prefer a response rate above 65% and a fast time-to-first-reply. Below ~40% response rate is a red flag.

4. **Check relevance of placements.** The companies and levels in `get_placements` should match what the user is targeting. An in-house recruiter only helps if their company is the target.

5. **Score the fit 1-5** and state the score and one-line reasoning before recommending a shortlist action.

6. **Add to the shortlist** with `add_to_shortlist` using a note that captures why they fit (or don't).

## Important Notes
- Never shortlist a recruiter without checking their profile with `get_recruiter_details` first.
- Always surface red flags to the user instead of silently recommending a weak match.
- Keep the qualification summary short: score, two or three evidence points, one action.
