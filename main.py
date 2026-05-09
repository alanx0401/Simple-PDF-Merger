import fitz  # PyMuPDF
import PySimpleGUI as sg
import os


file_list_col = [
    [
        sg.Text("PDF Files:"),
        # sg.Push(),
        sg.In(expand_x=True,enable_events=True,key="-FILES-"),
        sg.FilesBrowse(file_types=((("PDF", "*.pdf"),)))
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), expand_x=True, key="-FILE LIST-"
        )
    ],
    
    [
        sg.Text("Output File Destination:", size=(20,1)),
        # sg.Push(),
        sg.In(expand_x=True,enable_events=True,key="-OUT DESTINATION-"),
        sg.FileSaveAs(file_types=((("PDF", "*.pdf"),))),
    ],
    [
        
        sg.Text("Output File Name:", size=(20,1)),
        # sg.Push(),
        sg.In(expand_x=True,enable_events=True,key="-OUT FILE-", disabled=True),
        # sg.Push(),

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

    result_pdf.save(f"{output_name}")
    result_pdf.close()
    return True


file_list = []

while True:    
    event, values = window.read()
    # if event:
    #     print(event)
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
    
    elif event == "-OUT DESTINATION-":
        print(f"Event: -OUT DESTINATION-, Value: {values["-OUT DESTINATION-"]}")
        window["-OUT FILE-"].update(os.path.basename(values["-OUT DESTINATION-"]))
        print(values)

    elif event == "Merge":  
        print(values)
        if len(file_list) == 0:
            sg.popup_error(f"No file selected!",title="Error")
            continue
        elif values["-OUT DESTINATION-"] == "":
            sg.popup_error(f"No output file",title="Error")

        if merge_with_pymupdf(file_list, values["-OUT DESTINATION-"]):
            sg.popup(f"Merge Completed",title="Merge Completed")
            break