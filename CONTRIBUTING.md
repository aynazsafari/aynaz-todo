# Contributing (University Workflow)

## Branching model (GitHub Flow)
- main: stable branch
- feature/<name>: new feature
- fix/<name>: bugfix
- chore/<name>: tooling/docker/refactor
- docs/<name>: documentation

## Commits
Use Conventional Commits:
- feat:, fix:, test:, chore:, docs:

Examples:
- feat: implement change status endpoint
- chore: add docker compose for postgres
- docs: add running guide

## Pull Requests (Mandatory)
All merges to main MUST happen through a PR.
PR should include:
- clear title
- short description
- test instructions
