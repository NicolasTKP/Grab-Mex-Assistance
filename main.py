import streamlit as st
import vanna
from vanna.remote import VannaDefault

def init():
    merchant_id = "3e2b6"

    api_key = "2f8e680c8f324b95885327d83d1fe9c4"

    vanna_model_name = "grab-mex-ai" # https://vanna.ai/account/profile 
    vn = VannaDefault(model=vanna_model_name, api_key=api_key)

    vn.connect_to_mssql(odbc_conn_str='DRIVER={ODBC Driver 17 for SQL Server};SERVER=LOCALHOST;DATABASE=GrabFoodDB;Trusted_Connection=Yes;TrustServerCertificate=Yes;')

    return merchant_id, vn

def get_model_response(prompt, merchant_id, vn):    
    prompt = "My merchant id is " + merchant_id + ". " + prompt
    answer = vn.ask(question=prompt, visualize=False, print_results=False, allow_llm_to_see_data=True)
    print("Generated SQL:\n", answer[0])
    print("Answer:\n", answer[1])
    return answer[0], answer[1]

def gui():
    st.set_page_config(page_title="AI Assistant", layout="centered")
    st.title("Grab MEX AI Assistant")

    user_input = st.text_input("Ask me anything:")

    if user_input:
        merchant_id, vn = init()
        sql, response = get_model_response(user_input, merchant_id, vn)

        st.write("### Assistant's Response:")


        column_names = response.columns.tolist()
        print(column_names)

        st.success(response)
        st.data_editor(response)
        try:
            st.line_chart(response)
            st.area_chart(response)
            st.bar_chart(response)
        except:
            st.write("No chart available for this data.")

        if "driver_lead_time" in sql:
            query = "SELECT MAX(driver_lead_time) AS longest_driver_lead_time FROM transaction_data WHERE merchant_id = '3e2b6'"
            result = vn.run_sql(query)
            if result["longest_driver_lead_time"][0] > 15:
                st.warning(f"### Warning: The longest driver lead time is {result['longest_driver_lead_time'][0]} minutes, which is above the threshold. You might want to consider enabling Pre Order function.")

        elif "item_id" in sql or "item_name" in sql:
            query = "SELECT TOP 1 i.item_name, COUNT(ti.item_id) AS total_sales FROM transaction_items ti JOIN items i ON ti.item_id = i.item_id JOIN transaction_data td ON ti.order_id = td.order_id WHERE td.merchant_id = '3e2b6' GROUP BY i.item_name ORDER BY total_sales DESC;"
            result = vn.run_sql(query)
            if result["total_sales"][0] > 400:
                st.success(f"### The item {result['item_name'][0]} has been sold more than {result['total_sales'][0]} times. You might want to consider prepare more stock for it.")
            
            query = "SELECT TOP 1 i.item_name, COUNT(ti.item_id) AS total_sales FROM transaction_items ti JOIN items i ON ti.item_id = i.item_id JOIN transaction_data td ON ti.order_id = td.order_id WHERE td.merchant_id = '3e2b6' GROUP BY i.item_name ORDER BY total_sales ASC;"
            result = vn.run_sql(query)
            if result["total_sales"][0] < 100:
                st.success(f"### The item {result['item_name'][0]} has been sold less than {result['total_sales'][0]} times. You might want to consider remove it from the menu or create a promotion for it.")

        elif "keyword" in sql:
            query = "SELECT TOP 3 k.keyword AS item_name, k.[view], k.[menu], k.[checkout], k.[order] FROM keywords k JOIN items i ON k.keyword = i.item_name WHERE i.cuisine_tag IN (SELECT cuisine_tag FROM items WHERE merchant_id = '3e2b6') AND k.keyword NOT IN (SELECT item_name FROM items WHERE merchant_id = '3e2b6') ORDER BY k.[view] DESC, k.[order] DESC;"
            st.write("### Here is some top order items from your competitors, you might want to add it to your menu:")
            result = vn.run_sql(query)
            st.dataframe(result)

        elif "merchant_id" in sql:
            query = "WITH merchant_orders AS (SELECT m.merchant_id, COUNT(td.order_id) AS total_orders FROM merchant m LEFT JOIN transaction_data td ON m.merchant_id = td.merchant_id GROUP BY m.merchant_id), my_merchant_order AS (SELECT total_orders FROM merchant_orders WHERE merchant_id = '3e2b6') SELECT COUNT(*) AS total_merchants, SUM(CASE WHEN mo.total_orders <= my.total_orders THEN 1 ELSE 0 END) AS merchants_below_or_equal, 100 - ROUND(SUM(CASE WHEN mo.total_orders <= my.total_orders THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS percentile_rank FROM merchant_orders mo CROSS JOIN my_merchant_order my;"
            result = vn.run_sql(query)
            st.write("### Your merchant is in the top ", result["percentile_rank"][0], "% of all merchants.")


if __name__ == "__main__":
    gui()