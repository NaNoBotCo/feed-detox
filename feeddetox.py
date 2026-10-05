#!/usr/bin/env python3
"""
Feed Detox — intake + custom playbook generator + the Precepts.

A "done WITH you" tool: it asks a few numbered questions, then writes a
personalized Facebook ad-hygiene playbook and a Precepts card the customer
keeps.  It never touches anyone's account or password — the ~5 minutes of
clicking is done by the customer on their own screen, following the plan.

Stdlib only.  Numbered menus, minimal typing.
"""

import os
import textwrap
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
WIDTH = 72


# --------------------------------------------------------------------------
# Content the intake picks from
# --------------------------------------------------------------------------

# Topics people commonly want turned DOWN. Facebook's built-in "Ad topics"
# control covers some of these directly; the rest are handled by removing
# interest categories and hiding advertisers.
SEE_LESS_TOPICS = [
    "Alcohol",
    "Gambling / betting",
    "Politics & social issues",
    "Body image / weight loss / dieting",
    "Cosmetic procedures & 'wellness'",
    "Parenting & baby products",
    "Pregnancy & fertility",
    "Pets",
    "Dating / relationships",
    "Religion & spirituality",
    "Cryptocurrency & trading",
    "Real estate & mortgages",
    "Gaming & in-app purchases",
    "Fast fashion / drop-shipping",
    "Get-rich / business opportunity",
]

# What the customer DOES want — this is what makes it "for you".
KEEP_INTERESTS = [
    "Books & reading",
    "Cooking & food",
    "Travel",
    "Music & instruments",
    "Art & design",
    "Gardening & plants",
    "Outdoors / hiking / camping",
    "Tech & gadgets",
    "Home & tools / DIY",
    "Fitness & sport",
    "Photography",
    "Local events & community",
    "Crafts & making",
    "Cars / bikes",
]

OFFACT_MODES = [
    ("Aggressive", "Clear all history AND disconnect future off-Meta activity. "
                   "Strongest cut; some sites may ask you to log in again."),
    ("Moderate",   "Clear history now, but leave future activity connected. "
                   "Good balance; re-clear monthly (see the Precepts)."),
    ("Light",      "Just review it, clear nothing. Not recommended — this is "
                   "the biggest source of 'creepy' ads."),
]

# The Precepts — how NOT to recontaminate the feed. (rule, why)
PRECEPTS = [
    ("Do not click ads out of curiosity.",  # stylecheck: allow — the playbook the customer asked for
     "A click is the single strongest 'I want this' signal you can send."),
    ("Do not linger on an ad you don't want.",  # stylecheck: allow — the playbook the customer asked for
     "Time-on-screen (dwell) is measured. Scroll past deliberately."),
    ("Do not react, comment, or argue on sponsored posts.",  # stylecheck: allow — the playbook the customer asked for
     "Any engagement — even angry — reads as 'show me more of this'."),
    ("Do not follow or like brand pages you don't want to hear from.",  # stylecheck: allow — the playbook the customer asked for
     "A follow is a standing invitation the algorithm honors for months."),
    ("Mind your searches.",  # stylecheck: allow — the playbook the customer asked for
     "Product searches inside Meta feed the ad engine. Search elsewhere."),
    ("Guard the back door.",
     "New browser, new phone, or accepting cookie tracking lets off-site "
     "pixels refill your profile. Re-clear off-Meta activity monthly."),
    ("Feed good seed.",
     "Engage with what you DO love. The feed grows toward your "
     "genuine attention — so aim it on purpose."),
    ("Renew the practice.",
     "Once a month, re-clear off-Meta activity and hide any new junk "
     "advertisers. Ten minutes keeps the whole thing clean."),
]


# --------------------------------------------------------------------------
# Small input helpers (numbered, low-typing)
# --------------------------------------------------------------------------

def rule(ch="-"):
    print(ch * WIDTH)


def wrap(text, indent=""):
    for para in text.split("\n"):
        if not para.strip():
            print()
            continue
        print(textwrap.fill(para, WIDTH, initial_indent=indent,
                            subsequent_indent=indent))


def pause():
    input("\n[ press Enter to continue ]")


