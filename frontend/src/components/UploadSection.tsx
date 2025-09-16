"use client";

import { useState } from "react";
import Papa from "papaparse";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { Button } from "@/components/ui/button";

export default function UploadSection() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string[][]>([]);
  const [pdfLink, setPdfLink] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);

    Papa.parse(selected, {
      complete: (result) => {
        console.log("CSV Preview:", result.data); // ✅ Debug
        setPreview(result.data.slice(0, 5)); // Show first 5 rows
      },
    });
  }; // 🛠️ This closing bracket was missing earlier

  const uploadFile = async () => {
    if (!file) return toast.error("Please select a CSV file first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      toast.loading("Uploading and generating report...");

      const response = await axios.post("http://localhost:8000/report/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      toast.dismiss();
      toast.success("Report generated 🎉");

      setPdfLink(`http://localhost:8000/${response.data.pdf_path}`);
    } catch (err) {
      toast.dismiss();
      toast.error("Upload failed ❌");
      console.error(err);
    }
  };

  return (
    <div className="p-6 bg-white/5 rounded-xl shadow-md text-white backdrop-blur-md mt-10 w-full max-w-4xl mx-auto">
      <Toaster />
      <h2 className="text-2xl font-bold mb-4">📤 Upload CSV</h2>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-4 block text-black"
      />

      {preview.length > 0 && (
        <div className="bg-black/30 rounded p-4 text-sm mb-4 overflow-auto max-h-64">
          <table className="table-auto w-full">
            <thead>
              <tr>
                {preview[0].map((col, idx) => (
                  <th key={idx} className="text-left px-2 py-1">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {preview.slice(1).map((row, rIdx) => (
                <tr key={rIdx}>
                  {row.map((cell, cIdx) => (
                    <td key={cIdx} className="px-2 py-1">{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Button onClick={uploadFile} className="bg-green-600 hover:bg-green-700">
        🔄 Generate Report
      </Button>

      {pdfLink && (
        <div className="mt-4">
          <a
            href={pdfLink}
            target="_blank"
            className="underline text-blue-400 hover:text-blue-300"
          >
            📄 View Generated Report
          </a>
        </div>
      )}
    </div>
  );
}
