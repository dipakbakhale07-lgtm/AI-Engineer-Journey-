# DAY 8 PRACTICE — RAG User Experience

## Project

RAG Assistant

## Objective

Improve the RAG Assistant so another person can understand and use it
without detailed instructions.

## Interface Tested

- Streamlit interface
- Project title
- User instruction
- Question input
- Ask button
- Answer display
- Source display

## Functional Tests

### Test 1 — Normal Question

Question:

What is RAG?

Result:

Answer generated successfully.

Status: PASS

---

### Test 2 — Lowercase Question

Question:

what is rag?

Result:

The question was processed successfully.

Status: PASS

---

### Test 3 — Empty Question

Question:

No question entered.

Expected:

Friendly warning asking the user to enter a question.

Status: PASS

---

### Test 4 — Source Display

The source information was displayed below the answer.

Status: PASS

---

### Test 5 — Independent User Test

A family member/friend used the RAG Assistant and tried 5 questions
without detailed instructions.

Status: PASS

## Tester Feedback

The tester was able to understand and use the interface independently.

No major confusion was reported.

## Day 8 Learning

A RAG application should be understandable to users, not only
technically functional.

The interface should provide:

1. Clear instructions
2. Simple input
3. Clean output
4. Source information
5. Friendly error messages

## Result

Day 8 practical work completed.