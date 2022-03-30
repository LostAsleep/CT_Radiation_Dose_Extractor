import tkinter as tk
from tkinter import ttk
from decimal import Decimal
import pyperclip


class CTRadiationDoseExtractor(object):
    def __init__(self, root):
        root.title("CT Radiation Dose Extractor")

        mainframe = ttk.Frame(root, padding="5 5 5 5")
        mainframe.grid(column=0, row=0, sticky=("n w e s"))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.mean_CTDIvol = tk.StringVar()
        self.mean_CTDIvol.set(0)
        self.DLP_total = tk.StringVar()
        self.DLP_total.set(0)

        # 1st row
        ttk.Label(
            mainframe, text="Hier Dosis Information aus JiveX einfügen"
        ).grid(
            column=0,
            row=0,
            columnspan=3,
            sticky=("n w e s"),
        )

        # 2nd row, big text input field
        self.input_field = tk.Text(mainframe, width=45, height=5)
        self.input_field.grid(
            column=0,
            row=1,
            columnspan=3,
            sticky=("n w e s"),
        )

        # 3rd row - CTDI
        ttk.Label(mainframe, text="Mean CTDIvol (mGy):").grid(
            column=0, row=2, sticky="w"
        )
        ttk.Label(
            mainframe,
            width=10,
            textvariable=self.mean_CTDIvol,
            anchor="center",
        ).grid(column=1, row=2)
        ttk.Button(
            mainframe,
            text="Copy",
            command=lambda: pyperclip.copy(self.mean_CTDIvol.get()),
        ).grid(column=2, row=2, sticky=("n w e s"))

        # 4th row - DLP
        ttk.Label(mainframe, text="Dose Length Product (mGycm):").grid(
            column=0, row=3, sticky="w"
        )
        ttk.Label(
            mainframe, width=10, textvariable=self.DLP_total, anchor="center"
        ).grid(column=1, row=3)
        ttk.Button(
            mainframe,
            text="Copy",
            command=lambda: pyperclip.copy(self.DLP_total.get()),
        ).grid(column=2, row=3, sticky=("n w e s"))

        # 5th row - Extract and Clear Button
        ttk.Button(
            mainframe,
            text="Extract",
            command=lambda: self.get_dose_values(
                self.input_field.get("1.0", "end")
            ),
        ).grid(
            column=0,
            row=4,
            columnspan=2,
            sticky=("n w e s"),
        )
        ttk.Button(
            mainframe, text="Clear", command=lambda: self.clear_fields()
        ).grid(column=2, row=4, sticky=("n w e s"))

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
        # and use the Decimal.quantize() method to round the number.
        mean_CTDIvol = Decimal(str(mean_CTDIvol)).quantize(Decimal("1"))
        DLP_total = Decimal(str(DLP_total)).quantize(Decimal("1"))

        self.mean_CTDIvol.set(mean_CTDIvol)
        self.DLP_total.set(DLP_total)

    def clear_fields(self):
        self.mean_CTDIvol.set(0)
        self.DLP_total.set(0)
        self.input_field.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    CTRadiationDoseExtractor(root)
    root.mainloop()
