import React, { useState } from 'react';
import { Play, RotateCcw, ShieldCheck, ShieldAlert, Clock, ListChecks, History } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [requestId, setRequestId] = useState(`req_${Math.floor(Math.random() * 100000)}`);
  const [workflowId, setWorkflowId] = useState('payment_workflow');
  const [amount, setAmount] = useState(500);
  const [currency, setCurrency] = useState('USD');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const processWorkflow = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('/api/workflow/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          requestId,
          workflowId,
          payload: { amount, currency }
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error processing workflow:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetRequest = () => {
    setRequestId(`req_${Math.floor(Math.random() * 100000)}`);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-[#E4E3E0] text-[#141414] font-sans p-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-12 border-b border-[#141414] pb-6 flex justify-between items-end">
          <div>
            <h1 className="font-serif italic text-5xl mb-2">Workflow Decision Platform</h1>
            <p className="text-sm opacity-60 uppercase tracking-widest">Configurable Decision Engine v1.0</p>
          </div>
          <div className="text-right">
            <span className="font-mono text-xs opacity-50">SYSTEM STATUS:</span>
            <span className="ml-2 font-mono text-xs text-emerald-600 font-bold">OPERATIONAL</span>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration Panel */}
          <div className="lg:col-span-1 border border-[#141414] p-6 bg-white shadow-[4px_4px_0px_0px_rgba(20,20,20,1)]">
            <h2 className="font-serif italic text-xl mb-6 flex items-center gap-2">
              <ListChecks size={20} /> Input Parameters
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block font-mono text-[10px] uppercase opacity-50 mb-1">Request ID</label>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    value={requestId} 
                    onChange={(e) => setRequestId(e.target.value)}
                    className="w-full border border-[#141414] p-2 font-mono text-sm focus:outline-none focus:bg-yellow-50"
                  />
                  <button onClick={resetRequest} className="border border-[#141414] p-2 hover:bg-[#141414] hover:text-white transition-colors">
                    <RotateCcw size={16} />
                  </button>
                </div>
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase opacity-50 mb-1">Workflow ID</label>
                <select 
                  value={workflowId} 
                  onChange={(e) => setWorkflowId(e.target.value)}
                  className="w-full border border-[#141414] p-2 font-mono text-sm focus:outline-none"
                >
                  <option value="payment_workflow">payment_workflow</option>
                </select>
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase opacity-50 mb-1">Amount</label>
                <input 
                  type="number" 
                  value={amount} 
                  onChange={(e) => setAmount(Number(e.target.value))}
                  className="w-full border border-[#141414] p-2 font-mono text-sm focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase opacity-50 mb-1">Currency</label>
                <select 
                  value={currency} 
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full border border-[#141414] p-2 font-mono text-sm focus:outline-none"
                >
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                </select>
              </div>

              <button 
                onClick={processWorkflow}
                disabled={loading}
                className="w-full mt-4 bg-[#141414] text-white p-4 font-mono text-sm uppercase tracking-widest hover:bg-opacity-90 disabled:opacity-50 flex items-center justify-center gap-2 transition-all active:translate-y-1"
              >
                {loading ? <Clock className="animate-spin" size={18} /> : <Play size={18} />}
                Execute Workflow
              </button>
            </div>
          </div>

          {/* Result Panel */}
          <div className="lg:col-span-2 space-y-8">
            <div className="border border-[#141414] p-6 bg-white shadow-[4px_4px_0px_0px_rgba(20,20,20,1)] min-h-[200px]">
              <h2 className="font-serif italic text-xl mb-6 flex items-center gap-2">
                <ShieldCheck size={20} /> Decision Result
              </h2>

              <AnimatePresence mode="wait">
                {!result && !loading && (
                  <motion.div 
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="flex flex-col items-center justify-center h-40 opacity-20"
                  >
                    <ShieldAlert size={48} />
                    <p className="font-mono text-xs mt-2 uppercase">Awaiting Input</p>
                  </motion.div>
                )}

                {loading && (
                  <motion.div 
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="flex flex-col items-center justify-center h-40"
                  >
                    <div className="w-12 h-12 border-4 border-[#141414] border-t-transparent rounded-full animate-spin"></div>
                    <p className="font-mono text-xs mt-4 uppercase animate-pulse">Processing Rules...</p>
                  </motion.div>
                )}

                {result && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    <div className="flex items-center justify-between border-b border-dashed border-[#141414] pb-4">
                      <div>
                        <p className="font-mono text-[10px] uppercase opacity-50">Final Status</p>
                        <p className={`font-mono text-xl font-bold ${result.status === 'COMPLETED' ? 'text-emerald-600' : 'text-red-600'}`}>
                          {result.status}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-mono text-[10px] uppercase opacity-50">Decision</p>
                        <p className="font-mono text-xl uppercase font-bold">
                          {result.result?.action || 'N/A'}
                        </p>
                      </div>
                    </div>

                    {result.result?.reason && (
                      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3">
                        <p className="font-mono text-xs italic">"{result.result.reason}"</p>
                      </div>
                    )}

                    <div>
                      <h3 className="font-mono text-[10px] uppercase opacity-50 mb-3 flex items-center gap-1">
                        <History size={12} /> Audit Trail
                      </h3>
                      <div className="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                        {result.auditLogs.map((log: any, i: number) => (
                          <div key={i} className="flex gap-4 text-[11px] border-b border-gray-100 py-2">
                            <span className="font-mono opacity-40 whitespace-nowrap">{new Date(log.timestamp).toLocaleTimeString()}</span>
                            <span className="font-mono font-bold uppercase w-24 whitespace-nowrap">{log.stage}</span>
                            <span className="font-sans opacity-80">{log.details}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Config Preview */}
            <div className="border border-[#141414] p-6 bg-[#141414] text-white shadow-[4px_4px_0px_0px_rgba(228,227,224,1)]">
              <h2 className="font-serif italic text-xl mb-4 text-white/80">Active Configuration</h2>
              <pre className="font-mono text-[10px] opacity-70 overflow-x-auto">
{`{
  "id": "payment_workflow",
  "rules": [
    { "condition": "amount === 777", "action": "retry" },
    { "condition": "amount > 1000", "action": "manual_review" },
    { "condition": "currency !== 'USD'", "action": "reject" },
    { "condition": "true", "action": "approve" }
  ]
}`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
