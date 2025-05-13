@REM Set up a clean Python virtual environment for the test.
@REM Really this only needs to be done when the dependencies change.
rmdir /S /q venv
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

@REM Run the Python file with some bogus input that doesn't fail.
python 3_chromophore_vibronic_simulation.py output 2 2 2 2 2 2 2 2 2 2 2 2 2

@REM Deactivate the virtual environment when we're done.
deactivate
