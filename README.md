# 🧪 Orion Ops Automation Framework

Automated Selenium test framework for the **Orion Ops Web Application** (Dashboard, Upload, Conversions, Jobs, and Clusters).

---

## 🚀 Features
- Built using **Python + Selenium**
- Implements **Page Object Model (POM)** structure
- Generates detailed **Excel test reports**
- Modular and easy to extend for new test cases
- Configurable browser setup via `browser_setup.py`

---

## 📁 Project Structure
automation/
├── pages/ → Page object files (login, dashboard, upload)
├── tests/ → Test scripts for each module
├── utils/ → Helper utilities (browser setup, Excel logger)
└── run_tests.py → Master script to run all tests
reports/ → Generated Excel test results

## Create Virtual Environment
###  Linux / Mac
python -m venv .venv
source .venv/bin/activate                     
### OWindows
.venv\Scripts\activate                        

## Install Dependencies
pip install -r requirements.txt


# Running Tests

## Run individual test modules
python -m automation.tests.dashboard_test
python -m automation.tests.login_test
python -m automation.tests.upload_test

## Run all tests
python automation/run_tests.py


# Tech Stack
Component	Tool / Library
Language	Python 3.12+
Framework	Selenium WebDriver
Test Reports	Excel (via pandas)
Dependency Mgmt.	requirements.txt