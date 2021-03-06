import json
import urllib.parse
import psycopg2

print('Loading function')

dbname = ''
host = ''
port = ''
user = ''
password = ''
iam_role = ''

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    company_id = event['responsePayload']['company_id']
    unload_query=f"UNLOAD (' \
    select payment, sum(total) total_sales \
    FROM SUPERMARKET_SALES  \
    WHERE COMPANY_NAME = ''{company_id}'' \
    group by payment \
    order by 2 desc') \
    to 's3://rseg176-filewarehouse/sales_reports_out/{company_id}/Payment_Type_Sales.csv_' \
    credentials 'aws_iam_role={iam_role}' \
    CSV delimiter ',' HEADER PARALLEL OFF allowoverwrite;"

    try:
        con=psycopg2.connect(dbname=dbname, host=host, 
        port=port, user=user, password=password)
        cur = con.cursor()
        cur.execute(unload_query)
        con.commit()
        cur.close() 
        con.close()

    except Exception as e:
        print(e)
        print('Error generating branch sales reports')
        raise e

    print('COMPLETE')
    return {'company_id':company_id}
