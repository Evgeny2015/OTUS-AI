from typing import Any, Optional
import subprocess
import json
import os
import xml.etree.ElementTree as ET
from fastmcp import FastMCP, Context
from fastmcp.utilities.logging import get_logger
import coverage
import pytest
import logging



# Initialize FastMCP server
mcp = FastMCP("jwt-test-runner")

# Configure server logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mcp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("jwt-test-runner")
logger.info("initializing")

# Config client logging
to_client_logger = get_logger(name="fastmcp.server.context.to_client")
to_client_logger.setLevel(level=logging.INFO)


# Constants
DEFAULT_PROJECT_PATH = "../jwt"  # Relative path to the JWT project


def run_command(command: list[str], cwd: Optional[str] = None) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, and stderr."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def parse_xml_report(xml_content: str) -> dict:
    """Parse JUnit XML test report."""
    try:
        root = ET.fromstring(xml_content)
        testsuite = root.find("testsuite")
        if testsuite is None:
            return {"error": "No testsuite found in XML report"}

        return {
            "tests": int(testsuite.get("tests", 0)),
            "failures": int(testsuite.get("failures", 0)),
            "errors": int(testsuite.get("errors", 0)),
            "skipped": int(testsuite.get("skipped", 0)),
            "time": float(testsuite.get("time", 0)),
        }
    except Exception as e:
        return {"error": f"Failed to parse XML report: {str(e)}"}


@mcp.tool()
async def run_tests(
    test_path: str = ".",
    markers: str = "",
    parallel: bool = False,
    html_report: bool = False,
    xml_report: bool = False,
    json_report: bool = False
) -> str:
    """Execute test with customizable parameters.

    Args:
        test_path: Path to test files or directories (default: current directory)
        markers: Pytest markers to run (e.g., "not slow")
        parallel: Run tests in parallel using pytest-xdist
        html_report: Generate HTML report
        xml_report: Generate XML report
        json_report: Generate JSON report
    """
    logger.info(f"Running tests with params: test_path={test_path}, markers={markers}, parallel={parallel}")
    # Build pytest command
    cmd = ["python", "-m", "pytest", test_path]

    if markers:
        cmd.extend(["-m", markers])

    if parallel:
        cmd.extend(["-n", "auto"])

    # Add reporting options
    if html_report:
        cmd.extend(["--html=report.html", "--self-contained-html"])

    if xml_report:
        cmd.extend(["--junitxml=report.xml"])

    if json_report:
        cmd.extend(["--json-report", "--json-report-file=report.json"])

    # Run the command
    exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

    logger.info(f"Test run completed with exit code: {exit_code}")

    result = {
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "command": " ".join(cmd)
    }

    return json.dumps(result, indent=2)


