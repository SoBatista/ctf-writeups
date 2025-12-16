# picoCTF asm2 Solver Scripts

This repository contains two Python scripts used to solve **picoCTF asm2-style reverse engineering challenges**.
Both scripts compute the return value of the `asm2` function by analyzing its assembly logic.

They serve different purposes:

* one is **simple and educational**
* the other is **fully automated and assembly-driven**

---

## Script 1: Simple Python Translation

### Purpose

This script is a **direct Python translation** of the `asm2` function.
It is ideal for:

* learning
* validating your manual reasoning
* confirming the final result

### How it works

* Manually mirrors the assembly logic
* Uses the loop condition and updates exactly as seen in `test.S`
* Requires you to already know the arguments and constants

### Example Code

```python
def asm2(arg1, arg2):
    local1 = arg2
    local2 = arg1

    while local2 <= 0x2d12:
        local1 += 1
        local2 += 0x9f

    return hex(local1)

print(asm2(0x6, 0x21))
```

### How to run

```bash
python3 asm2_simple.py
```

### Output

```text
0x6a
```

---

## Script 2: Automated asm2 Solver (pwntools version)

### Purpose

This script is the **extra-nerdy version** 😄.

It:

* reads the assembly **directly from disk or a URL**
* parses the loop logic automatically
* computes the result **without hard-coding constants**
* works for many asm2 variants

This is useful if:

* the constants change
* you want a reusable solver
* you enjoy abusing pwntools whenever possible
* or simply if you want to extend your toolkit a bit

---

### Requirements

```bash
pip install pwntools
```

---

### How it works

1. Loads `test.S` from:

   * a local file **or**
   * a remote URL (wget-style)
2. Parses the assembly to extract:

   * how `local1` changes per iteration
   * how `local2` changes per iteration
   * the loop termination threshold
3. Solves the loop mathematically (no brute force)
4. Prints the returned value in hexadecimal

---

### Basic usage (local file)

```bash
python3 full_script.py test.S
```

---

### Download and solve from a URL

```bash
python3 full_script.py https://example.com/test.S
```

---

### Custom arguments

If the challenge uses different arguments:

```bash
python3 full_script.py test.S --arg1 0x6 --arg2 0x21
or
python3 full_script.py https://example.com/test.S --arg1 0x6 --arg2 0x21
```

Arguments default to:

```text
arg1 = 0x6
arg2 = 0x21
```

---

### Example output

```text
[*] Parsed loop constants:
[*]   local1 delta/iter = 1
[*]   local2 delta/iter = 159
[*]   threshold         = 0x2d12
[+] Computed iterations: 73
0x6a
```

---

## When to Use Which Script

| Script                | Use Case                         |
| --------------------- | -------------------------------- |
| Simple Python version | Learning, writeups, validation   |
| pwntools solver       | Automation, reusability, flexing |

---

## Notes

* The pwntools solver assumes the **standard asm2 layout**:

  * locals at `[ebp-0x4]` and `[ebp-0x8]`
  * loop controlled by `cmp` + `jle`
* If the assembly structure changes significantly, the regex parser may need adjustment.

---

## Final Thoughts

These scripts show two equally valid approaches to reverse engineering:

* **understanding the logic**
* **automating the analysis**

Both are valuable skills.

Happy hacking
