# Recruiter Finder agent

A custom Strands Agents harness that finds, qualifies, and shortlists recruiters for a
job search, then drafts personalized outreach. Same harness pattern as the customer
service modules, different domain.

## Stages

| Stage | What it maps to | With |
|---|---|---|
| Build the harness | Agent loop + tools (Module 1), hooks (Module 2), skills + steering (Module 3), session memory (Module 4) | `chat.py` |
| Run the harness | Managed compute, memory, identity, observability (Module 5) | `main.py` + AgentCore |
| Go further (optional) | Multi-agent delegation and evals (Modules 6-7) | See module READMEs — same patterns apply |

## The harness

- `recruiter_tools.py` — the tool layer: `search_recruiters`, `get_recruiter_details`,
  `get_placements`, `add_to_shortlist`, `view_shortlist` over a mock recruiter directory.
- `hooks.py` — `SearchBudgetHook` caps `search_recruiters` calls per turn.
- `skills/` — `boolean-sourcing` (search strings), `recruiter-qualification`
  (fit scoring + red flags), `outreach` (personalized messages).
- `steering_handlers.py` — `ShortlistWorkflowHandler` enforces search → inspect →
  shortlist ordering and blocks duplicates; `tone_handler` (LLM steering) guards
  outreach against invented claims and spammy language.
- `chat.py` — assembles all of it on `SnapshotSessionManager` +
  `context_manager="auto"` so sessions persist across runs.

## Run it

```bash
cd samples/recruiter-finder
pip install -r requirements.txt     # or: uv pip install -r requirements.txt
python chat.py
python chat.py --session-id alice   # resume/keep a named session
```

Try: *"Find me recruiters who place backend engineers in fintech."* Then ask it to
qualify the matches, shortlist the good ones, and draft outreach.

## Deploy to AgentCore (Module 5 pattern)

Requires AWS credentials with Amazon Bedrock access (region `us-east-1`) and the
AgentCore CLI (`sudo npm install -g @aws/agentcore@1.0.1 --ignore-scripts`):

```bash
agentcore create --name recruitfind --template empty
cd recruitfind && agentcore add runtime --name RecruitFind --language python
# copy main.py, recruiter_tools.py, steering_handlers.py, hooks.py, skills/
# into app/RecruitFind/, then uv init --bare + uv add
agentcore deploy
agentcore invoke --runtime RecruitFind --payload '{"prompt": "Find recruiters who place data scientists in health tech"}'
agentcore remove all --yes && agentcore deploy --yes   # cleanup
```

Never commit generated `agentcore/` or `app/RecruitFind/` folders.
