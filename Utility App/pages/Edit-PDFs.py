import streamlit as st
import PyPDF2
import pikepdf
from pdf2docx import Converter
import fitz
import img2pdf
from streamlit_pdf_viewer import pdf_viewer
from gtts import gTTS 

# Initialize state for merge
if "merge_button_clicked" not in st.session_state:
    st.session_state.merge_button_clicked = False
def callback_merge():
    st.session_state.clear()
    # Button was clicked
    st.session_state.merge_button_clicked = True

# Initialize state for delete
if "page_delete_button_clicked" not in st.session_state:
    st.session_state.page_delete_button_clicked = False
def callback_delete():
    st.session_state.clear()
    # Button was clicked
    st.session_state.page_delete_button_clicked = True

# Initialize state for docx
if "docx_button_clicked" not in st.session_state:
    st.session_state.docx_button_clicked = False
def callback_docx():
    st.session_state.clear()
    # Button was clicked
    st.session_state.docx_button_clicked = True

# Initialize state for image
if "img_button_clicked" not in st.session_state:
    st.session_state.img_button_clicked = False
def callback_img():
    st.session_state.clear()
    # Button was clicked
    st.session_state.img_button_clicked = True

# Initialize state for pdf to image
if "img_to_pdf_button_clicked" not in st.session_state:
    st.session_state.img_to_pdf_button_clicked = False
def callback_img_to_pdf():
    st.session_state.clear()
    # Button was clicked
    st.session_state.img_to_pdf_button_clicked = True

# Initialize state for pdf Read
if "read_button_clicked" not in st.session_state:
    st.session_state.read_button_clicked = False
def callback_read():
    st.session_state.clear()
    # Button was clicked
    st.session_state.read_button_clicked = True


def mergePDFs(pdfs):
    merger = PyPDF2.PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write('NewPDF.pdf')
    # webbrowser.open_new_tab('NewPDF.pdf')
    st.markdown('<h3>The Merged PDF</h3>', unsafe_allow_html=True)
    pdf_viewer('NewPDF.pdf')
    with open('NewPDF.pdf', 'rb') as f:
        pdfBytes = f.read()

    st.download_button(label='Download New PDF', data=pdfBytes,
                       file_name='newPDF.pdf', mime='application/pdf')

# st.title('You can edit your pdf here')
st.sidebar.title("PDF Utility Functions")

if st.sidebar.button("PDF Merger", use_container_width=True, on_click=callback_merge) or st.session_state.merge_button_clicked:
    uploadedFiles = st.file_uploader(
        'Choose PDF files: ', accept_multiple_files=True, type='pdf')
    if uploadedFiles:
        pdfs = [pdf for pdf in uploadedFiles]
        mergePDFs(pdfs)

if st.sidebar.button('Delete a Page in Pdf', use_container_width=True, on_click=callback_delete) or st.session_state.page_delete_button_clicked:
    pdfFile = st.file_uploader('Choose PDF file: ', type='pdf')
    if pdfFile:
        pdf = pikepdf.Pdf.open(pdfFile)
        pg_no = st.text_input("Enter the page number you want to delete: ")
        if pg_no:
            del pdf.pages[int(pg_no)-1]
            pdf.save('NewPDF.pdf')
            st.markdown('<h3>The Page is deleted</h3>', unsafe_allow_html=True)
            # pdf_viewer('NewPDF.pdf')
            with open('NewPDF.pdf', 'rb') as f:
                pdfBytes = f.read()

            st.download_button(label='Download New PDF', data=pdfBytes,
                            file_name='newPDF.pdf', mime='application/pdf')
            
if st.sidebar.button('Convert PDF to DOCx', use_container_width=True, on_click=callback_docx) or st.session_state.docx_button_clicked:
    pdfFile = st.file_uploader('Choose PDF file: ', type='pdf')
    if pdfFile:
        st.write('Converting to DOCx...')
        try:
            pdf = pdfFile.getvalue()
            convert = Converter(stream=pdf)
            convert.convert('NewDocx.docx')
            convert.close()
            st.success("Converted to DOCx")
            with open('NewDocx.docx', 'rb') as f:
                docxByte = f.read()
            
            st.download_button(label='Download New DOCx file', data=docxByte, file_name='NewDocx.docx', mime='application/docx')
        except:
            st.error("Can't convert to DOCx")

if st.sidebar.button('Convert PDF to Images', use_container_width=True, on_click=callback_img) or st.session_state.img_button_clicked:
    pdfFile = st.file_uploader('Choose PDF file: ', type='pdf')
    if pdfFile:
        pdf = pdfFile.getvalue()
        st.write('Converting to Images...')
        try:
            doc = fitz.open(stream=pdf)
            zoom = 4
            mat = fitz.Matrix(zoom, zoom)
            count = 0
            for p in doc:
                count += 1
            for i in range(count):
                val = f"image_{i+1}.png"
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                pix.save(val)
                st.image(f"image_{i+1}.png")
                with open(val, 'rb') as f:
                    file = f.read()
                st.download_button(label='Download Image', data=file, file_name=val, mime='application/png')
            doc.close()
        except:
            st.error("Can't Convert PDF to Images...")

if st.sidebar.button('Convert Images to PDF', use_container_width=True, on_click=callback_img_to_pdf) or st.session_state.img_to_pdf_button_clicked:
    imgFiles = st.file_uploader('Choose image files: ', accept_multiple_files=True)
    if imgFiles:
        img = [i for i in imgFiles]
        try:
            st.write('Converting Images to pdf...')
            pdf_data = img2pdf.convert(img)
            with open("output.pdf", "wb") as file:
                file.write(pdf_data)
            
            with open('output.pdf', 'rb') as f:
                bytesFile = f.read()
            
            st.markdown('<h3>The Merged PDF</h3>', unsafe_allow_html=True)
            pdf_viewer('output.pdf')

            st.download_button(label='Download PDF', data=bytesFile, file_name='New.pdf', mime='application/pdf')
        except:
            st.error("Can't convert images to PDF...")


if st.sidebar.button('Read PDF', use_container_width=True, on_click=callback_read) or st.session_state.read_button_clicked:
    pdfFile = st.file_uploader('Choose PDF file:', type='pdf')
    if pdfFile:
        # pdf_Bytes = pdfFile.getvalue()
        pdf_document = PyPDF2.PdfReader(pdfFile)
        text_content = ""
        for page_num in range(len(pdf_document.pages)):
            page = pdf_document.pages[page_num]
            text_content += page.extract_text()
        
        st.write('Converting Text to Audio...')

        # st.write(text_content)

        myobj = gTTS(text=text_content, lang='en', slow=False)
        myobj.save('output.mp3')
        
        st.markdown('<h3>The Converted Audio from PDF</h3>', unsafe_allow_html=True)

        with open('output.mp3', 'rb') as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.download_button(label='Download Audio', data=audio_bytes, mime='application/mp3', file_name='audio.mp3')