@mcp.tool()
async def get_test_coverage(include: str = "*.py", omit: str = "") -> str:
    """Generate test coverage analysis and reporting.

    Args:
        include: File patterns to include in coverage (default: "*.py")
        omit: File patterns to omit from coverage
    """
    logger.info(f"Generating test coverage with params: include={include}, omit={omit}")
    try:
        # Start coverage
        cov = coverage.Coverage(include=include if include else None,
                               omit=omit if omit else None)
        cov.start()

        # Run tests
        cmd = ["pytest"]
        exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

        # Stop coverage
        cov.stop()
        cov.save()

        # Generate coverage report
        report_output = []
        try:
            # Get coverage report as string
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                cov.report(file=f)
            report_output.append(f.getvalue())
        except Exception as e:
            logger.error(f"Error generating coverage report: {str(e)}")
            report_output.append(f"Error generating coverage report: {str(e)}")

        logger.info(f"Coverage report generated: {report_output}")
        result = {
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "coverage_report": "\n".join(report_output),
            "command": " ".join(cmd)
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Failed to generate coverage: {str(e)}")
        return json.dumps({
            "error": f"Failed to generate coverage: {str(e)}",
            "command": "coverage report"
        }, indent=2)


@mcp.tool()
async def analyze_test_failures(test_path: str = ".") -> str:
    """Analyze failed tests and suggest fixes.

    Args:
        test_path: Path to test files or directories
    """
    logger.info(f"Analyzing test failures for path: {test_path}")

    # Run tests with verbose output to capture failures
    cmd = ["pytest", test_path, "-v", "--tb=short"]
    exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

    # Parse failures and provide suggestions
    failures = []
    lines = stdout.split('\n')

    current_failure = None
    for line in lines:
        if line.startswith("FAILED "):
            if current_failure:
                failures.append(current_failure)
            current_failure = {"test": line, "details": []}
        elif current_failure and line.strip() and not line.startswith("="):
            current_failure["details"].append(line.strip())

    if current_failure:
        failures.append(current_failure)

    # Provide suggestions based on common failure patterns
    suggestions = []
    if failures:
        suggestions.append("Common fixes for test failures:")
        suggestions.append("1. Check if test dependencies are properly installed")
        suggestions.append("2. Verify test data and fixtures are correct")
        suggestions.append("3. Ensure mock objects are properly configured")
        suggestions.append("4. Check for race conditions in async tests")
        suggestions.append("5. Verify environment variables and configuration")

    logger.info(f"Test failures found: {failures}")
    result = {
        "exit_code": exit_code,
        "failures": failures,
        "suggestions": suggestions,
        "stdout": stdout,
        "stderr": stderr,
        "command": " ".join(cmd)
    }

    return json.dumps(result, indent=2)


@mcp.tool()
async def list_test_files(ctx: Context) -> str:
    """Discover and list available test files."""
    # Send log message
    logger.info("Discover and list available test files")
    await ctx.info("Listing test files")

    # Find all Python files that look like test files
    cmd = ["pytest", "--collect-only", "-q"]
    exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

    # Parse test files from output
    test_files = []
    test_functions = []

    lines = stdout.split('\n')
    for line in lines:
        if line.startswith("<Module "):
            # Extract file name
            file_name = line.replace("<Module ", "").replace(">", "").strip()
            if file_name not in test_files:
                test_files.append(file_name)
        elif line.startswith("<Function "):
            # Extract test function name
            func_name = line.replace("<Function ", "").replace(">", "").strip()
            test_functions.append(func_name)

    result = {
        "test_files": test_files,
        "test_functions": test_functions,
        "total_files": len(test_files),
        "total_functions": len(test_functions),
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "command": " ".join(cmd)
    }

    logger.info("Result: OK")

    return json.dumps(result, indent=2)


@mcp.tool()
async def get_test_metrics(days: int = 7) -> str:
    """Get test execution statistics and trends.

    Args:
        days: Number of days to analyze for trends (default: 7)
    """
    logger.info(f"Getting test metrics for {days} days")
    # Run tests with JSON reporting for metrics
    cmd = ["pytest", "--json-report", "--json-report-file=metrics.json"]
    exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

    # Try to read the metrics file
    metrics_data = {}
    try:
        if os.path.exists(os.path.join(DEFAULT_PROJECT_PATH, "pytest_metrics.json")):
            with open(os.path.join(DEFAULT_PROJECT_PATH, "pytest_metrics.json"), "r") as f:
                metrics_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read metrics file: {str(e)}")
        metrics_data = {"error": f"Failed to read metrics file: {str(e)}"}

    # Extract basic metrics
    summary = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "duration": 0,
        "exit_code": exit_code
    }

    if "summary" in metrics_data:
        summary.update(metrics_data["summary"])

    # Add trend analysis suggestions
    trends = [
        "Trend analysis suggestions:",
        f"- Run tests regularly to track performance over {days} days",
        "- Monitor test execution time for performance degradation",
        "- Track failure rates to identify flaky tests",
        "- Compare test coverage across different time periods"
    ]

    logger.info("Result: OK")

    result = {
        "summary": summary,
        "trends": trends,
        "raw_metrics": metrics_data,
        "stdout": stdout,
        "stderr": stderr,
        "command": " ".join(cmd)
    }

    return json.dumps(result, indent=2)


@mcp.tool()
async def collect_pytest_json_metrics(test_path: str = ".", markers: str = "") -> str:
    """Collect pytest JSON metrics for test execution analysis.

    Args:
        test_path: Path to test files or directories (default: current directory)
        markers: Pytest markers to filter tests (e.g., "not slow")
    """
    logger.info(f"Collecting pytest JSON metrics for path: {test_path} with markers: {markers}")

    # Build pytest command with JSON reporting
    cmd = ["pytest", test_path, "--json-report", "--json-report-file=pytest_metrics.json"]

    if markers:
        cmd.extend(["-m", markers])

    # Run the command
    exit_code, stdout, stderr = run_command(cmd, DEFAULT_PROJECT_PATH)

    # Read the generated JSON metrics file
    metrics_data = {}
    metrics_file_path = os.path.join(DEFAULT_PROJECT_PATH, "pytest_metrics.json")

    try:
        if os.path.exists(metrics_file_path):
            with open(metrics_file_path, "r") as f:
                metrics_data = json.load(f)
        else:
            logger.warning("JSON metrics file was not generated")
            metrics_data = {"error": "JSON metrics file was not generated"}
    except Exception as e:
        logger.error(f"Failed to read JSON metrics file: {str(e)}")
        metrics_data = {"error": f"Failed to read JSON metrics file: {str(e)}"}

    # Prepare result
    result = {
        "exit_code": exit_code,
        "metrics": metrics_data,
        "stdout": stdout,
        "stderr": stderr,
        "command": " ".join(cmd)
    }

    logger.info("Pytest JSON metrics collection completed")
    return json.dumps(result, indent=2)


def main():
    """Initialize and run the JWT test runner MCP server."""
    # Initialize and run the server
    mcp.run()



if __name__ == "__main__":
    main()