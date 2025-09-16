import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from analyze_csv import analyze_csv
from generate_report import PDFReport, generate_charts_from_csv

# 🔧 Init FastAPI
app = FastAPI()

# 🌐 Allow CORS for frontend (http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📍 Base directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🤖 DeepSeek Agent Setup
llm = Ollama(model="deepseek-coder:33b")

prompt_template = PromptTemplate(
    input_variables=["message"],
    template="Answer this prompt as a coding expert:\n\n{message}"
)

chain = LLMChain(llm=llm, prompt=prompt_template)

# ---------------------- 🔍 AGENT CHAT ----------------------

class Prompt(BaseModel):
    message: str

@app.post("/agent/")
async def run_agent(prompt: Prompt):
    """
    🤖 Accepts prompt and returns DeepSeek-generated response.
    """
    response = chain.run(message=prompt.message)
    return {"reply": response}

# ---------------------- 📊 CSV INSIGHT ONLY ----------------------

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    """
    📂 Uploads a CSV file, analyzes and returns insights
    """
    save_path = os.path.join(BASE_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    insights = analyze_csv(save_path)
    return {"insights": insights}

# ---------------------- 📄 PDF GENERATOR ----------------------

@app.post("/report/")
async def generate_pdf(file: UploadFile = File(...)):
    print("📥 Received file:", file.filename)
    
    """
    📄 Uploads CSV, generates insights + graphs, compiles into a PDF report
    """
    # Step 1: Save uploaded CSV
    save_path = os.path.join(BASE_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Step 2: Analyze CSV
    insights = analyze_csv(save_path)
    insight_text = "\n".join(insights)

    # Step 3: Generate LLM-based business summary
    prompt = f"Summarize these CSV insights in a professional business report:\n{insight_text}"
    final_summary = chain.run(message=prompt).replace("₹", "Rs.")

    # Step 4: Generate visual charts
    chart_paths = generate_charts_from_csv(save_path)

    # Step 5: Create PDF with summary + charts
    pdf = PDFReport(title="AutoBiz.AI | CSV Business Insights")
    pdf.add_text(final_summary)
    for chart in chart_paths:
        pdf.add_image(chart)
    pdf_path = pdf.save()

    # Convert Windows path to forward slashes for frontend
    return {"pdf_path": pdf_path.replace("\\", "/")}
