"""Hooks for the Recruiter Finder agent.

Hooks are deterministic guardrails wired into the agent loop. SearchBudgetHook
caps how many times the agent may call search_recruiters in a single turn,
so a vague prompt can't burn the whole search budget.
"""

from strands.hooks import (
    HookProvider, HookRegistry,
    BeforeInvocationEvent, BeforeToolCallEvent,
)


class SearchBudgetHook(HookProvider):
    """Caps search_recruiters at max_calls per agent invocation."""

    def __init__(self, max_calls: int = 4):
        self.max_calls = max_calls
        self.counts: dict[str, int] = {}

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.reset)
        registry.add_callback(BeforeToolCallEvent, self.check)

    def reset(self, event: BeforeInvocationEvent) -> None:
        """Reset counts at the start of each invocation."""
        self.counts = {}
        print("[HOOK] 🔄 Search budget reset")

    def check(self, event: BeforeToolCallEvent) -> None:
        """Check and enforce the budget before each tool call."""
        name = event.tool_use["name"]
        self.counts[name] = self.counts.get(name, 0) + 1
        print(f"[HOOK] 📊 {name}: call {self.counts[name]}/{self.max_calls}")

        if self.counts[name] > self.max_calls:
            event.cancel_tool = (
                f"'{name}' hit the {self.max_calls}-call budget for this turn. "
                "Do NOT call this tool again. Work with the results you already have."
            )
            print(f"[HOOK] 🚫 BLOCKED: {name} exceeded budget!")
