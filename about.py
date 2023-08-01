import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


def intro():
    st.markdown("<br>", unsafe_allow_html=True)
    button(username="rririanto", floating=True, width=221)
    st.markdown("""
    # Extract your docs using Unstructured-IO""")
    st.info("""
        Approximately 80% of enterprise data exists in challenging formats such as HTML, PDF, CSV, PNG, PPTX, and more. 
        Unstructured simplifies the process by effortlessly extracting and converting this complex data for compatibility with popular vector databases and LLM frameworks.
        Visit https://unstructured.io/ for additional information.      
    """)
    st.write("This is a demo of using unstructured-io on streamlit. Check out the repository here [![Star](https://img.shields.io/github/stars/rririanto/unstructured-demo-streamlit.svg?logo=github&style=social)](https://github.com/rririanto/unstructured-demo-streamlit) and use it for your own GPT and LLM projects.")
    st.markdown("""
<font size="3"><i>If you find my code helpful, you can support me by buying me a coffee. 🙌</font>&nbsp;&nbsp;[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/rririanto)</i>
<br><font size="3"><i> Follow me to get update my latest post</i></font> &nbsp;&nbsp; [![Follow](https://img.shields.io/twitter/follow/rririanto?style=social)](https://www.twitter.com/rririanto)
""", unsafe_allow_html=True)
    st.markdown("""

""", unsafe_allow_html=True)

    st.markdown("---")
