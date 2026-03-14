import json

with open('reports/report.json') as f:
    data = json.load(f)

html = ['<html><head><title>Behave Test Report</title></head><body>']
html.append('<h1>Behave Test Report</h1>')

for feature in data:
    html.append(f"<h2>Feature: {feature['name']}</h2>")
    for scenario in feature['elements']:
        html.append(f"<h3>Scenario: {scenario['name']}</h3>")
        html.append('<ul>')
        for step in scenario['steps']:
            status = step.get('result', {}).get('status', 'N/A')
            html.append(f"<li>{step['keyword']} {step['name']} - <b>{status}</b></li>")
        html.append('</ul>')
html.append('</body></html>')

with open('reports/report.html', 'w') as f:
    f.write('\n'.join(html))

print("HTML report generated at reports/report.html")
