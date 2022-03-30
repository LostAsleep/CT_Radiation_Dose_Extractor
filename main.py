from tkinter import *
from tkinter import ttk
from decimal import Decimal
import pyperclip


FONT = "Arial"


class CTRadiationDoseExtractor(object):
    def __init__(self, root):
        root.title("CT Radiation Dose Extractor")

        mainframe = ttk.Frame(root, padding="5 5 5 5")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.mean_CTDIvol = 0
        self.DLP_total = 0

        # First row, big text input field
        self.dose_input = StringVar()
        input_field = Text(mainframe, width=45, height=5).grid(
            column=0,
            row=0,
            columnspan=3,
            sticky=(W, N, E, S),
        )

        # Second row - CTDI
        ttk.Label(mainframe, text="Mean CTDIvol (mGy):").grid(
            column=0, row=1, sticky=W
        )
        CTDI_text = ttk.Label(mainframe, textvariable=self.mean_CTDIvol).grid(
            column=1, row=1, sticky=E
        )
        ttk.Button(
            mainframe,
            text="Copy",
            command=lambda: pyperclip.copy(self.mean_CTDIvol),
        ).grid(column=2, row=1, sticky=(W, N, E, S))

        # Third row - DLP
        ttk.Label(mainframe, text="Dose Length Product (mGycm):").grid(
            column=0, row=2, sticky=W
        )
        DLP_text = ttk.Label(mainframe, textvariable=self.DLP_total).grid(
            column=1, row=2, sticky=E
        )
        ttk.Button(
            mainframe,
            text="Copy",
            command=lambda: pyperclip.copy(self.DLP_total),
        ).grid(column=2, row=2, sticky=(W, N, E, S))

        # Fourth row - Extract and Clear Button
        ttk.Button(mainframe, text="Extract").grid(
            column=0,
            row=3,
            columnspan=2,
            sticky=(W, N, E, S),
        )
        ttk.Button(mainframe, text="Clear").grid(
            column=2, row=3, sticky=(W, N, E, S)
        )

    def get_dose_values(self, dose_report):
        """Extracting the DLP total and CTDIvol 
        from a standard JiveX CT dose report.

        Args:
            dose_report (string): A multiline string

        Updates class variables with the extracted mean CTDIvol
        and total dose length product, rounded to two decimal places.
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
                    print(
                        "Could not find DLP total value to convert to float,"
                    )

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

        self.mean_CTDIvol = mean_CTDIvol
        self.DLP_total = DLP_total

    def clear_fields(self):
        pass


if __name__ == "__main__":
    root = Tk()
    CTRadiationDoseExtractor(root)
    root.mainloop()
