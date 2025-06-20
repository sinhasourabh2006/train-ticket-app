import mysql.connector
from xhtml2pdf import pisa
from datetime import datetime

# User input for date
date_input = input("Enter date (YYYY-MM-DD): ").strip()

try:
    # Validate date format
    datetime.strptime(date_input, "%Y-%m-%d")
except ValueError:
    print("❌ Invalid date format! Use YYYY-MM-DD.")
    exit()

# DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9852',
    'database': 'train_ticket'
}

# Connect and fetch data
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT * FROM tickets
    WHERE DATE(datetime) = %s
""", (date_input,))
tickets = cursor.fetchall()
cursor.close()
conn.close()

if not tickets:
    print("⚠️ No tickets found for this date.")
    exit()

# HTML generation
html = f"""
<html>
<body>
    <h2>Train Tickets on {date_input}</h2>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>PNR</th><th>From</th><th>To</th><th>Date & Time</th></tr>
"""

for ticket in tickets:
    html += f"""
    <tr>
        <td>{ticket['pnr']}</td>
        <td>{ticket['from_station']}</td>
        <td>{ticket['to_station']}</td>
        <td>{ticket['datetime']}</td>
    </tr>
    """

html += """
    </table>
</body>
</html>
"""

# Export PDF
pdf_filename = f"tickets_{date_input}.pdf"
with open(pdf_filename, "wb") as f:
    pisa.CreatePDF(html, dest=f)

print(f"✅ PDF created: {pdf_filename}")
