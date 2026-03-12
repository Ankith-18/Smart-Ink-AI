import { useMemo, useState } from 'react';
import DrawingCanvas from './components/DrawingCanvas';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [image, setImage] = useState('');
  const [textHint, setTextHint] = useState('');
  const [result, setResult] = useState({});
  const [loading, setLoading] = useState(false);

  const suggestions = useMemo(() => {
    const s = [];
    if (result.expression?.is_expression) s.push(`Calculate result: ${result.expression.result}`);
    if (result.phone?.is_phone) s.push(`Call number: ${result.phone.value}`);
    if (result.phone?.is_phone) s.push(`Save contact: ${result.phone.value}`);
    if (result.email?.is_email) s.push(`Send email to ${result.email.value}`);
    if (result.shape?.shape) s.push(`Convert to perfect ${result.shape.shape}`);
    return s;
  }, [result]);

  const analyze = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const payload = { image_base64: image, text_hint: textHint };
      const [digit, expression, phone, email, shape] = await Promise.all([
        fetch(`${API_BASE}/predict-digit`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then((r) => r.json()),
        fetch(`${API_BASE}/detect-expression`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then((r) => r.json()),
        fetch(`${API_BASE}/detect-phone`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then((r) => r.json()),
        fetch(`${API_BASE}/detect-email`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then((r) => r.json()),
        fetch(`${API_BASE}/detect-shape`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then((r) => r.json()),
      ]);
      setResult({ digit, expression, phone, email, shape });
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6">
        <section className="md:col-span-2 bg-white rounded-2xl shadow p-6 space-y-4">
          <h1 className="text-2xl font-bold text-slate-800">SMART INK AI</h1>
          <p className="text-slate-600">Draw digits, shapes, or rough commands on canvas and let AI interpret it.</p>
          <DrawingCanvas onImageChange={setImage} />
          <input
            value={textHint}
            onChange={(e) => setTextHint(e.target.value)}
            placeholder="Optional hint: e.g. 4+5, john@mail.com, 9876543210"
            className="w-full border rounded-lg p-2"
          />
          <button
            type="button"
            onClick={analyze}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-indigo-300"
          >
            {loading ? 'Analyzing...' : 'Analyze Ink'}
          </button>
        </section>

        <aside className="bg-white rounded-2xl shadow p-6 space-y-4">
          <h2 className="text-xl font-semibold">Results</h2>
          {result.error && <p className="text-red-600">Error: {result.error}</p>}
          <div className="text-sm space-y-1">
            <p><strong>Digit:</strong> {result.digit?.digit ?? '-'}</p>
            <p><strong>Confidence:</strong> {result.digit?.confidence ? `${(result.digit.confidence * 100).toFixed(2)}%` : '-'}</p>
            <p><strong>Expression:</strong> {result.expression?.normalized || '-'}</p>
            <p><strong>Expression Result:</strong> {result.expression?.result ?? '-'}</p>
            <p><strong>Phone:</strong> {result.phone?.value || '-'}</p>
            <p><strong>Email:</strong> {result.email?.value || '-'}</p>
            <p><strong>Shape:</strong> {result.shape?.shape || '-'}</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Smart Suggestions</h3>
            {suggestions.length === 0 ? (
              <p className="text-sm text-slate-500">No smart actions yet.</p>
            ) : (
              <ul className="space-y-2 text-sm">
                {suggestions.map((s) => (
                  <li key={s} className="bg-indigo-50 rounded-lg p-2">{s}</li>
                ))}
              </ul>
            )}
          </div>
        </aside>
      </div>
    </main>
  );
}
