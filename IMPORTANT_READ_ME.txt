===============================================================================
  HOW TO RUN THE VOLUNTEER MANAGEMENT SYSTEM
===============================================================================

PROBLEM: "ModuleNotFoundError: No module named 'flask'"

WHY IT HAPPENS:
Your PowerShell doesn't automatically find the Python packages because they're
installed in a user directory.

SOLUTION - USE ONE OF THESE METHODS:

===============================================================================
METHOD 1: Double-click RUN.bat (EASIEST - RECOMMENDED)
===============================================================================
Just double-click the file: RUN.bat

This automatically sets up everything and starts the app.


===============================================================================
METHOD 2: Use PowerShell with environment variable
===============================================================================
Open PowerShell in this folder and run:

$env:PYTHONPATH = "$env:APPDATA\Python\Python313\site-packages"
python app.py


===============================================================================
METHOD 3: Use START_APP.bat
===============================================================================
Double-click: START_APP.bat


===============================================================================
METHOD 4: One-line PowerShell command
===============================================================================
$env:PYTHONPATH = "$env:APPDATA\Python\Python313\site-packages"; python app.py


===============================================================================
AFTER STARTING THE APP:
===============================================================================
1. Wait for "Server starting at http://localhost:5000"
2. Open your browser
3. Go to: http://localhost:5000
4. Use the volunteer management system!


===============================================================================
IMPORTANT NOTES:
===============================================================================
- You MUST be in the project folder when running
- Current folder: C:\Users\pathi\OneDrive\Desktop\New folder
- All Python packages ARE installed correctly
- The PYTHONPATH setting is required to find them


===============================================================================
QUICK START:
===============================================================================
Double-click: RUN.bat

Then open: http://localhost:5000

That's it!
===============================================================================

