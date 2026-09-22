# Case Study: ShopEase — A Memory-Aware Shopping Assistant

**Track:** Agentic AI
**Lesson basis:** `04_memory_agent.ipynb` — Short-Term (In-Session) Memory
**Presented by:** Sharad Rajore | **Organization:** Zensar Technologies
**Audience:** L3 participants building toward a production-ready, customer-facing use case

---

## 1. Business Context

**ShopEase** is a mid-size e-commerce retailer piloting an AI shopping assistant on its website and mobile app. Customer support leadership has approved the pilot on one condition:

> *"The bot cannot act like it's meeting the customer for the first time every time they say something. If it forgets what's in their cart or what they just asked, we will get worse reviews than having no bot at all."*

You are the engineering team responsible for taking the assistant from a stateless demo to a pilot-ready build. This case study walks you through that journey using exactly the three memory approaches from Lesson A — but applied to a real product surface instead of the weather/stock toy tools.

**Your deliverable is not a notebook that "runs once."** It is something you could screen-share to a ShopEase product manager and say, convincingly, "this is ready for a limited pilot."

---

## 2. The Problem, In ShopEase's Words

Support has logged three real complaints from the internal beta:

| # | Customer said | Bot did |
|---|---|---|
| 1 | "Add the blue sneakers to my cart." → next message: "Actually make it size 9." | Asked "What item are you referring to?" |
| 2 | Two beta testers used the bot at the same time from two browser tabs | One tester saw the *other* tester's cart contents |
| 3 | The staging server restarted mid-conversation (routine deploy) | Every active shopper's cart and conversation vanished |

Each row maps directly to a gap you will close:

- Row 1 → **no memory at all** (Part 1 of the lesson)
- Row 2 → **memory that isn't isolated per session** (motivates `thread_id`)
- Row 3 → **memory that isn't durable** (motivates `SqliteSaver`)

---

## 3. Learning Objectives Mapped to This Case Study

| Notebook concept | ShopEase milestone |
|---|---|
| Manual message history (`conversation_history` list) | M1 — Prove the bug, then patch it by hand |
| `MemorySaver` + `thread_id` | M2 — Multi-shopper session isolation |
| `SqliteSaver` | M3 — Survive a server restart |
| Everything above, integrated | M4 — Pilot-readiness demo |

---

## 4. Functional Requirements

Build a agent (`create_agent`) for ShopEase with the following tools. Model them on `get_weather` / `get_stock_price` from the notebook — plain Python functions decorated with `@tool`, returning strings, backed by an in-memory mock "database" (a Python dict is fine; no real DB needed for this exercise).

| Tool | Signature | Behavior |
|---|---|---|
| `search_products` | `search_products(query: str) -> str` | Returns 2–3 matching items from a hardcoded catalog (name, price, sizes/colors available) |
| `add_to_cart` | `add_to_cart(item_name: str, size: str = None) -> str` | Adds an item to *that session's* cart; confirms what was added |
| `view_cart` | `view_cart() -> str` | Lists current cart contents and running total |
| `check_order_status` | `check_order_status(order_id: str) -> str` | Returns a mock status for a hardcoded set of order IDs |
| `apply_discount_code` | `apply_discount_code(code: str) -> str` | Validates against 1–2 hardcoded codes, applies a discount to the cart total |

**System prompt requirement:** the assistant must be told, explicitly, to use cart/session context rather than re-asking the customer for information already provided in the conversation.

---

## 5. Milestones

### M1 — Prove the Bug, Then Patch It Manually
1. Build the agent **without** a checkpointer.
2. Write a 3-turn script that reproduces complaint #1 above (name an item, then say "actually make it size 9" without repeating the item name). Capture the failure — this is your "before" evidence for the demo.
3. Now fix it using the **manual history** pattern (a Python list you append to and pass back in on every `invoke`). Re-run the same script and capture the "after" evidence.
4. Document, in your own words, why this fix does not scale past a single-user prototype (tie back to the table under "Approach 1 Limitations" in the notebook).

**Exit criteria:** a before/after transcript, plus 3–4 bullet points on why M1's approach can't ship.

### M2 — Multi-Shopper Session Isolation
1. Swap the manual list for `MemorySaver` + `thread_id`.
2. Reproduce complaint #2: simulate two shoppers (`thread_id="shopper_A"`, `thread_id="shopper_B"`) adding *different* items to their carts in an interleaved sequence, then ask each "what's in my cart?" and confirm no cross-contamination.
3. Inspect the checkpoint directly (`memory.get(config)`) for one thread and explain in one paragraph what LangGraph is storing on your behalf.

