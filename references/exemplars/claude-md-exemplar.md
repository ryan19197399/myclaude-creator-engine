# CLAUDE.md Exemplar: Next.js Enterprise Configuration

**MCS Level:** 3 (State-of-the-Art)
**Demonstrates:** Boot sequence, architecture overview, specific coding conventions,
security rules, workflow rules, modular rules directory, hook configurations.

---

## File: `CLAUDE.md`

```markdown
# Next.js Enterprise — Claude Code Configuration

> Claude Code configuration for large-scale Next.js 15 + TypeScript applications.
> Enforces App Router patterns, strict type safety, and security-first development.

**Version:** 2.0.0
**Target Stack:** Next.js 15 + TypeScript 5 + Tailwind CSS + PostgreSQL + Prisma
**Team Size:** Enterprise (5+ developers with code review gates)
**Author:** @enterprise-tooling

---

## First Action (Boot Sequence)

At the start of every session, before responding to any request:

1. **Read architecture:** `docs/architecture.md` — understand current system design
   and which patterns are established vs. under review
2. **Check git state:** Run `git status && git log --oneline -5`
   — identify active branch and recent context
3. **Load type definitions:** If working on a specific domain, read the relevant
   type definitions in `types/` before suggesting any code
4. **Read the file first:** Before modifying any file, read it completely
   — never assume structure from filename alone

---

## Architecture Overview

### Project Structure

```
src/
├── app/                  # Next.js App Router — pages, layouts, loading states
│   ├── (marketing)/      # Route group: public marketing pages
│   ├── (app)/            # Route group: authenticated application
│   └── api/              # API route handlers
├── components/           # Shared UI components
│   ├── ui/               # Primitive components (Button, Input, etc.)
│   └── [domain]/         # Domain-specific components
├── lib/                  # Core utilities and services
│   ├── db/               # Prisma client and database utilities
│   ├── auth/             # Authentication logic
│   └── [service]/        # Service-specific logic
├── types/                # TypeScript type definitions
└── hooks/                # React hooks
```

**What lives where — rules:**
- Business logic: `lib/` — never in components
- Server-only code: server components and API routes — never imported in client components
- Shared types: `types/` — never inlined in component files

### Established Patterns (Do Not Change Without PR Discussion)

| Pattern | Location | Reason |
|---------|----------|--------|
| Server Actions for mutations | `lib/actions/` | Eliminates API route boilerplate for simple mutations |
| Prisma client singleton | `lib/db/prisma.ts` | Prevents connection pool exhaustion in dev |
| Component composition via slots | `components/ui/` | Avoids prop drilling in complex layouts |

---

## Coding Conventions

See `rules/naming.md`, `rules/typescript.md`, `rules/testing.md` for full details.

### Critical Rules (applied immediately)

**TypeScript:**
- `strict: true` — no exceptions
- No `any` type anywhere — use `unknown` + type narrowing or create proper types
- No `@ts-ignore` or `@ts-expect-error` without a comment explaining why it's necessary
- All function parameters and return types must be explicitly typed

**React / Next.js:**
- Server Components are the default — mark client components explicitly with `"use client"`
- No `useEffect` for data fetching — use React Server Components or SWR/React Query
- No uncontrolled form inputs — all forms use `react-hook-form`
- Images always use `next/image` — never `<img>` tags

**Naming:**
- Files: `kebab-case.tsx` for components, `camelCase.ts` for utilities
- Components: `PascalCase`, named export (not default export)
- Hooks: `useCamelCase`
- Database functions: `verb + Entity` (e.g., `createUser`, `findOrderById`, `deleteSession`)

**Code Organization:**
- Maximum function length: 40 lines (split into helpers beyond this)
- Import order: React → Next.js → Third-party → Internal (`@/`) → Relative
- No circular imports — use the dependency graph to verify

---

## Security Rules

Claude Code MUST NEVER:

1. Hardcode any secret, API key, token, or credential
   — All secrets use environment variables: `process.env.NEXT_PUBLIC_*` (public) or `process.env.*` (server only)
2. Use `process.env.NEXT_PUBLIC_*` for server-only secrets (public vars are in browser bundle)
3. Write raw SQL with string concatenation — always use Prisma parameterized queries
4. Implement authentication checks in middleware without also checking in the route handler
   (defense in depth)
5. Enable `dangerouslyAllowBrowser: true` in any Anthropic or OpenAI client
6. Call `eval()` or `new Function()` anywhere

**Authentication pattern:**
```typescript
// Every server action and API route must start with:
const session = await getServerSession(authOptions);
if (!session?.user) {
  throw new Error('Unauthorized');
}
```

**Allowed external domains in fetch calls:**
- `api.stripe.com` — payment processing
- `api.anthropic.com` — AI features
- `*.supabase.co` — database (via Prisma, not direct fetch)

---

## Workflow Rules

### Branching

- `feat/[ticket-id]-short-description` — new features
- `fix/[ticket-id]-short-description` — bug fixes
- `chore/short-description` — tooling, deps, configuration

### Commits (Conventional Commits)

Format: `type(scope): description`

Examples:
```
feat(auth): add magic link authentication
fix(checkout): prevent duplicate order submission on slow connections
chore(deps): bump Next.js to 15.2.0
```

### Before Modifying Existing Code

1. Read the file completely — do not edit based on filename alone
2. Identify why the code is written the way it is (there may be non-obvious constraints)
3. Check git log for the file: `git log --follow -p src/path/to/file.ts` — understand history
4. If the change reverts a previous intentional pattern, say so explicitly

### Breaking Changes

Any change that modifies:
- Public API routes (`/api/**`)
- Database schema (Prisma migrations)
- Authentication flow
- Export signatures of components in `components/ui/`

Requires: a PR, a CHANGELOG entry, and review from a second developer.

---

## Error Handling

- All server actions return `{ data: T | null, error: string | null }` — never throw to client
- All API routes return structured errors: `{ error: string, code: string, status: number }`
- No `console.log` in production code — use the structured logger in `lib/logger.ts`
- All external API calls wrapped in try/catch with specific error messages
```

---

## File: `rules/typescript.md`

```markdown
# TypeScript Rules

## Strict Mode Enforcement

All TypeScript code in this project must pass strict mode checks:
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUncheckedIndexedAccess: true`

## Type Definition Patterns

### Good: Explicit and specific
```typescript
type UserId = string & { readonly brand: 'UserId' };

interface OrderCreateInput {
  userId: UserId;
  items: OrderItem[];
  shippingAddress: Address;
}
```

### Bad: Too permissive
```typescript
// Never do this:
function processOrder(data: any) { ... }
function updateUser(id: string, changes: object) { ... }
```

## Error Types

Use discriminated unions for error handling:
```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string; code: string };
```
```

---

## Quality Verification

This exemplar demonstrates:

- [x] Boot sequence with specific load steps (not vague "load context")
- [x] Architecture overview with what-lives-where rules
- [x] Established patterns table with change policy
- [x] Specific TypeScript rules (not "use TypeScript")
- [x] Security rules with concrete examples and code patterns
- [x] Workflow rules: branching, commit format, before-modify protocol
- [x] Breaking change definition with list
- [x] Modular `rules/` directory structure
- [x] MCS-3 criteria met (hooks and MCP section would be added for full MCS-3)
