import tkinter as tk
from tkinter import ttk

def visualize_data(data):
    root = tk.Tk()
    root.title("Gene Expression Data")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    columns = [
        "patient_id", "bcr_patient_barcode", "cancer_cohort",
        "C6orf150", "CCL5", "CXCL10", "TMEM173", "CXCL9", "CXCL11",
        "NFKB1", "IKBKE", "IRF3", "TREX1", "ATM", "IL6", "IL8",
        "DSS", "OS", "clinical_stage"
    ]

    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=v_scrollbar.set)

    h_scrollbar = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=h_scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)

    for record in data:
        row = [
            record["patient_id"],
            record["bcr_patient_barcode"],
            record["cancer_cohort"],
            record["gene_expressions"]["C6orf150"],
            record["gene_expressions"]["CCL5"],
            record["gene_expressions"]["CXCL10"],
            record["gene_expressions"]["TMEM173"],
            record["gene_expressions"]["CXCL9"],
            record["gene_expressions"]["CXCL11"],
            record["gene_expressions"]["NFKB1"],
            record["gene_expressions"]["IKBKE"],
            record["gene_expressions"]["IRF3"],
            record["gene_expressions"]["TREX1"],
            record["gene_expressions"]["ATM"],
            record["gene_expressions"]["IL6"],
            record["gene_expressions"]["IL8"],
            record["DSS"],
            record["OS"],
            record["clinical_stage"]
        ]
        tree.insert("", tk.END, values=row)

    root.mainloop()
