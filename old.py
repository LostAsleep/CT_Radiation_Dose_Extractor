import PySimpleGUI as sg
import pyperclip
from decimal import Decimal


def define_basic_sg_layout():
    """The basic PySimpleGUI layout for this program.

    Returns:
        layout (list): The layout of the GUI.
        window (PySimpleGUI.PySimpleGUI.Window): The window widget.
    """
    sg.theme("LightGrey1")
    # fmt: off
    layout = [[sg.Text("Hier Dosis Information aus JiveX einfügen")],
              [sg.Multiline("", size=(40, 5), key="-TEXTFELD-")],
              [sg.InputText("", size=(40, 1), key="-Mean-CTDIvol-"), sg.Text("mGy"), sg.Button("Copy", key="-CTDI-copy-")],
              [sg.InputText("", size=(40, 1), key="-Dose-Length-Product-"), sg.Text("mGycm"), sg.Button("Copy", key="-DLP-copy-")],
              [sg.Button("Extrahieren"), sg.Button("Zwischenablage"), sg.Button("Text löschen")]]
    # fmt: on
    window = sg.Window("CT radiation dose extractor", layout)

    return layout, window


def get_dose_values(dose_report):
    """Extracting the DLP total and CTDIvol from a standard JiveX CT dose report.

    Args:
        dose_report (string): A multiline string from the JiveX dose report.

    Returns:
        float: The extracted mean CTDIvol and total dose length product, rounded to two decimal places.
    """
    DR_lines = dose_report.split("\n")
    num_lines = len(DR_lines)
    DLP_total, CTDIvol_list = 0.0, [0.0]

    for i in range(num_lines - 1):
        # -1 to avoid index errors [i + 1]
        if "CT Dose Length Product Total" in DR_lines[i]:
            temp_list = DR_lines[i + 1].split(" ")
            try:
                DLP_total = float(temp_list[0])
                # Should be only once in the dose report
            except ValueError:
                print("Could not find DLP total value to convert to float,")

        if "Mean CTDIvol" in DR_lines[i]:
            temp_list = DR_lines[i + 1].split(" ")
            try:
                CTDIvol_list.append(float(temp_list[0]))
            except ValueError:
                print(
                    "You either double clicked on 'extract' or no CTDIvol in dose report."
                )
    mean_CTDIvol = sum(CTDIvol_list)

    # Use the Decimal module to get correct decimal representation
    # and use the Decimal.quantize() method to round to two decimal places
    mean_CTDIvol = Decimal(str(mean_CTDIvol)).quantize(Decimal("1.00"))
    DLP_total = Decimal(str(DLP_total)).quantize(Decimal("1.00"))

    return mean_CTDIvol, DLP_total


def main():
    """The main function with the PySimpleGUI loop."""
    result_for_clipboard = ""  # To prevent NameErrors from events

    layout, window = define_basic_sg_layout()
    while True:  # Event Loop for GUI
        event, values = window.read(timeout=50)

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Extrahieren":
            # Extract mean CTDIvol and DLP total
            dose_report = values["-TEXTFELD-"]
            mean_CTDIvol, DLP_total = get_dose_values(dose_report)
            result_for_clipboard = f"{mean_CTDIvol} mGy\n{DLP_total} mGycm\n"
            output_text = f"Mean CTDIvol (mGy): {mean_CTDIvol}\nDose Length Product (mGycm): {DLP_total}"
            window["-TEXTFELD-"].update(output_text)

        if event == "Zwischenablage":
            # Copy result values to clipboard
            pyperclip.copy(result_for_clipboard)

        if event == "Text löschen":
            # Clear the Multiline element
            window["-TEXTFELD-"].update("")
    window.close()


if __name__ == "__main__":
    main()
