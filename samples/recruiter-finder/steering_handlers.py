import re

from strands.vended_plugins.steering import (
    SteeringHandler, LLMSteeringHandler,
    Proceed, Guide, ToolSteeringAction,
    LedgerProvider,
)


class ShortlistWorkflowHandler(SteeringHandler):
    """Deterministic handler: enforce the shortlisting workflow.

    Rules:
    1. Must search the directory before shortlisting anyone
    2. Must check a recruiter's full profile before shortlisting them
    3. Never shortlist the same recruiter twice
    """

    name = "shortlist-workflow"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "add_to_shortlist":
            return Proceed(reason="Not a shortlist operation")

        print("[STEERING] 🔍 add_to_shortlist attempted — checking workflow...")

        # Get execution history through managed ledger
        ledger = self.steering_context.data.get("ledger", {})
        tool_calls = ledger.get("tool_calls", [])
        print(f"[STEERING] 📋 Ledger has {len(tool_calls)} tool calls: {[c.get('tool_name', '?') + ':' + c.get('status', '?') for c in tool_calls]}")

        # Must search the directory first
        searched = any(
            c["tool_name"] == "search_recruiters" and c["status"] == "success"
            for c in tool_calls
        )
        if not searched:
            print("[STEERING] ⚠️  Blocked: must search the directory first")
            return Guide(
                reason="You must search the directory with search_recruiters "
                "before adding anyone to the shortlist."
            )

        # Must inspect the full profile before shortlisting
        checked = any(
            c["tool_name"] == "get_recruiter_details" and c["status"] == "success"
            for c in tool_calls
        )
        if not checked:
            print("[STEERING] ⚠️  Blocked: must check the profile first")
            return Guide(
                reason="You must check the recruiter's profile with get_recruiter_details "
                "before adding them to the shortlist."
            )

        # Never shortlist the same recruiter twice
        recruiter_id = tool_use.get("input", {}).get("recruiter_id", "")
        already_shortlisted = any(
            c["tool_name"] == "add_to_shortlist"
            and c["status"] == "success"
            and c.get("input", {}).get("recruiter_id") == recruiter_id
            for c in tool_calls
        )
        if already_shortlisted:
            print(f"[STEERING] ⚠️  Blocked: {recruiter_id} is already on the shortlist")
            return Guide(
                reason=f"{recruiter_id} is already on the shortlist. "
                "Don't add duplicates."
            )

        print("[STEERING] ✅ Shortlist workflow validated — proceeding")
        return Proceed(reason="Shortlist workflow validated")


class OutreachToneHandler(LLMSteeringHandler):
    name = "outreach-tone"

    def __init__(self):
        super().__init__(
            system_prompt="""You are evaluating a recruiter-outreach assistant's responses.
Ensure the agent follows these communication guidelines:

- Never invent or imply a guaranteed response rate, interview, or placement
- Never fabricate a recruiter's details — only use what the tools returned
- Outreach must be personalized (no "Dear Sir/Madam", no mass-blast language)
- One clear ask per message; keep it short (under 150 words)
- No attachments, tracking links, or pushy follow-up threats
- Warn the user about recruiters with red flags (no niche, very low response
  rate) instead of pitching them as strong matches
- If a recruiter is a weak match, say so and explain why

If the agent violates any of these, provide specific guidance on what to fix."""
        )

    async def steer_after_model(self, **kwargs):
        print("[TONE] 🔍 Evaluating agent response...")
        result = await super().steer_after_model(**kwargs)
        action_type = type(result).__name__
        print(f"[TONE] {'✅ Tone OK' if action_type == 'Proceed' else '⚠️  Tone guided: ' + getattr(result, 'reason', '')}")
        return result


tone_handler = OutreachToneHandler()
