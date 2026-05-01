# Quality Control Framework

## The Rule
Nothing publishes unless it passes all three gates. No exceptions. No "this is good enough." If it doesn't clear the bar, it gets rewritten from scratch. We'd rather publish nothing than publish filler.

---

## Gate 1: Quality Rubric (CMO Agent)

Every piece of content must score YES on all 5 criteria. One NO = rewrite, not edit.

| # | Criteria | Test |
|---|----------|------|
| 1 | **Teaches something real** | Would a developer or founder learn something they didn't know 60 seconds ago? If you strip the NeoCrew branding, is this still worth reading? |
| 2 | **CTO-shareable** | Would a senior engineer share this with their team without looking dumb? Is the technical framing accurate and substantive? |
| 3 | **Drives conversation** | Does this invite a response, start a debate, or make someone want to DM? Is there a genuine question or tension in it? |
| 4 | **Specific, not generic** | Is there a concrete insight, number, pattern, or example? Or is it just a vague observation anyone could make? |
| 5 | **Protects IP** | Does it talk about philosophy and outcomes (4 pillars, deterministic pipeline, quality gates) WITHOUT exposing proprietary details (exact agent count, specific validator-patcher patterns, internal architecture specifics)? |

### Architecture Disclosure Rules
SAFE to discuss publicly:
- The 4-pillar structure (Discover, Design, Blueprint, Build)
- Deterministic pipeline philosophy
- Quality gates and self-healing correction concept
- Human-in-the-loop at stage boundaries
- Parallel execution as a pattern
- The problem of probabilistic drift

KEEP PRIVATE (sales conversations and deep-dives only):
- Exact number of agents (51)
- Specific agent types and their individual roles
- The 14 agent types in Blueprint, 23 in Build
- Detailed validator-patcher-assembler patterns
- E2B sandbox specifics
- Specific review layer architecture

### Red Flags That Kill a Post
- Reads like every other AI company's LinkedIn post
- Uses phrases like "game-changing", "revolutionary", "the future of"
- Makes a claim without backing it with experience or data
- Could be written by someone who's never shipped software
- Contains emdashes
- Names specific competitor tools
- Mentions pricing
- Generic CTA like "follow for more"

---

## Gate 2: Human Review (Slack)

Every approved piece from Gate 1 goes to #content-review in Slack.

Format:
```
CHANNEL: [LinkedIn / Twitter / Blog]
PILLAR: [which content pillar]
RUBRIC: [5/5 - all criteria passed]
CONTENT:
[full post text]
```

Shri or Jhilik responds:
- Thumbs up = publish
- Feedback = CMO agent revises and resubmits
- Kill = post is scrapped, reason logged for learning

Target: review should take under 30 seconds per post. If it takes longer, the content isn't clear enough.

---

## Gate 3: Weekly Retro (Every Friday)

CMO agent generates a weekly content performance report:

### What to Analyze
1. **Which posts hit all 3 bars?** (taught, shared, drove conversation)
2. **Which posts fell flat?** (low engagement, no comments, no shares)
3. **What patterns emerge?** (certain pillars performing better, certain formats winning)
4. **Comment quality check** - are the right people engaging? (developers, founders, CTOs vs. random likes)
5. **Inbound attribution** - did any content directly lead to a DM, email, or call?

### Output Format
```
WEEK OF: [date]

TOP PERFORMER:
[post link + why it worked]

WORST PERFORMER:
[post link + why it failed]

PATTERN:
[what to do more of / less of next week]

INBOUND LEADS FROM CONTENT: [count + details]

RECOMMENDATION FOR NEXT WEEK:
[specific topic/pillar/format adjustment]
```

### Feedback Loop
- Top performer patterns feed into next week's content strategy
- Failed patterns get flagged so writer agents avoid them
- If a pillar consistently underperforms, reduce its frequency
- If a format consistently wins, increase it

---

## Measurement Framework

### Metrics That Matter (Track Weekly)

**LinkedIn Company Page:**
- Saves and shares (not just likes - these show real value)
- Comment quality (substance vs. "great post")
- Company page visits from posts
- Inbound DMs attributed to content
- Follower growth rate (and follower quality - are they ICP?)

**Twitter/X:**
- Quote tweets and bookmarks (strongest signals of value)
- Reply quality from builders and engineering leads
- Follower quality (ICP vs. bots)
- Thread completion rate (how far do people read?)

**Blog:**
- Organic search impressions and clicks per target keyword
- Time on page and scroll depth (are they actually reading?)
- Blog-to-site conversion (do readers visit neocrew.ai?)
- Keyword ranking movement week over week

### The One Metric That Proves It's Working
**Inbound conversations attributed to content.**

Someone DMs, emails, or books a call and references a post, blog, or thread. Track every single one. This is the only metric that directly connects content to revenue.

### Monthly Review
At the end of each month:
1. Total inbound conversations from content
2. Best-performing content type and pillar
3. Keyword ranking progress
4. Cost per piece of content (API spend / pieces published)
5. Decision: what to scale up, what to cut