**Exit criteria:** an isolation test that programmatically asserts (not just eyeballs) that shopper A never sees shopper B's cart items.

### M3 — Survive a Restart
1. Swap `MemorySaver` for `SqliteSaver` pointed at a `shopease_sessions.db` file.
2. Simulate complaint #3: run a session, add items to a cart, then **actually tear down and recreate the checkpointer object** (simulating a process restart — this mirrors the "Session 2" cell in the notebook) and resume with the same `thread_id`.
3. Confirm the cart survived the "restart" by asking the bot to `view_cart`.

**Exit criteria:** a script that closes and reopens the SQLite connection mid-run and proves state survived, plus the resulting `.db` file.

### M4 — Pilot-Readiness Demo (Customer-Facing Milestone)
This is the milestone that makes the exercise "customer ready," not just "technically correct." Prepare a 5-minute walkthrough as if presenting to the ShopEase product manager who filed the three complaints. Your demo must:

1. Open with the three original complaints, restated as *resolved*.
2. Run one live end-to-end shopper journey: search → add to cart → change mind on size → apply a discount code → close the tab → come back with the same `thread_id` → check cart → check an order status.
3. Explicitly call out **which memory approach (M1/M2/M3) is powering production** and why the other two are dev-only / insufficient.
4. State one honest limitation of your current build and how you'd address it next (see Section 7 — this is where you gesture at long-term/user-scoped memory, which is explicitly *out of scope* for this build but worth naming).

---

## 6. Non-Functional Requirements (What Makes This "Production," Not "Demo")

Address each of these in your write-up — a sentence or two each is fine, but do not skip any:

- **Session ID strategy:** how would `thread_id` actually get generated/passed in a real web app (hint: not typed by hand — think cookies, auth tokens, or a session header)?
- **Context growth:** what happens to this agent's cost and latency after 200 turns in one thread? Propose (in words, no code required) one mitigation.
- **PII handling:** the cart and order tools will eventually touch names, addresses, order history. What would you *not* want stored in a checkpoint that never expires?
- **Failure mode:** what should the bot say if `SqliteSaver` can't reach the `.db` file (disk full, permissions)? "Crash" is not an acceptable answer for a customer-facing surface.
- **Concurrency:** two browser tabs, same shopper, same `thread_id` — what could go wrong, and is that in scope for this pilot or a known limitation?

---

## 7. Stretch Goal (Optional — Not Graded)

Complaint pattern you'll likely hit if you push this further: a shopper closes the tab, comes back **next week in a brand-new session**, and asks "do you remember my size preference?" — and the bot has no idea, because a new `thread_id` means a blank slate even with `SqliteSaver`.

That gap is real, and it's *not* solved by anything in this case study — it requires a second, user-scoped store (keyed by `user_id`, not `thread_id`) sitting alongside the checkpointer. If you want to explore it independently, look at how `store` differs from `checkpointer` in LangGraph. **Do not implement this for M1–M4** — name it in your M4 demo as the acknowledged next step, that's enough.

---

## 8. Deliverables Checklist

- [ ] Working notebook or `.py` module implementing M1–M3, each in its own clearly labeled section
- [ ] Before/after transcript for M1
- [ ] Isolation test output for M2
- [ ] Restart-survival proof (script output + resulting `.db` file) for M3
- [ ] One-page write-up covering Section 6 (non-functional requirements)
- [ ] 5-minute live demo per M4, delivered to the group as if the group is the ShopEase stakeholder

---

## 9. Evaluation Rubric

| Criterion | Weight | What "good" looks like |
|---|---|---|
| Correctness of each milestone | 30% | M1–M3 each demonstrably fix the complaint they target |
| Multi-user isolation proof (M2) | 15% | Assertion-based test, not just visual inspection |
| Durability proof (M3) | 15% | Genuine teardown/recreate of the checkpointer, not just re-running the same process |
| Non-functional write-up | 15% | Specific to ShopEase's context, not generic textbook answers |
| Demo quality (M4) | 20% | Framed around the original complaints; honest about limitations; runs live without errors |
| Code clarity | 5% | Tool functions are small, named clearly, mirror the notebook's style |

---

## 10. Reference Material

- `04_memory_agent.ipynb` — all three memory approaches, plus the thread-isolation demo you'll adapt for M2 and the SQLite session-restart demo you'll adapt for M3.
- Reuse the `chat()` manual-history helper pattern from Approach 1 as your M1 starting point.
- Reuse the `config = {"configurable": {"thread_id": ...}}` pattern from Approach 2 as your M2 starting point.
- Reuse the `SqliteSaver.from_conn_string(db_path)` pattern from Approach 3 as your M3 starting point.
