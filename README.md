# Feed Detox

A "done **with** you" tool for the ad-cleanup service. It runs the customer
through a short numbered intake, then writes them a **personalized playbook**
plus a **Precepts card** — the ongoing rules that keep the feed from
recontaminating.

It never touches anyone's account or password. The ~15 minutes of clicking is
done by the customer on their own screen, following the plan. That's the whole
point: your bot does the thinking (intake + custom plan), the customer keeps
control of their account.

## Run it

Double-click **Feed Detox.command**, or:

```
python3 feeddetox.py
```

## What it produces

For each customer, in `data/`:

- `<name>_playbook.md` — ordered, personalized cleanup steps
- `<name>_precepts.md` — the keep-it-clean card

Both are Markdown — run them through your PDF Tool for a clean handout.

## The two halves

1. **The cleanup** (one time): off-Meta activity, interest categories,
   sensitive ad topics, hiding advertisers, planting good signal.
2. **The Precepts** (ongoing): the daily habits — don't click, don't linger,
   don't engage, guard the back door, renew monthly — because the feed
   rebuilds itself from behavior. Skip these and it all comes back.


## Licence

Records, prose and pages: CC BY-SA 4.0. Code: AGPL-3.0-or-later. Anything
carried in from elsewhere keeps its own terms — see [LICENSE](LICENSE).

**Commercial licence.** If share-alike doesn't fit your use — a corpus, a
product, a model — a commercial licence is available.
[Open an issue](https://github.com/NaNoBotCo/feed-detox/issues) and say what you need.

---

Contact: Nan · nan@motdang.net · Sponsor: [Ko-fi](https://ko-fi.com/defiantchiangmai) · [Patreon](https://www.patreon.com/nanobotco)
