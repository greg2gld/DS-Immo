"""
code de la page

"""

# import streamlit as st
from tools import *

def affiche1():
    


    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'

def affiche():
    data = {
        "Nom": ["Google", "OpenAI"],
        "Lien": [
            "[Visiter](https://google.com)",
            "[Visiter](https://openai.com)"
        ]
    }

    df = pd.DataFrame(data)

    # Afficher le tableau en Markdown (statique mais propre)
    st.write(df.to_markdown(index=False), unsafe_allow_html=False)
    # print(df.to_markdown(index=False))
