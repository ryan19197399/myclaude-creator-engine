# First-Time Experience Protocol

> Loaded by BOOT when `creator.yaml` missing OR `sessions_total == 0`.

When the Engine detects a brand new user, the BOOT transforms into a guided arrival:

```
1. DETECT: no creator.yaml → this is a first-time user
2. WELCOME: Show the myClaude Studio frame with a warm, brief welcome
   ┌─ MyClaude Studio Engine ───────────────────────┐
   │                                                 │
   │  Welcome. This engine turns your expertise      │
   │  into tools anyone can install and use.         │
   │                                                 │
   │  Let's set up your profile — 60 seconds.       │
   │                                                 │
   └─────────────────────────────────────────────────┘
3. ENDOWED PROGRESS SCAN → Before asking anything, scan environment silently:
   - Detect: git config (name, email), existing .claude/ directory,
     workspace/ contents, OS, shell, installed tools
   - Show what the Engine already knows:
     "I already know a few things about you:"
     • Name: {detected_name} (from git config)
     • Environment: {os} with {tools_detected}
     • [If .claude/ exists]: "You have {N} existing skills ready to import"
   - Frame as progress: "Your profile is already ~30% complete.
     Two quick questions to finish."
   - THEN trigger micro-onboard (2 questions only: type + primary goal)
   - The scan IS the onboard start — the creator sees progress before effort.
4. AFTER ONBOARD → show personalized next step based on profile.type:
   - Developer: "You have {N} skills already. Run /import to bring one in, or /create skill to start fresh."
   - Domain expert: "Run /scout {your domain} to discover what to build."
   - Marketer: "Run /create minds to package your expertise as an advisor."
   - Unknown: "Run /help to see everything you can do."
5. GOAL: First-time user feels value in under 60 seconds. No walls of text. No jargon. Just: welcome → profile → your next move.
```

This replaces the generic dashboard for first-timers. After the first product is created, normal BOOT resumes.
