import mysql.connector
import pandas as pd
import xlsxwriter

# Connect to the MySQL database
cnx = mysql.connector.connect(user='username', password='password',
                              host='localhost', database='zabbix')

# Define the SQL query to retrieve monthly data
query = """
SELECT
    FROM_UNIXTIME(clock, '%Y-%m') AS Month,
    AVG(value) AS 'Total CPU',
    AVG(memtotal) AS 'Total Memory',
    AVG(memfree) / AVG(memtotal) AS 'Memory Utilization',
    AVG(value) / 100 AS 'CPU Utilization'
FROM
    history_uint
WHERE
    itemid IN (
        SELECT itemid
        FROM items
        WHERE name LIKE 'CPU Total' OR name LIKE 'Memory Total'
    )
    AND clock >= UNIX_TIMESTAMP(DATE_FORMAT(NOW(), '%Y-%m-01'))
    AND clock < UNIX_TIMESTAMP(DATE_FORMAT(NOW() + INTERVAL 1 MONTH, '%Y-%m-01'))
GROUP BY
    FROM_UNIXTIME(clock, '%Y-%m')
"""

# Retrieve the data from the database using Pandas
data = pd.read_sql_query(query, cnx)

# Write the data to an Excel file using XlsxWriter
writer = pd.ExcelWriter('monthly_report.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
format_pct = workbook.add_format({'num_format': '0%'})
worksheet.set_column('D:D', None, format_pct)
writer.save()

# Close the database connection
cnx.close()
