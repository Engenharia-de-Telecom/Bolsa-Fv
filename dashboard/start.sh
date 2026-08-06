#!/bin/sh

echo "Iniciando serial_reader..."

python serial_reader.py &

echo "Iniciando dashboard..."

python app.py