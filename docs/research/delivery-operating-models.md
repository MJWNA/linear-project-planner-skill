# Delivery Operating Models For Long-Horizon Software Projects

## Source Scope

This research pass focused on current, high-signal delivery operating model
sources that are directly relevant to agent-heavy, long-horizon software
projects:

- DORA's 2026-updated guide to software delivery metrics, especially the
  current five-metric model and its split between throughput and instability.
- ACM Queue's SPACE framework for developer productivity, especially its warning
  against one-metric productivity systems and its emphasis on flow,
  collaboration, satisfaction, and system-level measures.
- Atlassian's Team Topologies summary, especially stream-aligned teams,
  platform teams, enabling teams, full ownership, team health, and technical
  quality metrics.
- Continuous Delivery / Thoughtworks-origin material from Jez Humble and later
  Thoughtworks commentary, especially organizing around outcomes, lowering
  release transaction cost, value-stream mapping, small batches, and avoiding
  functional silos.
- DORA capability material on continuous delivery and platform engineering,
  because Expanded Mode will depend on delivery system quality, not just more
  agent activity.

## Confirmed Practices

### Balance Throughput With Instability

DORA now frames software delivery performance as a balance between throughput
and instability. Throughput is represented by change lead time, deployment
frequency, and failed deployment recovery time. Instability is represented by
change fail rate and deployment rework rate. The important operating model
lesson is that fast delivery is only healthy when the system also remains
recoverable and low rework.

For long-horizon projects, this argues against tracking only "issues closed" or
"agents active." Expanded Mode should expose whether extra parallelism shortens
lead time without increasing failure, rework, rollback, or recovery effort.

### Organize Around Outcome Ownership

Thoughtworks' continuous delivery material argues that delivery should be
organized around outcomes rather than roles, because functional silos increase
handoffs, communication overhead, batch size, and release risk. Cross-functional
teams reduce lead time when they can collaborate across development, testing,
operations, infrastructure, architecture, and product decisions before work is
late in the process.

Team Topologies reaches a similar conclusion through stream-aligned teams:
durable teams should own a product, service, feature stream, user journey, or
persona and should be able to build, run, and fix their work with minimal
handoffs. Support teams exist to reduce cognitive load and increase autonomy,
not to create permanent dependency queues.

### Treat Platform Work As A Product

Atlassian and DORA both describe platform teams as enablers of autonomy for
stream-aligned teams. DORA's platform engineering capability is especially
explicit: internal platforms should be treated as developer-facing products with
golden paths, self-service, clear feedback, and a product-management mindset.

The platform is not a ticket desk. Its job is to remove recurring friction from
delivery streams and to standardize secure, reliable, compliant paths for
building, testing, deploying, and operating software. DORA also warns that poor
platform quality can absorb individual productivity gains into downstream
disorder, especially when AI or agentic coding increases the rate of code
production.

### Use Enabling Teams Temporarily

Team Topologies positions enabling teams as specialists who help stream-aligned
teams learn, experiment, and gain capability. The healthy pattern is temporary
facilitation: support should leave the receiving team more autonomous after a
short period, not dependent on a permanent expert bottleneck.

For long-running programs, this matters because architecture, testing,
observability, AI-agent operations, and release engineering expertise can either
become reusable capability or become a hidden serial queue. The operating model
should make the difference visible.

### Measure Flow, Quality, And Human Sustainability

SPACE is the strongest warning against one-dimensional productivity management.
It recommends a small set of metrics across multiple dimensions: satisfaction
and well-being, performance, activity, communication and collaboration, and
efficiency and flow. It also says activity metrics like commits, pull requests,
reviews, or tickets are useful only as limited signals and should not be used in
isolation to reward, penalize, or compare productivity.

DORA's continuous delivery capability also reinforces flow measurement through
value-stream mapping. Teams should inspect elapsed time, value-add time,
handoffs, queues, rework, and percentage complete-and-accurate across the path
from change to production. Thoughtworks makes the same practical point: pick a
recently finished feature and map its path from idea to production to find the
real bottleneck.

## Implications For Expanded Mode

### Throughput vs Instability

Expanded Mode should treat parallel agent count as an input, not a success
metric. The success metrics should be whether the mode improves flow without
increasing instability.

Required implications:

- Track throughput signals: issue lead time, time in blocked/review states,
  cycle time from claim to verified completion, deployment or release cadence
  when applicable, and queue age for active work.
- Track instability signals: failed verification rate, reopened issues, rework
  caused by conflicting agents, merge conflicts, broken tests, rollback/fixup
  commits, production incidents, and time to recover from a bad agent change.
- Present these as paired signals. A week with more completed issues but more
  rework or failed verification is not automatically a better week.

### Cross-Functional Ownership

Expanded Mode should organize work around durable outcome streams, not role
lanes. A "research agent," "implementation agent," "test agent," and "release
agent" can be useful temporarily, but the operating model should keep ownership
anchored to a product/service/workstream outcome.

Required implications:

- Every workstream needs an owner who can make tradeoff decisions and reconcile
  research, implementation, verification, and release evidence.
- Issues should make the business or system outcome explicit, not only the
  activity to perform.
- Handoffs between agents should be minimized and documented only when they
  compress useful context.
- Agent output should be integrated into the same verification path rather than
  split into separate "done by role" queues.

### Platform And Enabling Teams

Expanded Mode needs a platform layer and an enabling layer, but they should have
different jobs.

Required implications:

- Platform responsibilities: reusable templates, branch/worktree conventions,
  safe Linear transition wrappers, ledger conventions, verification commands,
  release checklists, test harnesses, and self-service "golden paths" for common
  project shapes.
