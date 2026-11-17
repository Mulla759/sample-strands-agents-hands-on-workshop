"""
Recruiter search tools for the Recruiter Finder agent.

These mock tools simulate a recruiting research backend: a directory of
recruiters you can search, inspect, and shortlist. Swap the mock data for a
real backend (LinkedIn API, CRM, ATS) without changing the agent harness.
"""

from strands import tool

# --- Mock recruiter directory ---

RECRUITERS = {
    "R-2001": {
        "name": "Dana Whitfield",
        "agency": "TalentBridge Partners",
        "title": "Senior Technical Recruiter",
        "industry": "tech",
        "specialties": ["backend engineering", "platform", "distributed systems"],
        "location": "Remote (US)",
        "placements_last_12_months": 18,
        "response_rate": 0.82,
        "avg_time_to_first_reply_hours": 6,
        "contact": {"email": "dana@talentbridge.io", "linkedin": "linkedin.com/in/danawhitfield"},
        "notes": "Highly responsive; strong network in staff+ backend roles.",
    },
    "R-2002": {
        "name": "Priya Raman",
        "agency": "HealthHire Collective",
        "title": "Principal Recruiter, Clinical Ops",
        "industry": "healthcare",
        "specialties": ["clinical operations", "health tech", "nursing leadership"],
        "location": "Boston, MA",
        "placements_last_12_months": 12,
        "response_rate": 0.74,
        "avg_time_to_first_reply_hours": 24,
        "contact": {"email": "priya@healthhire.co", "linkedin": "linkedin.com/in/priyaraman"},
        "notes": "Deep healthcare network; prefers warm intros.",
    },
    "R-2003": {
        "name": "Marcus Bell",
        "agency": "FinStaff Search",
        "title": "Director, Front Office Recruiting",
        "industry": "finance",
        "specialties": ["quant", "trading", "risk"],
        "location": "New York, NY",
        "placements_last_12_months": 9,
        "response_rate": 0.61,
        "avg_time_to_first_reply_hours": 48,
        "contact": {"email": "marcus@finstaff.com", "linkedin": "linkedin.com/in/marcusbell"},
        "notes": "Works mostly with hedge funds; selective about candidates.",
    },
    "R-2004": {
        "name": "Sofia Delgado",
        "agency": "Northwind Talent",
        "title": "Technical Sourcer",
        "industry": "tech",
        "specialties": ["frontend", "design systems", "mobile"],
        "location": "Austin, TX",
        "placements_last_12_months": 4,
        "response_rate": 0.55,
        "avg_time_to_first_reply_hours": 72,
        "contact": {"email": "sofia@northwindtalent.com", "linkedin": "linkedin.com/in/sofiadelgado"},
        "notes": "Early-career sourcer; high volume, less senior-level focus.",
    },
    "R-2005": {
        "name": "James Okafor",
        "agency": "TalentBridge Partners",
        "title": "Recruiting Manager, AI/ML",
        "industry": "tech",
        "specialties": ["machine learning", "MLOps", "data engineering"],
        "location": "Remote (EU/US)",
        "placements_last_12_months": 21,
        "response_rate": 0.79,
        "avg_time_to_first_reply_hours": 12,
        "contact": {"email": "james@talentbridge.io", "linkedin": "linkedin.com/in/jamesokafor"},
        "notes": "Best match for AI/ML roles; runs a monthly talent newsletter.",
    },
    "R-2006": {
        "name": "Emily Zhang",
        "agency": "In-house — Meridian Health",
        "title": "Senior Talent Partner",
        "industry": "healthcare",
        "specialties": ["health tech", "product", "data science in health"],
        "location": "San Francisco, CA",
        "placements_last_12_months": 15,
        "response_rate": 0.88,
        "avg_time_to_first_reply_hours": 4,
        "contact": {"email": "emily.zhang@meridianhealth.com", "linkedin": "linkedin.com/in/emilyzhang"},
        "notes": "In-house; hires for one company only — great if Meridian is the target.",
    },
    "R-2007": {
        "name": "Tom Alvarez",
        "agency": "Generic Staffing Co.",
        "title": "Recruiter",
        "industry": "general",
        "specialties": ["anything and everything"],
        "location": "Remote",
        "placements_last_12_months": 2,
        "response_rate": 0.21,
        "avg_time_to_first_reply_hours": 168,
        "contact": {"email": "tom@genericstaffing.example", "linkedin": "linkedin.com/in/tomalvarez"},
        "notes": "No niche focus; very low response rate; sends mass mailings.",
    },
    "R-2008": {
        "name": "Aisha Khan",
        "agency": "Northwind Talent",
        "title": "Lead Recruiter, Fintech",
        "industry": "finance",
        "specialties": ["fintech", "payments", "backend engineering"],
        "location": "London, UK (also US roles)",
        "placements_last_12_months": 11,
        "response_rate": 0.69,
        "avg_time_to_first_reply_hours": 36,
        "contact": {"email": "aisha@northwindtalent.com", "linkedin": "linkedin.com/in/aishakhan"},
        "notes": "Fintech specialist; strong payments network in Europe.",
    },
}

