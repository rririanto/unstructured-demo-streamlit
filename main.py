import streamlit as st
import requests
import time
from unstructured.partition.auto import partition
from about import intro

def extract_text(uploaded_file, **kwargs):
    """
    Process extraction data in streamlit server. 
    
    :param uploaded_file: The file uploaded by the user

    :param kwargs: Required settings fields for the extraction

    :return: True if the input is valid, False otherwise
    """
    try:
        elements = partition(file=uploaded_file, **kwargs)
        return "\n\n".join([str(el) for el in elements])
    except Exception as e:
        st.error(f"Failed to extract text: {e}")
        return None

def send_file_to_api(uploaded_file, api_key, **kwargs):
    """
    Send data to unstructed.io API. It will use unstructured.io server to process the extraction.

    :param uploaded_file: The file uploaded by the user

    :param api_key: The API key entered by the user

    :param kwargs: Required fields for submiting to unstructured.io

    :return: True if the input is valid, False otherwise
    """
    url = 'https://api.unstructured.io/general/v0.0.33/general'
    headers = {'accept': 'application/json', 'unstructured-api-key': api_key}

    # Prepare the files parameter for the API request
    # The dict must have a tuple format type
    files = {
        'pdf_infer_table_structure': (None, kwargs['pdf_infer_table_structure']),
        'xml_keep_tags': (None, kwargs['xml_keep_tags']),
        'include_page_breaks': (None, kwargs['include_page_breaks']),
        'encoding': (None, kwargs['encoding']),
        'strategy': (None, kwargs['strategy']),
        'output_format': (None, kwargs['output_format']),
        'files': uploaded_file,
        'gz_uncompressed_content_type': (None, ''),
        'ocr_languages': (None, kwargs['ocr_languages']),
        'coordinates': (None, ''),
        'hi_res_model_name': (None, ''),
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # raise exception if request was unsuccessful
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to send file to API: {e}")  # Display error message on Streamlit
        return None

def boolean_to_string(value):
    return 'true' if value else ''


def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """
    intro()

    if "enable_api" in st.session_state and st.session_state.enable_api:
        st.session_state.advance = True
    
    active_online_api = st.checkbox("Use unstructured.io API?", help="Please note: The file will be uploaded and extracted through the unstructured.io server.", key="enable_api")
    unstructured_api_input = None
    with st.expander("Advance Options", expanded=st.session_state.get("advance", False)):
        if active_online_api:
            unstructured_api_input = st.text_input('Input your API key:', st.secrets["UNSTRUCTURED_API_KEY"], help="You can use mine first, you can also request your own API key here: https://unstructured.io/api-key/#get-api-key")
    
        settings = {
            'strategy': st.radio("Choose the strategy", ('auto', 'hi_res', 'fast', 'ocr_only'), horizontal=True, index=1),
            'pdf_infer_table_structure': boolean_to_string(st.checkbox('pdf_infer_table_structure')),
            'xml_keep_tags': boolean_to_string(st.checkbox('xml_keep_tags')),
            'include_page_breaks': boolean_to_string(st.checkbox('include_page_breaks')),
            'encoding': st.text_input('encoding', 'utf_8'),
            'ocr_languages': st.text_input('ocr_languages', 'en'),
            'output_format': st.radio("Choose the output format", ('text/json', 'text/csv'), horizontal=True, index=0)
        }
        st.info("For more information visit: https://unstructured-io.github.io/unstructured/api.html")


    uploaded_file = st.file_uploader("Upload your document. Accept (HTML, PDF, CSV, PNG, PPTX, and more)")
    if uploaded_file is not None:
        start_time = time.time()
        with st.spinner("Extracting document. This may take a while⏳"):
            try:
                if unstructured_api_input:
                    texts = send_file_to_api(uploaded_file=uploaded_file, api_key=unstructured_api_input, **settings)
                else:
                    texts = extract_text(uploaded_file=uploaded_file, **settings)

                st.write('### Preview:')
                st.text_area('Preview textbox', texts, height=500)
                st.divider()

                with st.expander("See Preview Text"):
                    st.write(texts)
            except Exception as e:
                st.error(f"Failed to process document: {e}")

        execution_time = time.time() - start_time  # Calculate the execution time
        st.write(f"Execution time: {execution_time} seconds")  # Display the execution time

if __name__ == '__main__':
    main()
