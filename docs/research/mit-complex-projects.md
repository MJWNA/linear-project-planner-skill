# MIT Complex Technical Projects Research

Retrieved: 2026-04-29 AEST

Linear issue: MAS-691

## Source Scope

This note prioritizes current MIT-owned sources and uses MIT-adjacent sources
only where they clarify MIT program content. Primary sources reviewed:

- MIT Sloan Executive Education, `Managing Complex Technical Projects`.
- MIT Sloan Executive Education, `The Design Structure Matrix`.
- MIT Industrial Liaison Program, `Design Structure Matrix`.
- MIT Sloan Ideas Made to Matter, `10 agile ideas worth sharing`.
- MIT xPRO, `Software Architecture: Designing Scalable and Modular Systems`.
- MIT System Architecture Group, `System Architecture Methods`.
- MIT News, `Organizing "spaghetti" software so it can be easily modified`.

## Confirmed Practices

- Complex technical project management is treated as more than a schedule. MIT
  frames complex systems as many interdependent components, often built by
  different groups across organizations, where cost and schedule overruns are
  common.
- DSM is the central method for making hidden structure visible. MIT describes
  DSM as a compact matrix representation of elements and their dependencies,
  useful for understanding products, organizations, and processes.
- Dependency mapping is an explicit planning practice. Process DSM maps
  activities and deliverables, surfaces information flow, shows feedback loops,
  and supports more realistic sequencing than a one-way task list.
- DSM/modularity analysis applies to architecture and organization, not only
  project schedules. MIT's course takeaways include system decomposition,
  architecture modeling, modularity/integration patterns, and restructuring
  organizations based on system architecture.
- Planned and unplanned iteration are separate management concerns. MIT's
  course explicitly teaches participants to facilitate planned iterations and
  reduce unplanned iterations.
- Agile is positioned as useful but contextual. MIT Sloan's agile guidance
  favors spiral cycles, time-boxed sprints, visual work tracking, branch/merge,
  feature prioritization, DevOps alignment, and hybridized agile plus staged
  planning for large systems.
- Software architecture education centers on modularity, hidden dependencies,
  technical debt, maintainability, scalability, system evolution, code quality,
  and team productivity.
- MIT system architecture work frames architecture as coupled decisions across
  technologies, subsystems, and use contexts. Architectures are iteratively
  defined by a sequence of choices, not chosen in one step.

## Implications For Expanded Mode

- Dependency mapping should become an explicit expanded-mode artifact, not just
  a Linear relationship pass. Expanded mode should capture task, component,
  team, verification, data, and external-system dependencies in a compact graph
  or matrix before issue creation hardens sequencing.
- DSM/modularity should inform issue grouping. Parent workstreams should map to
  modules, bounded contexts, service boundaries, or architecture decisions where
  possible, while high-coupling areas should be marked as integration zones
  rather than treated as parallel-safe by default.
- Planned vs unplanned iteration should become a first-class planning axis.
  Expanded mode should identify planned learning loops, spike/prototype loops,
  integration loops, and expected review loops, then separately call out
  unplanned iteration risks caused by unknown dependencies, unclear interfaces,
  missing test or observability coverage, and stakeholder ambiguity.
- Architecture-to-organization mapping should be required for agent-heavy work.
  The plan should show which agents, owners, teams, or reviewers align to which
  architectural areas, and where communication links are needed because the
  organization cuts across the architecture.
- Expanded mode should support hybrid staged/agile execution. Use stage gates
  for discovery, architecture, implementation, integration, verification, and
  release readiness, but allow time-boxed sprint-like issue batches inside each
  stage.
- Software architecture research implies an architecture-health preflight:
  identify hidden dependencies, architectural debt, module boundaries, change
  hotspots, and the productivity impact of poor code structure before creating
  broad parallel implementation tickets.
- System architecture research implies a decision-log layer. Expanded mode
  should track high-leverage architecture decisions, coupled decision options,
  unresolved tradeoffs, and the order in which decisions must be made.

## What To Require vs Offer

Require in expanded mode:

- Dependency map covering tasks, code modules, data/sinks, environments,
  verification, owners/agents, and external services.
- DSM-style modularity review that classifies work as modular, integrative,
  cyclic, high-coupling, or unknown-coupling.
- Planned-iteration plan and unplanned-iteration risk register.
- Architecture-to-organization map for agents, reviewers, domain owners, and
  integration responsibilities.
- Explicit stage gates for discovery, architecture, implementation,
  integration, verification, and release/finalization.
- A decision log for high-leverage architecture or sequencing decisions.

Offer as optional depth:

- Full DSM matrix tables when the project is large enough to justify them.
- Clustering suggestions for modules, issue parents, or agent work packages.
- Architecture debt scoring or hotspot ranking.
- Tradespace comparison for multiple architecture or implementation options.
- Time-boxed sprint batches inside stage gates.
- Visual dependency diagrams in docs or Linear comments.

## Risks/Anti-Patterns

- Treating DSM as decoration. A matrix or graph is only useful if it changes
  sequencing, ownership, verification, or parallelism decisions.
- Over-requiring heavy artifacts for normal mode. Expanded mode can require
  deeper structure, but the default skill path should stay concise.
- Labeling coupled work as parallel-safe because the Linear issues look
  separate. MIT's DSM framing suggests hidden interfaces and feedback loops are
  the risk, not only obvious file overlap.
- Confusing planned iteration with rework. Expanded mode should intentionally
  budget learning cycles while reducing avoidable surprise loops.
- Copying agile ceremonies without architecture analysis. Time boxes and boards
  do not solve hidden dependency, modularity, or integration problems alone.
- Mirroring current org structure blindly. MIT's DSM organization framing
  implies organization design should be tested against system architecture, not
  assumed to be correct.
- Deferring architecture-to-organization mapping until implementation. In
  agent-heavy projects, this increases handoff loss, duplicated research, and
  integration conflict.

## Source Links

- MIT Sloan Executive Education, Managing Complex Technical Projects:
  https://executive.mit.edu/course/Managing-Complex-Technical-Projects/a056g00000URaMzAAL.html
- MIT Sloan Executive Education, The Design Structure Matrix:
  https://executive.mit.edu/the-design-structure-matrix.html
- MIT Industrial Liaison Program, Design Structure Matrix:
  https://ilp.mit.edu/node/36771
- MIT Sloan Ideas Made to Matter, 10 agile ideas worth sharing:
  https://mitsloan.mit.edu/ideas-made-to-matter/10-agile-ideas-worth-sharing
- MIT xPRO, Software Architecture: Designing Scalable and Modular Systems:
  https://learn-xpro.mit.edu/software-architecture
- MIT System Architecture Group, System Architecture Methods:
  https://systemarchitect.mit.edu/system-architecture-methods/
- MIT News, Organizing "spaghetti" software so it can be easily modified:
  https://news.mit.edu/2023/silverthread-organizing-spaghetti-software-1012