def multiselect(title, options, help_line=""):
    """Show a numbered list; user types numbers (space/comma), 'a'=all,
    Enter=none. Returns the chosen option strings, in listed order."""
    print()
    rule("=")
    print(title)
    rule("=")
    if help_line:
        wrap(help_line)
        print()
    for i, opt in enumerate(options, 1):
        print(f"  {i:2}. {opt}")
    print()
    print("  Type the numbers you want (e.g. 1 3 4).  'a' = all.  Enter = none.")
    raw = input("  > ").strip().lower()
    if raw == "a":
        return list(options)
    if not raw:
        return []
    picks = []
    for tok in raw.replace(",", " ").split():
        if tok.isdigit():
            n = int(tok)
            if 1 <= n <= len(options):
                picks.append(options[n - 1])
    # de-dup, keep listed order
    return [o for o in options if o in picks]


def singleselect(title, labeled_options):
    """labeled_options: list of (label, description). Returns index chosen."""
    print()
    rule("=")
    print(title)
    rule("=")
    for i, (label, desc) in enumerate(labeled_options, 1):
        print(f"  {i}. {label}")
        wrap(desc, indent="     ")
        print()
    while True:
        raw = input("  > ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(labeled_options):
            return int(raw) - 1
        print("  Please type one number from the list.")


# --------------------------------------------------------------------------
# Intake
# --------------------------------------------------------------------------

def run_intake():
    os.system("clear")
    rule("=")
    print("  FEED DETOX  —  intake")
    rule("=")
    wrap("A few quick questions. Numbers only — almost no typing.")
    print()

    name = input("  Customer name or nickname (Enter to skip): ").strip() or "Friend"

    keep = multiselect(
        "1)  What do you actually WANT to see ads about?",
        KEEP_INTERESTS,
        "This is the point of the whole thing — the feed grows toward "
        "what you feed it, so name the good stuff.")

    less = multiselect(
        "2)  What do you want to see LESS of?",
        SEE_LESS_TOPICS,
        "Pick the topics that make you want to close the app.")

    off_idx = singleselect(
        "3)  How hard do you want to cut off the data supply?",
        OFFACT_MODES)

    return {
        "name": name,
        "keep": keep,
        "less": less,
        "off_mode": OFFACT_MODES[off_idx][0],
        "off_desc": OFFACT_MODES[off_idx][1],
    }


# --------------------------------------------------------------------------
# Playbook generation
# --------------------------------------------------------------------------

def build_playbook(a):
    L = []
    W = L.append

    W(f"# Feed Detox playbook — {a['name']}")
    W(f"_Generated {date.today().isoformat()}_")
    W("")
    W("Do these once, in order. About 15 minutes. You stay logged in the "
      "whole time — nobody but you touches your account.")
    W("")
    W("**Where the controls live**")
    W("- Phone: tap the **menu (≡)** → **Settings & privacy** → "
      "**Settings** → scroll to **Ads** / **Ad preferences**.")
    W("- Computer: top-right menu → **Settings & privacy** → "
      "**Settings** → **Ads** in the left sidebar.")
    W("")
    W("(Meta moves these around. If a name doesn't match, search the "
      "Settings page for the word in **bold**.)")
    W("")

    step = 1

    # Step: off-Meta activity
    W(f"## Step {step}. Cut off the outside data supply")
    step += 1
    W(f"Chosen level: **{a['off_mode']}** — {a['off_desc']}")
    W("")
    W("Go to **Off-Meta activity** (older name: *Off-Facebook activity*).")
    if a["off_mode"] == "Aggressive":
        W("1. Open **Manage future activity** → turn it **off** "
          "(disconnect future activity).")
        W("2. Then **Clear history** / **Disconnect** to wipe what's "
          "already stored.")
    elif a["off_mode"] == "Moderate":
        W("1. Tap **Clear history** / **Disconnect** to wipe what's stored.")
        W("2. Leave future activity connected — but re-clear monthly "
          "(Precept 6 & 8).")
    else:
        W("1. Open it and read the list of companies that sent your "
          "activity to Meta. When you're ready, come back and clear it.")
    W("")

    # Step: interest categories
    W(f"## Step {step}. Prune the interest categories")
    step += 1
    W("Open **Ad preferences → Categories used to reach you** "
      "(a.k.a. *Interest categories*). This is the profile Meta built "
      "about you. Remove anything that doesn't match what you want.")
    if a["less"]:
        W("")
        W("Hunt down and **remove** anything related to your see-less list:")
        for t in a["less"]:
            W(f"- {t}")
    if a["keep"]:
        W("")
        W("**Keep** (or don't worry about) categories matching what you "
          "*do* want:")
        for t in a["keep"]:
            W(f"- {t}")
    W("")

    # Step: ad topics (sensitive)
    W(f"## Step {step}. Turn down sensitive ad topics")
    step += 1
    W("Open **Ad topics**. Facebook lets you say **See less** on a set of "
      "sensitive topics directly. Set **See less** on any that apply:")
    covered = [t for t in a["less"] if any(
        k in t for k in ("Alcohol", "Gambling", "Politics", "Body",
                         "Parenting", "Pregnancy", "Pets", "Cosmetic"))]
    if covered:
        for t in covered:
            W(f"- {t} → **See less**")
    else:
        W("- (None of your picks are in Meta's built-in list — they're "
          "handled by Steps 2 and 4 instead.)")
    W("")

    # Step: advertisers
    W(f"## Step {step}. Hide the junk advertisers")
    step += 1
    W("Open **Advertisers → Advertisers you've seen recently** (and "
      "**...whose ads you clicked**). For every one you don't want:")
    W("- Tap it → **Don't show ads from this advertiser** / **Hide**.")
    W("Be ruthless. This list is where most of the daily clutter comes from.")
    W("")

    # Step: plant good seed
    W(f"## Step {step}. Plant good seed")
    step += 1
    W("The feed needs positive signal, not just deletions. Give it "
      "signal toward what you like:")
    if a["keep"]:
        for t in a["keep"]:
            W(f"- Follow 1–2 genuinely good pages about **{t}**.")
    else:
        W("- Follow a few pages about things you truly enjoy.")
    W("- When a *good* ad appears, it's fine to let it be. You're teaching "
      "the algorithm what 'right' looks like.")
    W("")

    # Step: the everyday tool
    W(f"## Step {step}. Learn the everyday tool")
    step += 1
    W("From now on, on ANY ad you don't want:")
    W("- Tap the **···** (three dots) on the ad → "
      "**Why am I seeing this ad?** → **Hide ad** or "
      "**Hide all ads from this advertiser**.")
    W("This is the 3-second move that keeps the feed clean forever.")
    W("")

    # Precepts
    W("---")
    W("## The Precepts — how not to recontaminate your feed")
    W("")
    W("The cleanup above is one-time. Staying clean is a practice. The "
      "feed rebuilds itself from what you do every day — so live by these:")
    W("")
    for i, (rule_txt, why) in enumerate(PRECEPTS, 1):
        W(f"{i}. **{rule_txt}**")
        W(f"   _Why:_ {why}")
        W("")

    return "\n".join(L)


def build_precepts_card(name="Friend"):
    L = [f"# The Precepts — {name}", "",
         "Keep this where you'll see it. The feed recontaminates itself "
         "from daily habits; these keep it clean.", ""]
    for i, (rule_txt, why) in enumerate(PRECEPTS, 1):
        L.append(f"{i}. {rule_txt}")
        L.append(f"     — {why}")
        L.append("")
    return "\n".join(L)


def save(name, suffix, text):
    safe = "".join(c if c.isalnum() else "_" for c in name).strip("_") or "customer"
    path = os.path.join(DATA, f"{safe}_{suffix}.md")
    with open(path, "w") as f:
        f.write(text)
    return path


# --------------------------------------------------------------------------
# Flows
# --------------------------------------------------------------------------

def flow_new():
    a = run_intake()
    playbook = build_playbook(a)
    card = build_precepts_card(a["name"])

    p_path = save(a["name"], "playbook", playbook)
    c_path = save(a["name"], "precepts", card)

    os.system("clear")
    rule("=")
    print(f"  PLAYBOOK for {a['name']}")
    rule("=")
    print()
    print(playbook)
    print()
    rule("=")
    print("  Saved:")
    print(f"   • {p_path}")
    print(f"   • {c_path}")
    rule("=")
    print("  (Both are Markdown — run them through your PDF Tool for a")
    print("   clean handout to give the customer.)")
    pause()


def flow_precepts():
    os.system("clear")
    print(build_precepts_card())
    pause()


def main():
    while True:
        os.system("clear")
        rule("=")
        print("  FEED DETOX")
        rule("=")
        print()
        print("  1.  New customer — intake + custom playbook")
        print("  2.  View the Precepts")
        print("  3.  Quit")
        print()
        choice = input("  > ").strip()
        if choice == "1":
            flow_new()
        elif choice == "2":
            flow_precepts()
        elif choice in ("3", "q", ""):
            print("\n  Be well.\n")
            return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Be well.\n")
