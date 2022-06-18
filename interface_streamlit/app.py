from base64 import b64decode
from math import ceil
from os import environ
from time import time

import requests
import streamlit as st

URL = environ.get("DALLE_URL")

# disable hamburger menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def check_if_valid_backend(url):
    try:
        resp = requests.get(url, timeout=3)
        return resp.status_code == 200
    except requests.exceptions.Timeout:
        return False


def call_dalle(url, text, num_images=1):
    data = {"text": text, "num_images": num_images}
    resp = requests.post(url + "/dalle", json=data)
    if resp.status_code == 200:
        return resp


def create_images(text, num_images):
    valid = check_if_valid_backend(URL)
    if not valid:
        return "Backend service is not running"
    else:
        resp = call_dalle(URL, text, num_images)
        if resp is not None:
            return [b64decode(image) for image in resp.json()]
        return "Failed to create images..."


def main():
    st.title("DALL·E")
    col1, col2 = st.columns(2)
    with col1:
        text = st.text_input("What should I create?")
    with col2:
        num_images = st.number_input("How many images?", value=4, min_value=1, max_value=10)

    ok = st.button("Create Images")

    if ok and text:
        with st.spinner("Creating images..."):
            start = time()
            images = create_images(text, num_images)
            generation_time_len = time() - start

        if not isinstance(images, list):
            st.write(images)
            return

        split_idx = ceil(len(images) / 2)
        col1, col2 = st.columns(2)
        with col1:
            for image in images[:split_idx]:
                st.image(image)
        with col2:
            for image in images[split_idx:]:
                st.image(image)

        st.text(f"Generated in {round(generation_time_len, 1)} secs")


main()
