@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"
if errorlevel 1 (
    echo [ERROR] Unable to enter the DocMind project directory.
    goto :failed
)

if not exist "app.py" (
    echo [ERROR] app.py was not found in the project directory.
    goto :failed
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt was not found in the project directory.
    goto :failed
)

set "PYTHON_EXE="
set "PYTHON_ARGS="

where py >nul 2>&1
if not errorlevel 1 (
    for %%V in (3.13 3.14 3.12 3.11 3.10) do (
        if not defined PYTHON_EXE (
            py -%%V -c "import sys" >nul 2>&1
            if not errorlevel 1 (
                set "PYTHON_EXE=py"
                set "PYTHON_ARGS=-%%V"
            )
        )
    )
    if not defined PYTHON_EXE (
        py -3 -c "import sys" >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON_EXE=py"
            set "PYTHON_ARGS=-3"
        )
    )
)

if not defined PYTHON_EXE (
    where python >nul 2>&1
    if not errorlevel 1 (
        python -c "import sys" >nul 2>&1
        if not errorlevel 1 set "PYTHON_EXE=python"
    )
)

if not defined PYTHON_EXE (
    echo [ERROR] Python was not found.
    echo Install Python 3.13 and enable "Add Python to PATH" during setup.
    goto :failed
)

%PYTHON_EXE% %PYTHON_ARGS% -c "import sys; raise SystemExit(0 if sys.version_info.major == 3 and sys.version_info.minor in range(10, 15) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] DocMind supports Python 3.10-3.14. Python 3.13 is recommended.
    %PYTHON_EXE% %PYTHON_ARGS% --version
    goto :failed
)

set "NEW_VENV=0"
set "NEED_INSTALL=0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] First run: creating the .venv virtual environment...
    %PYTHON_EXE% %PYTHON_ARGS% -m venv ".venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create the virtual environment.
        goto :failed
    )

    set "NEW_VENV=1"
    set "NEED_INSTALL=1"
) else (
    if not exist ".venv\.docmind-v2.2-ready" (
        ".venv\Scripts\python.exe" -c "import streamlit, openai, httpx, docx, pdfplumber, openpyxl, reportlab, ddgs, defusedxml" >nul 2>&1
        if errorlevel 1 (
            set "NEED_INSTALL=1"
        ) else (
            > ".venv\.docmind-v2.2-ready" echo DocMind V2.2 environment ready.
        )
    )
)

if "!NEED_INSTALL!"=="1" (
    if "!NEW_VENV!"=="0" echo [INFO] The existing .venv is missing dependencies. Repairing it...

    if "!NEW_VENV!"=="1" (
    echo [INFO] Upgrading pip...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    if errorlevel 1 (
        echo [ERROR] Failed to upgrade pip. Check the network connection and retry.
        goto :failed
    )
    )

    echo [INFO] Installing requirements.txt...
    ".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed. Review the error above and check the network connection.
        goto :failed
    )
    > ".venv\.docmind-v2.2-ready" echo DocMind V2.2 environment ready.
) else (
    echo [INFO] Reusing the existing .venv; dependencies will not be reinstalled.
)

echo [INFO] Starting DocMind AI...
".venv\Scripts\python.exe" -m streamlit run "app.py"
set "APP_EXIT_CODE=%ERRORLEVEL%"

echo.
if "%APP_EXIT_CODE%"=="0" (
    echo [INFO] Streamlit exited normally.
) else (
    echo [ERROR] Streamlit exited with code %APP_EXIT_CODE%.
)
pause
exit /b %APP_EXIT_CODE%

:failed
echo.
echo Startup did not complete. Fix the issue shown above and retry.
pause
exit /b 1
