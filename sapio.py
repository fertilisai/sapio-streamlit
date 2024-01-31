import os
import copy
import streamlit as st
import openai
import agent as ag
import embeddings as emb

### GLOBAL VARIABLES ###

system = [{"role": "system",
           "content": "You are a helpful assistant. Answer as concisely as possible."}]
key_error = """
            Please, enter a valid OpenAI API key in the settings menu.
            You can get one [here](https://beta.openai.com/).
            """
key_exist = False

tool_list = ["llm-math", "requests_all", "wikipedia", "python_repl"]

### SESSION STATE ###

if 'openai_key' not in st.session_state:
    st.session_state['openai_key'] = ''
    openai.key = ''
    os.environ['OPENAI_API_KEY'] = ''
else:
    openai.key = st.session_state['openai_key']
    os.environ['OPENAI_API_KEY'] = st.session_state['openai_key']

# if 'serpapi_key' not in st.session_state:
#     st.session_state['serpapi_key'] = ''

ss = {'chat-messages': copy.copy(system),
      'qa-messages': copy.copy(system),
      'temp-messages': copy.copy(system),
      'draw-image': '',
      'agent-answer': '',
      'chat_model': 'gpt-3.5-turbo',
      'draw_model': 'DALL-E',
      'emb_model': 'text-embedding-ada-002',
      'size': '1024x1024',
      'max_length': 256,
      'temperature': 0.7,
      'presence': 0.0,
      'ddg': True,
      "llm-math": True,
      "requests_all": False,
      "wikipedia": False,
      "python_repl": False,
      'stableDiffusion': False
      }


for s in ss.keys():
    if s not in st.session_state:
        st.session_state[s] = ss[s]


def test_key(key):
    if key == '' or key[0:3] != 'sk-' or len(key) != 51:
        error_msg.error(key_error)
        return False
    else:
        openai.api_key = key
        st.session_state['openai_key'] = key
        return True


def chat_request(messages):
    if key_exist:
        chat_response = openai.ChatCompletion.create(
            model=st.session_state['chat_model'],
            messages=messages,
            temperature=st.session_state['temperature'],
            max_tokens=st.session_state['max_length'],
            presence_penalty=st.session_state['presence'],
        )
        answer = chat_response["choices"][0]["message"]["content"]
        st.session_state['chat-messages'].append(
            {"role": "assistant", "content": answer})
        chat_response = False
        write_to_chat_resp()
    else:
        error_msg.error(key_error)


def draw_request(description):
    if key_exist:
        image_response = openai.Image.create(
            prompt=description,
            n=1,
            size=st.session_state['size'],
            response_format="url",
        )
        image_url = image_response["data"][0]["url"]
        st.session_state['draw-image'] = image_url
        draw_to_draw_resp(image_url)
    else:
        error_msg.error(key_error)


def agent_request(ask, t_list):
    if key_exist:
        answer = ag.ask_agent(ask, t_list, st.session_state['ddg'],
                              st.session_state['stableDiffusion'])
        st.session_state['agent-answer'] = answer
        write_to_agent_resp(answer)
    else:
        error_msg.error(key_error)


def qa_request(temp_messages):
    if key_exist:
        qa_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=temp_messages,
            temperature=0,
            max_tokens=256,
        )
        qa_answer = qa_response["choices"][0]["message"]["content"]
        st.session_state['qa-messages'].append(
            {"role": "assistant", "content": qa_answer})
        st.session_state['temp-messages'].append(
            {"role": "assistant", "content": qa_answer})
        write_to_qa_resp()
    else:
        error_msg.error(key_error)


def write_to_chat_resp():
    with chat_resp.container():
        for m in st.session_state['chat-messages'][::-1]:
            if m["role"] != "system":
                st.write(m["role"].upper()+":")
                st.write(m["content"])
                st.divider()
            else:
                pass


def draw_to_draw_resp(image_url):
    with draw_resp.container():
        st.image(image_url, use_column_width=True)


def write_to_agent_resp(answer):
    with agent_resp.container():
        st.write("QUESTION:")
        st.write(answer['input'])
        st.write("ANSWER:")
        st.write(answer['output'])
        st.write("REASON:")
        st.json(answer['intermediate_steps'], expanded=True)


def write_to_qa_resp():
    with qa_resp.container():
        for m in st.session_state['qa-messages'][::-1]:
            if m["role"] != "system":
                st.write(m["role"].upper()+":")
                st.write(m["content"])
                st.divider()
            else:
                pass


def chat_input():
    if key_exist:
        st.session_state['chat-messages'].append(
            {"role": "user", "content": question})
        chat_request(st.session_state['chat-messages'])
        st.session_state['question'] = ''
    else:
        error_msg.error(key_error)


def draw_input():
    draw_request(description)
    st.session_state['description'] = ''


def make_tool_list(tool_list):
    t_list = []
    for t in tool_list:
        if st.session_state[t] == True:
            t_list.append(t)
    return t_list


def agent_input():
    t_list = make_tool_list(tool_list)
    agent_request(ask_agent, t_list)
    st.session_state['ask_agent'] = ''


def qa_input():
    qa = st.session_state['qa']
    if key_exist:
        context = emb.get_context_from_emb(db, qa)
        query_and_context = f'Answer the following QUESTION base on this CONTEXT:{context} \n\n QUESTION:{qa} \n\n Limit and yourself to the context.'
        st.session_state['temp-messages'].append(
            {"role": "user", "content": query_and_context})
        st.session_state['qa-messages'].append(
            {"role": "user", "content": qa})
        qa_request(st.session_state['temp-messages'])
        st.session_state['qa'] = ''
    else:
        error_msg.error(key_error)


