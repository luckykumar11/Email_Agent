"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { EmailSignature } from "@/lib/types";

export default function SignaturePage() {
  const { token } = useAuth();
  const [sig, setSig] = useState<EmailSignature | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    signature_text: "",
    enabled: true,
    append_automatically: true,
  });

  useEffect(() => {
    if (!token) return;
    api.getSignature(token).then((s) => {
      if (s) {
        const sigData = s as EmailSignature;
        setSig(sigData);
        setForm({
          signature_text: sigData.signature_text,
          enabled: sigData.enabled,
          append_automatically: sigData.append_automatically,
        });
      }
    }).catch(() => {}).finally(() => setLoading(false));
  }, [token]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    setSaving(true);
    setMessage("");
    try {
      if (sig) {
        await api.updateSignature(token, form);
      } else {
        await api.createSignature(token, form);
      }
      setMessage("Signature saved successfully");
      const s = (await api.getSignature(token)) as EmailSignature;
      setSig(s);
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!token || !sig) return;
    if (!confirm("Delete signature?")) return;
    try {
      await api.deleteSignature(token);
      setSig(null);
      setForm({ signature_text: "", enabled: true, append_automatically: true });
      setMessage("Signature deleted");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Failed to delete");
    }
  };

  if (loading) return <DashboardLayout><p>Loading...</p></DashboardLayout>;

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Email Signature</h1>
      {message && (
        <div className={`p-3 rounded mb-4 text-sm ${message.includes("success") || message.includes("deleted") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {message}
        </div>
      )}
      <div className="bg-white p-6 rounded-lg shadow max-w-2xl">
        <form onSubmit={handleSave}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Signature Text</label>
            <textarea
              value={form.signature_text}
              onChange={(e) => setForm({ ...form, signature_text: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm h-32"
              required
              placeholder="Best Regards,&#10;John Doe&#10;CEO&#10;ABC Technologies"
            />
          </div>
          <div className="flex gap-6 mb-4">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={form.enabled}
                onChange={(e) => setForm({ ...form, enabled: e.target.checked })}
              />
              Enabled
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={form.append_automatically}
                onChange={(e) => setForm({ ...form, append_automatically: e.target.checked })}
              />
              Append Automatically
            </label>
          </div>

          <div className="mb-6 p-4 bg-gray-50 rounded border">
            <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
            <pre className="text-sm text-gray-600 whitespace-pre-wrap">{form.signature_text || "No signature"}</pre>
          </div>

          <button type="submit" disabled={saving} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50">
            {saving ? "Saving..." : "Save Signature"}
          </button>
          {sig && (
            <button type="button" onClick={handleDelete} className="ml-2 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">
              Delete
            </button>
          )}
        </form>
      </div>
    </DashboardLayout>
  );
}
