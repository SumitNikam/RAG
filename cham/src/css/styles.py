from typing import Literal
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html


FIXED_CONTAINER_CSS = """
    :root {{
        --background-color: #ffffff; /* Default background color */
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) {{
        position: {mode};
        width: inherit;
        background-color: inherit;
        {position}: {margin};
        z-index: 999;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) div[data-testid="stVerticalBlock"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: transparent;
        width: 100%;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) div[data-testid="stVerticalBlock"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) > div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--background-color);
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) div[data-testid="stVerticalBlock"]:has(div.fixed-container-{id}):not(:has(div.not-fixed-container)) > div[data-testid="element-container"] {{
        display: none;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.not-fixed-container):not(:has(div[class^='fixed-container-'])) {{
        display: none;
    }}
""".strip()

FIXED_CONTAINER_JS = """
    const root = parent.document.querySelector('.stApp');
    let lastBackgroundColor = null;
    function updateContainerBackground(currentBackground) {
        parent.document.documentElement.style.setProperty('--background-color', currentBackground);
        ;
    }
    function checkForBackgroundColorChange() {
        const style = window.getComputedStyle(root);
        const currentBackgroundColor = style.backgroundColor;
        if (currentBackgroundColor !== lastBackgroundColor) {
            lastBackgroundColor = currentBackgroundColor; // Update the last known value
            updateContainerBackground(lastBackgroundColor);
        }
    }
    const observerCallback = (mutationsList, observer) => {
        for(let mutation of mutationsList) {
            if (mutation.type === 'attributes' && (mutation.attributeName === 'class' || mutation.attributeName === 'style')) {
                checkForBackgroundColorChange();
            }
        }
    };
    const main = () => {
        checkForBackgroundColorChange();
        const observer = new MutationObserver(observerCallback);
        observer.observe(root, { attributes: true, childList: false, subtree: false });
    }
    // main();
    document.addEventListener("DOMContentLoaded", main);
""".strip()


MARGINS = {
    "top": "3rem",
    "bottom": "10rem",
}


counter = 0


def st_fixed_container(
    *,
    height: int | None = None,
    border: bool | None = None,
    mode: Literal["fixed", "sticky"] = "fixed",
    position: Literal["top", "bottom"] = "top",
    margin: str | None = None,
    transparent: bool = False,
):
    if margin is None:
        margin = MARGINS[position]
    global counter

    fixed_container = st.container()
    non_fixed_container = st.container()

    css = FIXED_CONTAINER_CSS.format(
        mode=mode,
        position=position,
        margin=margin,
        id=counter,
    )
    with fixed_container:
        html(f"<script>{FIXED_CONTAINER_JS}</script>", scrolling=False, height=0)
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='fixed-container-{counter}'></div>",
            unsafe_allow_html=True,
        )
    with non_fixed_container:
        st.markdown(
            "<div class='not-fixed-container'></div>",
            unsafe_allow_html=True,
        )
    counter += 1

    parent_container = fixed_container if transparent else fixed_container.container()

    return parent_container.container(height=height, border=border)


def st_layout_style():
    st.markdown("""
        <style>
        .block-container
        {
            padding-top: 2rem;
            padding-bottom: 2rem;
            margin-top: 4rem;
            padding-right: 1rem;
            padding-left: 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )


def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#9AD8E1",
) -> None:
    st.markdown(
        f"""
        <style>
            div[data-testid="stMetric"],
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 1% 1% 1% 5%;
                margin: 1px 1px 1px 1px;
                border-radius: {border_radius_px}px;
                overflow-wrap: break-word;
                white-space: break-spaces;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def visualizations_style():
    st.markdown('#')
    st.markdown(
        """
        <style>
            div[data-testid='stVerticalBlock']:
            {
                padding-top: 5rem;
                margin-top: 5rem;
            }
        </style>
        """, unsafe_allow_html=True)


def optimization_style_properties(
    df, 
    background_color1='aliceblue', 
    background_color2='lightblue'
    ):
    dataframe_style = df.style.set_properties(
        subset=['Total'],
        **{'background-color': background_color1},
    ).set_properties(
        subset=pd.IndexSlice[['Total'], :],
        **{'background-color': background_color1},
    ).set_properties(
        subset=(df.index[-1], df.columns[-1]),
        **{'background-color': background_color2}
    ).format('{:,.0f}')

    return dataframe_style
