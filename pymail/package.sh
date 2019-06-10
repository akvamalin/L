#!/bin/bash
rm -rf package.zip
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt --target libs
cd libs
zip -r ../package.zip .
cd ..
zip -g package.zip src/main.py
rm -rf libs