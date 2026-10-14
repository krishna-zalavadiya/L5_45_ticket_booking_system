# Lab 5: Static Code Analysis — Issues

**File reviewed:** `ticket_booking_system.py`

The uploaded tool reports were generated against a version that already contained several fixes. Pylint reported a score of **7.24/10**, Flake8 reported an unused import, two long lines, and a missing final newline, and Bandit reported a hardcoded placeholder secret. The table below combines those report findings with security and correctness issues from the original program.

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Use of `eval()` for promotional expressions | Security — High | Original version: `compute_discounted_price()` | Evaluating a string can execute arbitrary Python code if the expression is user-controlled. | Accept a numeric discount percentage, validate its range, and calculate the price directly. |
| Shell command built with user-controlled filename | Security — High | Original version: `export_seating_chart()` | Concatenating a filename into `os.system()` can allow shell command injection. | Write the file with `Path.write_text()` and print the confirmation with `print()`. |
| Hardcoded secret placeholder | Security / configuration — Medium | Analyzed version: line 76 (Bandit B105) | Bandit flagged `REPLACE_WITH_A_SECURE_SECRET_KEY` as a hardcoded password-like string. A placeholder is not a usable secret. | Remove the hardcoded value. If a keyed hash is required, load a properly generated secret from an environment variable or secret manager. |
| Mutable default argument | Correctness — Medium | Original version: `reserveSeat()` | `order_history=[]` is created once and reused across calls, so data can leak between calls. | Use `history=None` and choose the history list inside the function. |
| Bare `except:` hides errors | Reliability — Medium | Original version: `cancel_seat()` | All exceptions are silently ignored, making unexpected bugs difficult to diagnose. | Check whether the seat exists and return a success/failure result. |
| MD5 used for ticket hash | Security — Medium | Original version: `generate_ticket_hash()` | MD5 is not suitable for modern security-sensitive cryptographic uses. A plain hash also does not authenticate a ticket. | Use SHA-256 for a fingerprint; use HMAC-SHA-256 with a securely stored key if authenticity is required. |
| Insecure random PIN generator | Security — Medium | Original version: `generate_booking_pin()` | `random` is not designed for security-sensitive PIN generation. | Use `secrets.randbelow()` and enforce expiration, attempt limits, and one-time use in a production system. |
| Missing module/function docstrings | Maintainability | Pylint lines 1, 16, 33, 42, 51, 72, 84, 89, 98, 108 in analyzed version | Pylint reported missing documentation. | Add a module docstring and a concise docstring to each function. |
| Non-snake_case function name | Style | Pylint line 16 in analyzed version | `reserveSeat` does not follow Python's standard function naming convention. | Rename it to `reserve_seat`. |
| Unused import | Style | Line 4 (Flake8 F401 / Pylint W0611) | `Path` was imported but reported as unused in the analyzed version. | Remove unused imports, or use `Path` for file handling. The cleaned version uses it. |
| Long lines and missing final newline | Style | Lines 34, 118, 138 (Flake8); line 138 (Pylint) | Lines exceeded the configured 79-character limit and the file lacked a final newline. | Wrap long statements and end the file with a newline. |
| Unused loop variable | Style | Pylint line 101 in analyzed version | The `seat` variable was assigned but never used. | Iterate over `seats.values()` when only seat details are needed. |

## Tool reports

- **Pylint:** initial uploaded report score was 7.24/10.
- **Flake8:** reported `F401`, two `E501` line-length violations, and `W292`.
- **Bandit:** reported `B105` for the hardcoded placeholder secret.

After saving the cleaned Python file, rerun the tools and update this document with the actual final output. Do not claim that an issue is cleared until you have run the tools against the final file.
