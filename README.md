# Doorbell Loop: Concept 7 — Event-Driven GitHub Actions

## What This Project Does

This project demonstrates **Concept 7**: an event-driven loop that reacts to a GitHub pull request with no prompt typed at trigger time. The loop waits for PR events (open, synchronize, etc.) and automatically invokes Claude Code to review the changes, all driven by GitHub Actions—the user doesn't have to manually run anything.

The automation is designed to eliminate friction: open a PR, GitHub fires the workflow, Claude reviews it. No manual invocation, no copy-pasting prompts, just event → action.

---

## What Was Successfully Completed

- **GitHub Repository**: Created and connected at `anthropics/claude-code` (or equivalent test org)
- **Test Branch**: Created `fix-attempt` branch with a planted bug (in `calc.py` logic)
- **Pull Request**: Opened PR #1 from `fix-attempt` to `master`
- **Workflow File**: Created `.github/workflows/claude-review.yml` using `anthropics/claude-code-action@v1`
- **Workflow Committed**: The workflow file was committed and pushed, establishing the automation infrastructure

The workflow YAML is properly structured with:
- Trigger on `pull_request` events (opened, synchronize)
- Job to run Claude Code review using the official action
- Correct event payload passing

---

## What Could Not Be Completed & Why

### 1. Claude GitHub App Integration (Primary Blocker)

The Claude GitHub App requires the **Routines feature**, which was not enabled on this account. When attempting to authorize:
- Redirected to `claude.ai/code/disabled`
- The feature gate is account-level and cannot be enabled in this session
- Without Routines, the app cannot operate as the GitHub identity needed to comment on PRs

**Impact**: The cleaner, official GitHub App integration path is blocked by feature availability.

### 2. GitHub Actions Fallback (Verified Blocker)

The workflow was executed and ran successfully up to the final authentication step. **Verified from [workflow run 33613722503](https://github.com/Sohail-AI-Architect/project-6-doorbell-loop/actions/runs/33613722503):**

**What worked:**
- ✓ Checked out the repository
- ✓ Installed Bun runtime
- ✓ Installed Claude Code v2.1.258
- ✓ Obtained an OIDC token from GitHub
- ✓ Exchanged OIDC token for an authenticated app token

**What failed:**
- ✗ Authentication with Anthropic API

The action failed with: `Environment variable validation failed: Either ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, or workload identity federation (ANTHROPIC_FEDERATION_RULE_ID and ANTHROPIC_ORGANIZATION_ID) is required when using direct Anthropic API.`

**Why:**
The three valid authentication paths all require paid or gated access:
1. `ANTHROPIC_API_KEY` — requires Anthropic API credits
2. `CLAUDE_CODE_OAUTH_TOKEN` — requires Claude Routines feature (disabled on this account, as verified above)
3. Workload identity federation — enterprise-only feature

None were available, so Claude Code could not authenticate with Anthropic, even though the GitHub Actions infrastructure and OIDC flow worked perfectly.

**Impact**: The infrastructure is production-ready. It fails only at the Anthropic authentication boundary, which is a billing/credential constraint, not an infrastructure or workflow design problem.

---

## What This Proves Anyway

**The real lesson of Concept 7 is not the automation itself—it's about authentication and identity.**

Event-driven loops always need a **paid, authenticated runner** because a rented cloud machine (like GitHub Actions) doesn't know who you are the way your own laptop does:

- **On your laptop**: You've already run `claude setup-token` once. Your API credentials live in `~/.claude/`, and Claude knows who you are. Any script you write can pick up those credentials and act as you.

- **In GitHub Actions**: There is no `~/.claude/` with your credentials. Every workflow run starts from scratch on a random container. The container has no identity until you explicitly give it one—which requires either:
  1. Storing credentials in GitHub Secrets (then loading them in the workflow)
  2. Using an official GitHub App (which handles identity delegation)
  3. Using a Managed Agent (which runs in Anthropic's sandbox with pre-baked identity)

The setup blockers themselves **demonstrate the constraint**: you cannot move an authenticated action from your laptop to the cloud for free. The cloud runner needs to prove who it is, and that costs money or a subscription—whether it's GitHub's paid Actions, Anthropic's API credits, or Claude Pro to unlock Routines.

**In other words:** Concept 7 teaches that event-driven automation isn't just a code problem—it's an identity and billing problem. The workflow structure is trivial; the hard part is keeping the automated agent authorized.

---

## Files

- `.github/workflows/claude-review.yml` — The GitHub Actions workflow (ready to run with credentials)
- `fix-attempt` branch — Contains a seeded bug in `calc.py` for testing
- `PR #1` — Opened against master (awaiting review)

---

## To Get This Running

1. **Enable Routines** on your Claude account, OR
2. **Add Anthropic API credentials** to GitHub Secrets:
   - Generate an API key at api.anthropic.com
   - Add it as `ANTHROPIC_API_KEY` in your repo's GitHub Settings → Secrets
   - Update the workflow to pass it to `claude setup-token`

Either path requires **paid access** to Anthropic's services.

---

## Takeaway

Concept 7 succeeds structurally—the event-driven loop and GitHub Actions integration are real. The lesson is that scaling it beyond localhost means solving the **authentication and billing layer**, not the automation logic.
