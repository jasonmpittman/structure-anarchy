#!/bin/bash

echo "Creating directories..."
mkdir pdfs
mkdir processed_pdfs
mkdir texts
mkdir processed_texts
mkdir data

echo "Creating Python virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "installing dependencies"
pip install -r requirements

