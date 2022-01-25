import streamlit as st
import io
import apps
from typing import Callable

from os import walk

apps_path = "./apps"
filenames = list(
    map(lambda x: x.split(".py")[0], next(walk(apps_path), (None, None, []))[2])
)  # [] if no file
filenames.remove("home")
filenames.remove("__init__")
print(filenames)

PAGE_PARAM = "p"
CONTENT = {
    "Home": apps.home.main,
    "Demo": {
        "": apps.home.main,
        # "icheft": apps.icheft.app,
        # "ID": apps.id.app,
    },
}

for i in filenames:
    CONTENT["Demo"][i] = getattr(apps, i).app

# LONG_TO_SHORT = {"課程大綱與說明": "doc", "評分標準": "metrics", "成果展示": "demo"}

MAGE_EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/259/mage_1f9d9.png"

# Set page title and favicon
st.set_page_config(
    page_title="IMAGE CAMP", page_icon=MAGE_EMOJI_URL, initial_sidebar_state="collapsed"
)


def main():
    query_params = st.experimental_get_query_params()
    page_param = query_params[PAGE_PARAM][0] if PAGE_PARAM in query_params else "home"

    page_selected = None

    index = -1
    cur_index = 0

    for page_name, page_function in CONTENT["Demo"].items():
        if cur_index != 0:
            st.session_state[page_name] = page_name == page_param
            if st.session_state[page_name]:
                index = cur_index
        # print(st.session_state[page_name])
        cur_index += 1
    if index == -1:
        st.session_state["home"] = True
        index = 0

    selector = list(CONTENT["Demo"].keys())

    homepage = st.sidebar.button("🏠")

    if homepage:
        index = 0

    st.sidebar.title("成果展示")

    page_selected = st.sidebar.selectbox("選擇你的帳號", selector, index=index)

    # if page_selected in st.session_state and st.session_state[page_selected]:
    #     query_params = st.experimental_get_query_params()
    #     query_params[PAGE_PARAM] = page_selected
    #     print(query_params)

    #     st.experimental_set_query_params(**query_params)

    if page_selected == "" or homepage:
        query_params[PAGE_PARAM] = "home"
    else:
        query_params[PAGE_PARAM] = page_selected
    st.experimental_set_query_params(**query_params)

    if page_selected == "" or homepage:
        page_function = CONTENT["Home"]
    else:
        page_function = CONTENT["Demo"][page_selected]
    if isinstance(page_function, Callable):
        # st.sidebar.success(page_selected)
        page_function()
    # if app_mode == selector[0]:
    #     readme.main()
    # elif app_mode == selector[1]:
    #     # readme_text.empty()
    #     st.sidebar.success("評分標準")
    #     draft.main()
    # elif app_mode == selector[2]:
    #     # readme_text.empty()
    #     st.sidebar.success("Demo 範例參考")
    #     demo.main()


if __name__ == "__main__":
    main()
