"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { EmailPreferences } from "@/lib/types";

export default function PreferencesPage() {
  const { token } = useAuth();
  const [prefs, setPrefs] = useState<EmailPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    sender_name: "",
    reply_to: "",
    default_signature: true,
    append_signature: true,
    email_format: "html",
    default_cc: "",
    default_bcc: "",
    sending_limit: "",
  });

  useEffect(() => {
    if (!token) return;
    api.getPreferences(token).then((p) => {
      if (p) {
        const pd = p as EmailPreferences;
        setPrefs(pd);
        setForm({
          sender_name: pd.sender_name || "",
          reply_to: pd.reply_to || "",
          default_signature: pd.default_signature,
          append_signature: pd.append_signature,
          email_format: pd.email_format,
          default_cc: pd.default_cc || "",
          default_bcc: pd.default_bcc || "",
          sending_limit: pd.sending_limit ? String(pd.sending_limit) : "",
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
      const data = {
        ...form,
        sending_limit: form.sending_limit ? parseInt(form.sending_limit) : null,
      } as Record<string, unknown>;
      if (prefs) {
        await api.updatePreferences(token, data);
      } else {
        await api.createPreferences(token, data);
      }
      setMessage("Preferences saved successfully");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <DashboardLayout><p>Loading...</p></DashboardLayout>;

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Email Preferences</h1>
      {message && (
        <div className={`p-3 rounded mb-4 text-sm ${message.includes("success") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {message}
        </div>
      )}
      <form onSubmit={handleSave} className="bg-white p-6 rounded-lg shadow max-w-2xl">
        {[
          { key: "sender_name", label: "Default Sender Name", type: "text" },
          { key: "reply_to", label: "Default Reply-To", type: "email" },
          { key: "default_cc", label: "Default CC", type: "text" },
          { key: "default_bcc", label: "Default BCC", type: "text" },
          { key: "sending_limit", label: "Sending Limit", type: "number" },
        ].map((field) => (
          <div key={field.key} className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
            <input
              type={field.type}
              value={(form as unknown as Record<string, string>)[field.key] || ""}
              onChange={(e) => setForm({ ...form, [field.key]: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />
          </div>
        ))}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Email Format</label>
          <select
            value={form.email_format}
            onChange={(e) => setForm({ ...form, email_format: e.target.value })}
            className="w-full px-3 py-2 border rounded-md text-sm"
          >
            <option value="html">HTML</option>
            <option value="plain">Plain Text</option>
          </select>
        </div>
        <div className="flex gap-6 mb-4">
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.default_signature} onChange={(e) => setForm({ ...form, default_signature: e.target.checked })} />
            Default Signature
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.append_signature} onChange={(e) => setForm({ ...form, append_signature: e.target.checked })} />
            Append Signature Automatically
          </label>
        </div>
        <button type="submit" disabled={saving} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50">
          {saving ? "Saving..." : "Save Preferences"}
        </button>
      </form>
    </DashboardLayout>
  );
}
