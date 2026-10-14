# Lab 5: Static Code Analysis — Reflection

**Note:** The assignment refers to four reflection questions from the lab handout, but the questions themselves were not included with the provided material. The responses below address four common reflection themes. Replace the headings with the handout's exact questions if they differ.

## 1. What did the static analysis tools find?

Pylint identified maintainability and style problems, including missing docstrings, a function name that did not follow snake_case, an unused import and variable, and a missing final newline. Flake8 independently identified an unused import, long lines, and the missing final newline. Bandit flagged a hardcoded password-like placeholder. The uploaded Pylint report gave a score of 7.24/10.

## 2. Which issues were most important, and why?

Security issues were the highest priority. Using `eval()` on an externally controlled promotional expression can execute unintended code. Building a shell command by concatenating a filename can create command-injection risk. A hardcoded secret can be exposed in source control. The original mutable default list and broad exception handler were also correctness and reliability problems because they could retain unexpected state or hide errors.

## 3. How were the issues fixed?

The cleaned program accepts a numeric discount percentage instead of evaluating a string, validates seat IDs and discount ranges, uses `None` instead of a mutable default list, and returns an explicit result when cancelling a seat. It uses `secrets` for PIN generation, SHA-256 for a ticket fingerprint, `Path.write_text()` for file output, docstrings for functions, snake_case naming, and a main guard. The code no longer invokes a shell command to print the export message.

## 4. What are the limitations of static analysis?

Static analysis can identify many suspicious patterns without executing the program, but it cannot prove that the program is correct or secure. Some problems require running tests or reviewing the program's behavior and design. For example, a linter may not detect a double-booking race condition caused by simultaneous requests, and a hash function alone does not guarantee ticket authenticity. I would combine Pylint, Flake8, and Bandit with functional tests, code review, and database-level concurrency controls before deploying a real booking system.
