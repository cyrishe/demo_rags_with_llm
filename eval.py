import sys
from trulens_eval import Tru
from rag_with_azure import get_query_engine

question_file = sys.argv[1]
question_list = []
with open(question_file,"r") as fp:
    for line in fp.readlines():
        line = line.rstrip("\n")
        question_list.append(line)
        break

tru=Tru()

tru.reset_database()
from utils import get_prebuilt_trulens_recorder

query_engine  = get_query_engine(["./docs/1.txt"])
tru_recorder = get_prebuilt_trulens_recorder(query_engine,app_id='direct indexing')

with tru_recorder as recording:
    for question in question_list:
        response = query_engine.query(question)

records, feedback = tru.get_records_and_feedback(app_ids=[])

records.head()

tru.run_dashboard()