def clear_chat():
    st.session_state['question'] = ''
    st.session_state['chat-messages'] = copy.copy(system)
    chat_resp.empty()


def clear_draw():
    st.session_state['description'] = ''
    st.session_state['draw-image'] = ''
    draw_resp.empty()


def clear_agent():
    st.session_state['ask_agent'] = ''
    st.session_state['agent-answer'] = ''
    agent_resp.empty()


def clear_qa():
    st.session_state['qa'] = ''
    st.session_state['qa-messages'] = copy.copy(system)
    st.session_state['temp-messages'] = copy.copy(system)
    qa_resp.empty()


def reset():
    for s in ss.keys():
        st.session_state[s] = ss[s]


### PAGE LAYOUT ###
st.set_page_config(
    page_title="Sapio - A smarter ChatGPT",
    page_icon="🧠"
)

# st.header("Sapio")
# st.write("A smarter ChatGPT")

error_msg = st.empty()
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "Draw", "Agent", "Q&A", "Settings"])

with tab1: # Chat

    with st.expander("Chat Settings"):
        col1, col2 = st.columns((1, 1))

        with col1:
            st.selectbox('Chat Model',
                         ("gpt-3.5-turbo", "gpt-4", "gpt-4-32k"),
                         key="chat_model"
                         )
            st.slider('Max length', 0, 2048, key="max_length")
        with col2:
            st.slider('Temperature', 0.0, 1.0,
                      step=0.01, key="temperature")
            st.slider('Presence penalty', -2.0, 2.0,
                      step=0.01, key="presence")

    c1, c2 = st.columns((6, 1))
    question = c1.text_area(
        label="Question",
        height=90,
        placeholder='Ask something...',
        label_visibility='hidden',
        key='question',
    )

    with c2:
        st.markdown('##')
        send = st.button('Send', key='send', on_click=chat_input)
        clear = st.button('Clear', key='clear1', on_click=clear_chat)

    st.divider()
    chat_resp = st.empty()

    if st.session_state['chat-messages'] != system:
        write_to_chat_resp()


with tab2: # Draw

    with st.expander("Draw Settings"):
        col1, col2 = st.columns((1, 1))

        with col1:
            st.selectbox('Draw Model',
                         ("DALL-E", "Stable Diffusion"),
                         key="draw_model"
                         )
        with col2:
            st.selectbox('Image Size',
                         ("1024x1024", "512x512", "256x256"),
                         key="size"
                         )

    c1, c2 = st.columns((6, 1))
    description = c1.text_area(
        label='Description',
        height=90,
        placeholder='Describe something...',
        label_visibility='hidden',
        key='description'
    )
    with c2:
        st.markdown('##')
        draw = st.button('Draw', key='draw', on_click=draw_input)
        clear2 = st.button('Clear', key='clear2', on_click=clear_draw)

    st.divider()
    draw_resp = st.empty()

    if st.session_state['draw-image'] != '':
        draw_to_draw_resp(st.session_state['draw-image'])


with tab3: # Agent

    with st.expander("Agent Tools"):
        col1, col2, col3 = st.columns((1, 1, 1))

        with col1:
            st.checkbox("Web Search", key="ddg", value=True)
            st.checkbox("Calculator", key="llm-math", value=True)

        with col2:
            st.checkbox("Wikipedia", key="wikipedia")
            st.checkbox("Requests", key="requests_all")

        with col3:
            st.checkbox("Python REPL", key="python_repl")
            # st.checkbox("Stable Diffusion", key="stableDiffusion")

    c1, c2 = st.columns((6, 1))
    ask_agent = c1.text_area(
        label='Ask a Agent',
        height=90,
        placeholder='Ask something...',
        label_visibility='hidden',
        key='ask_agent'
    )
    with c2:
        st.markdown('##')
        ask = st.button('Ask', key='ask', on_click=agent_input)
        clear2 = st.button('Clear', key='clear3', on_click=clear_agent)

    st.divider()
    agent_resp = st.empty()

    if st.session_state['agent-answer'] != '':
        write_to_agent_resp(st.session_state['agent-answer'])


with tab4: # Q&A
    
    uploaded_files = st.file_uploader("Choose file (pdf, txt)", 
                                      accept_multiple_files=False, 
                                      type=["pdf", "txt"],)
                                      #type=["pdf", "txt", "docx"],)
    if uploaded_files is not None:
        with st.spinner("Indexing document... ⏳"):
            docs = emb.load_docs(uploaded_files)
            splits = emb.split_docs(docs, 200, 0)
            db = emb.get_emb(splits)

    c1, c2 = st.columns((6, 1))
    qa = c1.text_area(
        label='Question & Answer',
        height=90,
        placeholder='Ask something related to the document...',
        label_visibility='hidden',
        key='qa'
    )
    with c2:
        st.markdown('##')
        ask_doc = st.button('Send', key='ask_doc', on_click=qa_input)
        clear4 = st.button('Clear', key='clear4', on_click=clear_qa)

    st.divider()
    qa_resp = st.empty()

    if st.session_state['qa-messages'] != system:
        write_to_qa_resp()


with tab5: # Settings

    openai_key = st.text_input(label='OpenAI API Key',
                               placeholder='sk-...',
                               type='password',
                               value=st.session_state['openai_key']
                               )
    if openai_key:
        key_exist = test_key(openai_key)

    # serp_key = st.text_input(label='Serp API Key',
    #                          placeholder='sk-...',
    #                          type='password',
    #                          value=st.session_state['serpapi_key']
    #                          )
    
    st.divider()
    st.button(label="Reset all settings", on_click=reset)

# test key when UI is loaded
key_exist = test_key(st.session_state['openai_key'])
