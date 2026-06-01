import React, { useState } from 'react';

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [telemetryData, setTelemetryData] = useState(null);

  const processDocument = async (event) => {
    const activeFile = event.target.files[0];
    if (!activeFile) return;

    setSelectedFile(activeFile);
    setIsProcessing(true);
    setTelemetryData(null);

    const payload = new FormData();
    payload.append("file", activeFile);

    try {
      const endpointResponse = await fetch("http://127.0.0.1:8000/api/v1/analyze", {
        method: "POST",
        body: payload,
      });

      if (!endpointResponse.ok) {
        throw new Error("Server error");
      }

      const structuralMetrics = await endpointResponse.json();
      setTelemetryData(structuralMetrics);
    } catch (networkError) {
      console.error("Pipeline failed:", networkError);
      alert("Failed to connect to backend. Is the Python server running?");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="max-w-4xl mx-auto mb-8 pb-6 border-b border-slate-800 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-blue-500">OMNISPECT // SYSTEM ACTIVE</h1>
          <p className="text-slate-400 text-sm mt-1">Real-Time Threat Analysis Gateway</p>
        </div>
        
        {/* THE NEW ENTERPRISE EXPORT BUTTON */}
        {telemetryData && (
          <button 
            onClick={() => window.print()} 
            className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-bold py-2 px-4 rounded border border-slate-700 transition shadow-lg"
          >
            📥 Export PDF Report
          </button>
        )}
      </header>

      <main className="max-w-4xl mx-auto space-y-6">
        <section className="bg-slate-900 border border-dashed border-blue-900/60 rounded-xl p-10 text-center">
          <input type="file" accept="image/*" onChange={processDocument} id="telemetry-trigger" className="hidden" />
          <label htmlFor="telemetry-trigger" className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-6 rounded-lg cursor-pointer inline-block shadow-lg">
            {isProcessing ? "Analyzing Document..." : "Upload Target Asset"}
          </label>
        </section>

        {telemetryData && (
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-2xl">
            <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
              <h2 className="text-2xl font-black text-red-500">VERDICT: {telemetryData.status}</h2>
              <div className="text-right">
                <p className="text-xs text-slate-400 uppercase font-bold tracking-wider">Semantic Risk Score</p>
                <p className="text-2xl font-mono font-bold text-amber-400">{telemetryData.metrics.semantic_risk}/100</p>
              </div>
            </div>
            
            <h3 className="text-sm font-bold text-slate-300 mb-2 uppercase">Layer 1 Processing: ELA Heatmap</h3>
            <p className="text-slate-400 text-xs mb-4">Bright areas indicate detected pixel tampering.</p>
            
            <div className="bg-black p-4 rounded-lg flex justify-center border border-slate-950 mb-6">
              <img src={telemetryData.visuals.heatmap} alt="Analysis Result" className="max-h-96 object-contain rounded" />
            </div>

            <h3 className="text-sm font-bold text-slate-300 mb-2 uppercase">Engine Logs</h3>
            <ul className="space-y-2">
              {telemetryData.insights.map((log, idx) => (
                <li key={idx} className="text-xs font-mono text-slate-300 bg-slate-950 p-2 rounded border border-slate-800">
                  {log}
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}