PLACEMENTS = {
    "R-2001": [
        {"company": "Lumina Systems", "role": "Staff Backend Engineer", "level": "Staff", "months_ago": 1},
        {"company": "Arcwave", "role": "Senior Platform Engineer", "level": "Senior", "months_ago": 4},
        {"company": "Gridline", "role": "Principal Engineer", "level": "Principal", "months_ago": 7},
    ],
    "R-2002": [
        {"company": "Meridian Health", "role": "Director of Clinical Ops", "level": "Director", "months_ago": 2},
        {"company": "CarePilot", "role": "Senior Product Manager", "level": "Senior", "months_ago": 5},
    ],
    "R-2003": [
        {"company": "Halcyon Capital", "role": "Quantitative Researcher", "level": "VP", "months_ago": 3},
        {"company": "Vantage Trading", "role": "Risk Analyst", "level": "Associate", "months_ago": 8},
    ],
    "R-2004": [
        {"company": "Brightcart", "role": "Frontend Engineer", "level": "Mid", "months_ago": 6},
    ],
    "R-2005": [
        {"company": "Nimbus AI", "role": "ML Engineer", "level": "Senior", "months_ago": 2},
        {"company": "TensorForge", "role": "MLOps Lead", "level": "Lead", "months_ago": 3},
        {"company": "Pollen Robotics", "role": "Head of Data", "level": "Head", "months_ago": 9},
    ],
    "R-2006": [
        {"company": "Meridian Health", "role": "Senior Data Scientist", "level": "Senior", "months_ago": 1},
        {"company": "Meridian Health", "role": "Staff Product Manager", "level": "Staff", "months_ago": 6},
    ],
    "R-2007": [
        {"company": "Various", "role": "Entry-level temp roles", "level": "Entry", "months_ago": 12},
    ],
    "R-2008": [
        {"company": "SwiftPay", "role": "Senior Backend Engineer", "level": "Senior", "months_ago": 2},
        {"company": "LedgerLoop", "role": "Payments Platform Lead", "level": "Lead", "months_ago": 5},
    ],
}

# Shortlist survives across agent turns but not across processes (the session
# manager persists the conversation; this is the in-memory working set).
SHORTLIST: dict[str, str] = {}


def _matches(recruiter: dict, role: str, industry: str, location: str) -> bool:
    """Simple keyword matching against the mock directory."""
    haystack = " ".join(
        recruiter["specialties"] + [recruiter["industry"], recruiter["location"], recruiter["agency"]]
    ).lower()
    for term in (role, industry, location):
        if term and term.lower() not in haystack:
            return False
    return True


