REM Basic smoke tests (no HTML report)
pytest -m "smoke" -v

REM UI tests only
pytest -m "ui" -v

REM API tests only  
pytest -m "api" -v

REM Security tests
pytest -m "security" -v

REM All tests with simple text output
pytest -v > test_results.txt

REM Generate HTML report with encoding fix
chcp 65001
set PYTHONIOENCODING=utf-8
pytest -m "smoke" --html=reports/smoke_report.html --self-contained-html

REM Run specific test file
pytest tests/ui/test_login.py -v

REM Run with detailed output
pytest -m "smoke" -v -s --tb=short