import streamlit as st
import openai


system = [{"role": "system",
           "content": "You are a helpful assistant. Answer as concisely as possible."}]
key_error = """
            Please, enter a valid OpenAI API key in the settings menu. 
            You can get one [here](https://beta.openai.com/).
            """
key_exist = False

### SESSION STATE ###
if 'openai_key' not in st.session_state:
    st.session_state['openai_key'] = ''
    openai.key = ''
else:
    openai.key = st.session_state['openai_key']

if 'messages' not in st.session_state:
    st.session_state['messages'] = system

if 'image' not in st.session_state:
    st.session_state['image'] = ''

if 'model' not in st.session_state:
    st.session_state['model'] = 'gpt-3.5-turbo'

if 'size' not in st.session_state:
    st.session_state['size'] = '1024x1024'

if 'max_length' not in st.session_state:
    st.session_state['max_length'] = 256

if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.7

if 'presence' not in st.session_state:
    st.session_state['presence'] = 0.0


def test_key(key):
    if key == '' or key[0:3] != 'sk-' or len(key) != 51:
        error_msg.error(key_error)
        return False
    else:
        openai.api_key = key
        return True


def chat_request(messages):
    if key_exist:
        chat_response = openai.ChatCompletion.create(
            model=st.session_state['model'],
            messages=messages,
            temperature=st.session_state['temperature'],
            max_tokens=st.session_state['max_length'],
            presence_penalty=st.session_state['presence'],
        )
        answer = chat_response["choices"][0]["message"]["content"]
        st.session_state['messages'].append(
            {"role": "assistant", "content": answer})
        chat_response = False
        write_to_chat()
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
        st.session_state['image'] = image_url
        draw_to_canva(image_url)
    else:
        error_msg.error(key_error)


def write_to_chat():
    with chat.container():
        for m in st.session_state['messages'][::-1]:
            if m["role"] != "system":
                st.write(m["role"].upper()+":")
                st.write(m["content"])
                st.divider()
            else:
                pass


def draw_to_canva(image_url):
    with canva.container():
        st.image(image_url, use_column_width=True)


def chat_input():
    if key_exist:
        st.session_state['messages'].append(
            {"role": "user", "content": question})
        chat_request(st.session_state['messages'])
        st.session_state['question'] = ''
    else:
        error_msg.error(key_error)


def draw_input():
    draw_request(description)
    st.session_state['description'] = ''


def clear_chat():
    st.session_state['question'] = ''
    st.session_state['messages'] = system
    chat.empty()


def clear_draw():
    st.session_state['description'] = ''
    st.session_state['image'] = ''
    canva.empty()


def reset():
    st.session_state['model'] = 'gpt-3.5-turbo'
    st.session_state['size'] = '1024x1024'
    st.session_state['max_length'] = 256
    st.session_state['temperature'] = 0.7
    st.session_state['presence'] = 0.0


### PAGE LAYOUT ###
st.set_page_config(
    page_title="Sapio - A smarter ChatGPT",
    page_icon="🧠"
)

st.header("Sapio")
st.write("A smarter ChatGPT")

error_msg = st.empty()
tab1, tab2, tab3 = st.tabs(["Chat", "Draw", "Settings"])

with tab1:
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
    chat = st.empty()

    if st.session_state['image'] != system:
        write_to_chat()


with tab2:
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
    canva = st.empty()

    if st.session_state['image'] != '':
        draw_to_canva(st.session_state['image'])


with tab3:
    c1, c2 = st.columns(2)

    with c1:

        openai_key = st.text_input(label='OpenAI API Key',
                                   placeholder='sk-...',
                                   type='password',
                                   key='openai_key'
                                   )
        if openai_key:
            key_exist = test_key(openai_key)

        st.selectbox('Chat Model',
                     ("gpt-3.5-turbo", "gpt-4", "gpt-4-32k"),
                     key="model"
                     )

        st.radio("Image Size",
                 options=["1024x1024", "512x512", "256x256"],
                 key="size"
                 )

    with c2:
        st.slider('Max length', 0, 2048, key="max_length")
        st.slider('Temperature', 0.0, 1.0, step=0.01, key="temperature")
        st.slider('Presence penalty', -2.0, 2.0, step=0.01, key="presence")

    st.divider()
    st.button(label="Reset", on_click=reset)

# test key when UI is loaded
key_exist = test_key(st.session_state['openai_key'])
