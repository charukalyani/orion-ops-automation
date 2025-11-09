from automation.tests.login_test import run_login_tests
from automation.tests.dashboard_test import run_dashboard_tests

def main():
    print("Running all automated tests...")
    run_login_tests()
    run_dashboard_tests()
    print("All tests completed successfully.")

if __name__ == "__main__":
    main()
