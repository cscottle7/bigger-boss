#!/usr/bin/env python3
"""Quick test of core Bigger Boss functionality."""

import json
import sys
from pathlib import Path

def test_basic_functionality():
    """Test basic system components."""
    results = {}

    # Test 1: Check if core files exist
    project_root = Path(__file__).parent
    core_files = [
        '.claude/hooks.json',
        'scripts/md_to_docx.py',
        'scripts/gdrive_upload.py',
        'scripts/web_scraper_cli.py',
        'scripts/hooks/performance_monitor.py',
        'scripts/hooks/client_activity_tracker.py'
    ]

    print("Testing core files...")
    for file_path in core_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        results[file_path] = exists
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {file_path}: {'Found' if exists else 'Missing'}")

    # Test 2: Check hooks configuration
    hooks_file = project_root / '.claude/hooks.json'
    if hooks_file.exists():
        try:
            with open(hooks_file, 'r', encoding='utf-8') as f:
                hooks_config = json.load(f)
            results['hooks_valid'] = True
            print("[OK] Hooks configuration is valid JSON")
        except Exception as e:
            results['hooks_valid'] = False
            print(f"[ERROR] Hooks configuration error: {e}")

    # Test 3: Test Python imports
    print("\nTesting Python dependencies...")
    dependencies = [
        ('python-docx', 'docx'),
        ('markdown', 'markdown'),
        ('beautifulsoup4', 'bs4'),
        ('psutil', 'psutil'),
        ('python-decouple', 'decouple')
    ]

    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            results[f'import_{import_name}'] = True
            print(f"[OK] {dep_name}: Available")
        except ImportError:
            results[f'import_{import_name}'] = False
            print(f"[MISSING] {dep_name}: Missing")

    return results

def main():
    print("Bigger Boss Agent System - Quick Test\n")

    results = test_basic_functionality()

    # Summary
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)

    print(f"\nTest Summary:")
    print(f"Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

    if passed_tests == total_tests:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {total_tests - passed_tests} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())