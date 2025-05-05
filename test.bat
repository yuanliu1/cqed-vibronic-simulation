rmdir /S /q venv
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python 3_chromophore_vibronic_simulation.py output 2 2 2 2 2 2 2 2 2 2 2 2 2
deactivate
