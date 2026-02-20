# JWT Project Test Coverage Analysis

## Summary

- **Total Coverage**: 54%
- **Total Statements**: 292
- **Missed Statements**: 134

## File-by-File Coverage

| File | Statements | Missed | Coverage |
|------|------------|--------|----------|
| main.py | 77 | 77 | 0% |
| simple_test.py | 71 | 26 | 63% |
| test_client.py | 61 | 29 | 52% |
| test_jwt_service.py | 83 | 2 | 98% |
| **TOTAL** | **292** | **134** | **54%** |

## Coverage Reports Generated

1. HTML Report: `htmlcov/index.html`
2. XML Report: `coverage.xml`

## Notes

The main application file (`main.py`) shows 0% coverage because the tests primarily focus on testing the API endpoints through HTTP requests rather than directly testing the functions. This is a common pattern for API testing where the focus is on integration testing rather than unit testing individual functions.