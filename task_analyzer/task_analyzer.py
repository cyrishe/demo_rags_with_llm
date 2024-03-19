from llm_engine.azure_openai import get_llm_model
from llama_index.core.llms import ChatMessage


def build_break_down_msg(question):
    messages = [
            ChatMessage(
            role="system", content="你是一个非常精通经济学的学者，你很懂市场分析和研究，对市场规模、公司研究、制造端、消费端、国际形势和国内政策等的概念掌握的很深，接下来你需要根据你的知识，去拆解一个复杂的问题，给出解决这个问题的核心步骤和关键信息,拆解步骤尽量在3到5步，不要太细"
            ),
            ChatMessage(role="user", content="给你这个问题'%s',你会将其拆分为几个步骤？请给出你的答案,每个步骤请用'*'开头" % question),
            ]
    return  messages

def build_final_msg(context , question):
    messages = [
            ChatMessage(
            role="system", content="你是一个非常精通经济学的学者，你很懂市场分析和研究，对市场规模、公司研究、制造端、消费端、国际形势和国内政策等的概念掌握的很深，接下来请根据提供给你的核心信息，麻烦你用你的知识将其整理并用选择合适的信息来回答问题"
            ),
            ChatMessage(role="user", content="上下文'%s'.\n请参考上述的信息回答'%s',给出你的答案" % (context, question)),
            ]
    return  messages



llm = get_llm_model()


def task_analyzer(question):
    msg = build_break_down_msg(question)
    response = llm.chat(msg)
    return response.message.content


def final_answer(question,context):
    msg = build_final_msg(context,question)
    response = llm.chat(msg)
    return response.message.content



if __name__ == '__main__':
    r = task_analyzer('印尼的医疗器械市场怎么样？是否适合进入？为什么？')
    print(type(r))
    print(r)