- Enabling responsibilities: short-lived help for unfamiliar domains, unclear
  source material, new verification patterns, architecture spikes, and agent
  workflow coaching.
- Platform success should be measured by reduced cognitive load and fewer
  repeated questions, not by how many support tickets the platform team closes.
- Enabling success should be measured by whether stream agents can work more
  independently afterward.

### QA And Flow Metrics

Expanded Mode should bring QA closer to the work instead of treating QA as a
late gate. The research sources converge on smaller batches, earlier feedback,
and system-level flow measurement.

Required implications:

- Define verification gates at issue creation, not after implementation.
- Track first-pass verification success, rework loops, escaped defects, review
  latency, blocked time, handoff count, and percentage complete-and-accurate for
  agent deliverables.
- Include qualitative checks for documentation discoverability, handoff quality,
  and whether future agents can resume without re-discovery.
- Use value-stream reviews for completed issues to identify where work waited,
  bounced, or lost context.

### Avoid One-Metric Productivity Traps

Expanded Mode should not optimize for number of agents, number of commits,
number of issues closed, story points, token volume, or raw activity. SPACE and
DORA both warn that single metrics distort behavior and can hide burnout,
quality decline, rework, or collaboration costs.

Required implications:

- Use a balanced scorecard with at least one throughput signal, one instability
  signal, one flow/friction signal, and one human/operator sustainability signal.
- Report activity metrics as diagnostic context, not as the headline.
- Avoid comparing unrelated workstreams by a single number.
- Prefer trend-over-time improvement inside a comparable service or workstream.
- Make invisible work visible: review, mentoring, reconciliation, environment
  repair, documentation cleanup, and context compression all matter when they
  improve flow.

## What To Require vs Offer

### Require

- One named outcome owner per workstream or guide issue.
- A clear definition of done that includes verification evidence.
- Explicit dependency and blocker tracking for serial/risky work.
- Paired throughput and instability reporting for the project.
- A small balanced measurement set instead of one productivity score.
- Early QA criteria and a documented verification path.
- A platform/golden-path inventory for repeated agent workflows.
- A rule that support teams should reduce future dependency, not become the
  standing path for every change.
- Retrospective flow review for long-running or high-risk workstreams.

### Offer

- Optional SPACE-style health checks for larger projects where sustainability is
  a risk.
- Optional value-stream mapping templates for recently completed issues.
- Optional platform maturity checks: self-service, clear feedback, golden paths,
  extensibility, and bottleneck risk.
- Optional enabling-team playbooks for architecture, testing, observability, AI
  coding review, release management, and domain research.
- Optional dashboards that separate activity, flow, quality, and outcome
  metrics.
- Optional "minimum viable platform" guidance for teams that need just enough
  tooling to make the next repeated workflow better.

## Risks/Anti-Patterns

- Measuring agent productivity with one number, such as issues closed, commits,
  pull requests, story points, or active agents.
- Increasing deployment or merge frequency without improving tests,
  architecture, review quality, or recovery paths.
- Treating platform teams as ticket queues rather than internal product teams.
- Creating permanent enabling-team dependencies instead of growing capability in
  stream-aligned teams.
- Splitting delivery by role so research, implementation, QA, release, and ops
  become disconnected handoff lanes.
- Letting parallel agents produce large batches that are only reconciled at the
  end.
- Ignoring rework, failed verification, merge conflict rate, rollback effort, or
  issue reopen rate when celebrating throughput.
- Comparing unrelated services, teams, or project types with the same metric
  target.
- Overbuilding platform infrastructure before proving the most common workflow
  is better.
- Optimizing individual flow so aggressively that collaboration, review, and
  shared ownership suffer.

## Source Links

- [DORA: Software delivery performance metrics](https://dora.dev/guides/dora-metrics/) -
  five-metric model, throughput vs instability, common pitfalls, small batches,
  and cross-functional improvement conversations. Last updated January 5, 2026.
- [ACM Queue: The SPACE of Developer Productivity](https://queue.acm.org/detail.cfm?id=3454124) -
  multidimensional productivity framework, balanced metrics, flow,
  collaboration, well-being, and warnings against activity-only measurement.
- [Atlassian: Team Topologies](https://www.atlassian.com/devops/frameworks/team-topologies) -
  stream-aligned, platform, complicated-subsystem, and enabling teams; autonomy,
  minimal handoffs, team health, and quality metrics.
- [Continuous Delivery: Organize software delivery around outcomes, not roles](https://continuousdelivery.com/2011/12/organize-software-delivery-around-outcomes-not-roles/) -
  cross-functional teams, outcome-oriented organization, small batches,
  throughput, and reducing communication overhead.
- [Thoughtworks: Organize software delivery around outcomes](https://www.thoughtworks.com/insights/blog/organize-software-delivery-around-outcomes) -
  Thoughtworks republication of the same Jez Humble argument with emphasis on
  continuous delivery, silos, strategic products, and business outcomes.
- [Thoughtworks: Continuous delivery is not just a technical activity](https://www.thoughtworks.com/en-us/insights/blog/continuous-delivery/continuous-delivery-not-just-a-technical-activity) -
  organizational alignment, value streams, small stories, batch size, and
  bottleneck discovery.
- [DORA: Continuous delivery capability](https://dora.dev/capabilities/continuous-delivery/) -
  process and architecture change, value-stream mapping, rework, low-risk
  releases, and continuous daily improvement.
- [DORA: Platform engineering capability](https://dora.dev/capabilities/platform-engineering/) -
  internal platforms as developer products, golden paths, cognitive load,
  self-service, minimum viable platforms, and balanced impact measurement.
