import fitz  # PyMuPDF
import PySimpleGUI as sg
import os


file_list_col = [
    [
        sg.Text("PDF Files:"),
        # sg.Push(),
        sg.In(size=(25,1),enable_events=True,key="-FILES-"),
        sg.FilesBrowse(file_types=((("PDF", "*.pdf"),)))
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    
    [
        sg.Text("Output File Destination:"),
        sg.Push(),
        sg.In(size=(25,1),enable_events=True,key="-OUT DESTINATION-"),
        sg.FolderBrowse(),
    ],
    [
        
        sg.Text("Output File Name:"),
        sg.Push(),
        sg.In(size=(25,1),enable_events=True,key="-OUT FILE-"),
        sg.Push(),

        sg.Button("Merge")
    ],
]

layout = [[
    sg.Column(file_list_col)
]]

window = sg.Window("Simple PDF Merger", layout)

# # Usage
# merge_with_pymupdf(["doc1.pdf", "doc2.pdf"], "combined.pdf")
def merge_with_pymupdf(file_list, output_name):
    print(f"Merging Files: {file_list}")
    result_pdf = fitz.open()  # Create a new empty PDF

    for file in file_list:
        with fitz.open(file) as mupdf_file:
            result_pdf.insert_pdf(mupdf_file)

    result_pdf.save(f"{output_name}.pdf")
    result_pdf.close()
    return True


file_list = []

while True:    
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "-FILES-":
        files = values["-FILES-"]
        try:
            file_list = files.split(";")
            
        except:
            file_list = []
        
        print(file_list)    
        
        fnames = [
            os.path.basename(f)
            for f in file_list
            if os.path.isfile(f)
            and f.lower().endswith(".pdf")
        ]
        print(fnames)
        window["-FILE LIST-"].update(fnames)
    elif event == "Merge":
        if merge_with_pymupdf(file_list, os.path.join(
            values["-OUT DESTINATION-"],values["-OUT FILE-"]
        )):
            sg.popup(f"Merge Completed",title="Merge Completed")
            break