def _summary_line(recruiter_id: str, recruiter: dict) -> str:
    return (
        f"{recruiter_id} | {recruiter['name']} — {recruiter['title']} @ {recruiter['agency']} | "
        f"{recruiter['industry'].title()} | {recruiter['location']} | "
        f"{recruiter['placements_last_12_months']} placements | "
        f"{int(recruiter['response_rate'] * 100)}% response rate"
    )


# --- Tools ---


@tool
def search_recruiters(role: str, industry: str, location: str) -> str:
    """Search the recruiter directory for recruiters matching a role, industry,
    and location. Every term narrows the search; leave a term empty to skip it.

    Args:
        role: Role or skills to search for (e.g. "backend engineer", "data science")
        industry: Industry to filter by (e.g. "tech", "healthcare", "finance")
        location: Location to filter by (e.g. "New York", "Remote (US)")
    """
    matches = [
        (rid, rec)
        for rid, rec in RECRUITERS.items()
        if _matches(rec, role, industry, location)
    ]
    if not matches:
        return (
            "No recruiters matched those terms. Try broadening the search: "
            "use a more generic role, leave the industry or location empty, "
            "or search by a specialty keyword instead."
        )
    lines = [f"{len(matches)} recruiter(s) found:"] + [
        _summary_line(rid, rec) for rid, rec in matches
    ]
    return "\n".join(lines)


@tool
def get_recruiter_details(recruiter_id: str) -> str:
    """Get the full profile of a single recruiter.

    Args:
        recruiter_id: The recruiter ID (e.g. R-2001)
    """
    recruiter = RECRUITERS.get(recruiter_id)
    if not recruiter:
        return f"No recruiter found with ID {recruiter_id}"
    return (
        f"{recruiter['name']} ({recruiter_id})\n"
        f"Title: {recruiter['title']}\n"
        f"Agency: {recruiter['agency']}\n"
        f"Industry focus: {recruiter['industry']}\n"
        f"Specialties: {', '.join(recruiter['specialties'])}\n"
        f"Location: {recruiter['location']}\n"
        f"Placements (12 mo): {recruiter['placements_last_12_months']}\n"
        f"Response rate: {int(recruiter['response_rate'] * 100)}%\n"
        f"Avg time to first reply: {recruiter['avg_time_to_first_reply_hours']}h\n"
        f"Contact: {recruiter['contact']['email']} | {recruiter['contact']['linkedin']}\n"
        f"Notes: {recruiter['notes']}"
    )


@tool
def get_placements(recruiter_id: str) -> str:
    """Get a recruiter's recent placements (companies, roles, and levels).

    Args:
        recruiter_id: The recruiter ID (e.g. R-2001)
    """
    placements = PLACEMENTS.get(recruiter_id)
    if not placements:
        return f"No placement records found for recruiter {recruiter_id}"
    lines = [f"Recent placements for {recruiter_id}:"]
    for p in placements:
        lines.append(
            f"- {p['role']} at {p['company']} ({p['level']}) — {p['months_ago']} month(s) ago"
        )
    return "\n".join(lines)


@tool
def add_to_shortlist(recruiter_id: str, note: str) -> str:
    """Add a recruiter to the working shortlist with a short note on why they
    are a good match.

    Args:
        recruiter_id: The recruiter ID (e.g. R-2001)
        note: A short note explaining the fit (e.g. "Strong backend network")
    """
    if recruiter_id not in RECRUITERS:
        return f"No recruiter found with ID {recruiter_id}"
    SHORTLIST[recruiter_id] = note
    recruiter = RECRUITERS[recruiter_id]
    return f"Added {recruiter['name']} ({recruiter_id}) to the shortlist. Note: {note}"


@tool
def view_shortlist() -> str:
    """List the recruiters currently on the working shortlist."""
    if not SHORTLIST:
        return "The shortlist is empty."
    lines = ["Current shortlist:"]
    for rid, note in SHORTLIST.items():
        recruiter = RECRUITERS[rid]
        lines.append(
            f"- {recruiter['name']} ({rid}) — {recruiter['agency']} — Note: {note}"
        )
    return "\n".join(lines)
