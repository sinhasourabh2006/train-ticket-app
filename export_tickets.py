import mysql.connector
from xhtml2pdf import pisa
from io import BytesIO

# DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9852',
    'database': 'train_ticket'
}

# Connect to DB
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM tickets")
tickets = cursor.fetchall()
cursor.close()
conn.close()

# Build HTML
html = """
<html>
<body>
    <h2>Train Ticket List</h2>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>PNR</th><th>From</th><th>To</th><th>Date & Time</th>
        </tr>
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

# Export to PDF
with open("all_tickets.pdf", "wb") as f:
    pisa.CreatePDF(html, dest=f)

print("✅ PDF created: all_tickets.pdf")
