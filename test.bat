rmdir /S /q venv
python3 -m venv venv
venv\Scripts\activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 3_chromophore_vibronic_simulation.py output 1 2 3 4 5 6 7 8 9 0 1 2 3
deactivate
