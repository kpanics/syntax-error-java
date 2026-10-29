import re


class ValidationResult:
    def __init__(self, ok: bool, message: str = ""):
        self.ok = ok
        self.message = message


def balanced_braces(code: str) -> bool:
    cleaned = re.sub(r'//.*|/\*.*?\*/|"(?:\\.|[^"\\])*"', '', code, flags=re.S)
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for ch in cleaned:
        if ch in '({[':
            stack.append(ch)
        elif ch in ')}]':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


def semicolon_check(code: str) -> bool:
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith('//') or s.endswith('{') or s.startswith('*') or s.startswith('/*'):
            continue
        if not s.endswith(';') and not s.endswith('}'):
            return False
    return True


def validate(code: str, rules: dict) -> ValidationResult:
    checks = rules.get("structure_checks", {})

    if checks.get("balanced_braces") and not balanced_braces(code):
        return ValidationResult(False, "SyntaxError: unbalanced braces. The compiler is not amused.")
    if checks.get("semicolon_check") and not semicolon_check(code):
        return ValidationResult(False, "SyntaxError: expected ';'. The compiler is not amused.")

    # Автоматическая проверка всех *_regex из JSON (main_method_regex, lambda_regex и т.д.)
    for check_name, pattern in checks.items():
        if check_name.endswith("_regex"):
            if not re.search(pattern, code):
                return ValidationResult(False, f"StructureError: failed {check_name}")

    for req in rules.get("must_contain", []):
        if req not in code:
            return ValidationResult(False, f"Missing required element: {req}")

    for forb in rules.get("must_not_contain", []):
        if forb in code:
            return ValidationResult(False, f"Not allowed in this era: {forb}")

    return ValidationResult(True, "OK")