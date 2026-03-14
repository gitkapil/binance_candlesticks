#!/bin/bash

# Run Behave and generate JSON report
python -m behave -f json -o reports/report.json

# Convert JSON report to HTML
python json_to_html.py

echo "Reports generated: reports/report.json and reports/report.html"
