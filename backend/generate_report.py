import os
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class PDFReport:
    def __init__(self, title="CSV Report"):
        self.pdf = FPDF()
        self.title = title
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.add_title()

    def add_title(self):
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(200, 10, txt=self.title, ln=True, align='C')
        self.pdf.set_font("Arial", size=12)
        self.pdf.ln(10)

    def add_text(self, text):
        self.pdf.multi_cell(0, 10, txt=text)
        self.pdf.ln()

    def add_image(self, image_path, width=180):
        if os.path.exists(image_path):
            self.pdf.image(image_path, w=width)
            self.pdf.ln(10)
        else:
            self.add_text(f"[Missing image: {image_path}]")

    def save(self, filename="report.pdf"):
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, filename)
        self.pdf.output(path)
        return path

# --------------------------------------------------------
# 📊 Utility to Generate and Save Charts from CSV Data
# --------------------------------------------------------

def generate_charts_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    chart_dir = os.path.join(os.path.dirname(__file__), "reports", "charts")
    os.makedirs(chart_dir, exist_ok=True)

    image_paths = []

    # 1. Product-wise Sales (Bar Chart)
    if "Product" in df.columns and "Sales" in df.columns:
        product_sales = df.groupby("Product")["Sales"].sum()
        plt.figure(figsize=(6, 4))
        product_sales.plot(kind="bar", color="skyblue")
        plt.title("Product-wise Sales")
        plt.ylabel("Sales")
        bar_path = os.path.join(chart_dir, "bar_product_sales.png")
        plt.tight_layout()
        plt.savefig(bar_path)
        image_paths.append(bar_path)
        plt.close()

    # 2. Monthly Sales (Pie Chart)
    if "Month" in df.columns and "Sales" in df.columns:
        monthly_sales = df.groupby("Month")["Sales"].sum()
        plt.figure(figsize=(5, 5))
        monthly_sales.plot(kind="pie", autopct="%1.1f%%", startangle=90)
        plt.title("Monthly Sales Share")
        pie_path = os.path.join(chart_dir, "pie_monthly_sales.png")
        plt.tight_layout()
        plt.savefig(pie_path)
        image_paths.append(pie_path)
        plt.close()

    return image_paths

# --------------------------------------------------------
# 🚀 Full Flow: CSV → Charts → PDF Report
# --------------------------------------------------------

def generate_pdf_report_from_csv(csv_path, report_title="AutoBiz Report"):
    df = pd.read_csv(csv_path)

    report = PDFReport(title=report_title)
    report.add_text(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.add_text(f"Total rows in data: {len(df)}")

    # Basic stats summary
    if "Sales" in df.columns:
        total_sales = df["Sales"].sum()
        avg_sales = df["Sales"].mean()
        report.add_text(f"\nTotal Sales: ₹{total_sales:,.2f}")
        report.add_text(f"Average Sales per record: ₹{avg_sales:,.2f}")

    # Add charts
    image_paths = generate_charts_from_csv(csv_path)
    for img_path in image_paths:
        report.add_image(img_path)

    pdf_path = report.save()
    print(f"✅ PDF generated at: {pdf_path}")
    return pdf_path
