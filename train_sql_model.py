import vanna
from vanna.remote import VannaDefault
from utils import Utils
def train():
    api_key = "2f8e680c8f324b95885327d83d1fe9c4"# Your API key from https://vanna.ai/account/profile 

    vanna_model_name = "grab-mex-ai" # Your model name from https://vanna.ai/account/profile 
    vn = VannaDefault(model=vanna_model_name, api_key=api_key)

    vn.connect_to_mssql(odbc_conn_str='DRIVER={ODBC Driver 17 for SQL Server};SERVER=LOCALHOST;DATABASE=GrabFoodDB;Trusted_Connection=Yes;TrustServerCertificate=Yes;') # You can use the ODBC connection string here

    # The information schema query may need some tweaking depending on your database. This is a good starting point.
    # df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    # plan = vn.get_training_plan_generic(df_information_schema)
    # print(plan)

    # If you like the plan, then uncomment this and run it to train
    # vn.train(plan=plan)
    # vn.train(sql="SELECT TOP 1 keyword FROM keywords ORDER BY [view] DESC;")
    # training_data = vn.get_training_data()
    # print(training_data)
    
    # answer = vn.ask(question="What are the longest delivery_time?", visualize=False, print_results=False, allow_llm_to_see_data=True)
    # print("Generated SQL:\n", answer[0])
    # print("Answer:\n", answer[1])

    from vanna.flask import VannaFlaskApp
    app = VannaFlaskApp(vn)
    app.run()

if __name__ == "__main__":
    train()



