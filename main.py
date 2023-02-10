import tkinter as tk
from tkinter import ttk
from decimal import Decimal
import pyperclip


SKULL_ICON = "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"


class CTRadiationDoseExtractor(object):
    def __init__(self, root):
        root.title("CT Radiation Dose Extractor")
        # Set the Window Icon
        root.tk.call(
            "wm", "iconphoto", root._w, tk.PhotoImage(data=SKULL_ICON)
        )

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
            mainframe, text="Paste here the JiveX Dose Report:"
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

        Updates class variables with the rounded
        extracted mean CTDIvol and total dose length product.
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
    root.resizable(False, False)
    CTRadiationDoseExtractor(root)
    root.mainloop()
