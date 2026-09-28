"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { GeneratedEmail } from "@/lib/types";

export default function AgentPage() {
  const { token } = useAuth();
  const [form, setForm] = useState({
    recipient_name: "",
    recipient_email: "",
    purpose: "",
    tone: "professional",
    additional_instructions: "",
  });
  const [generated, setGenerated] = useState<GeneratedEmail | null>(null);
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [generating, setGenerating] = useState(false);
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState("");

  const handleGenerate = async () => {
    if (!token) return;
    setGenerating(true);
    setMessage("");
    try {
      const res = (await api.generateEmail(token, form)) as GeneratedEmail;
      setGenerated(res);
      setSubject(res.subject);
      setBody(res.body);
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setGenerating(false);
    }
  };

  const handleSend = async () => {
    if (!token || !generated) return;
    setSending(true);
    setMessage("");
    try {
      await api.sendEmail(token, {
        recipient: generated.recipient_email,
        subject,
        body,
        format: "html",
      });
      setMessage("Email sent successfully!");
      setGenerated(null);
      setSubject("");
      setBody("");
      setForm({ recipient_name: "", recipient_email: "", purpose: "", tone: "professional", additional_instructions: "" });
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Send failed");
    } finally {
      setSending(false);
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Email Agent</h1>
      {message && (
        <div className={`p-3 rounded mb-4 text-sm ${message.includes("success") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Compose</h2>
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-1">Recipient Name</label>
            <input type="text" value={form.recipient_name} onChange={(e) => setForm({ ...form, recipient_name: e.target.value })} className="w-full px-3 py-2 border rounded-md text-sm" required />
          </div>
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-1">Recipient Email</label>
            <input type="email" value={form.recipient_email} onChange={(e) => setForm({ ...form, recipient_email: e.target.value })} className="w-full px-3 py-2 border rounded-md text-sm" required />
          </div>
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-1">Purpose</label>
            <textarea value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} className="w-full px-3 py-2 border rounded-md text-sm h-20" required placeholder="e.g., Introduce our CRM product to a small business" />
          </div>
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-1">Tone</label>
            <select value={form.tone} onChange={(e) => setForm({ ...form, tone: e.target.value })} className="w-full px-3 py-2 border rounded-md text-sm">
              <option value="professional">Professional</option>
              <option value="formal">Formal</option>
              <option value="friendly">Friendly</option>
              <option value="casual">Casual</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Additional Instructions</label>
            <textarea value={form.additional_instructions} onChange={(e) => setForm({ ...form, additional_instructions: e.target.value })} className="w-full px-3 py-2 border rounded-md text-sm h-16" placeholder="e.g., Keep the email concise" />
          </div>
          <button onClick={handleGenerate} disabled={generating || !form.recipient_name || !form.recipient_email || !form.purpose} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50">
            {generating ? "Generating..." : "Generate Email"}
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Generated Email</h2>
          {generated ? (
            <>
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} className="w-full px-3 py-2 border rounded-md text-sm" />
              </div>
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">To</label>
                <p className="text-sm text-gray-600">{generated.recipient_name} ({generated.recipient_email})</p>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Body</label>
                <textarea value={body} onChange={(e) => setBody(e.target.value)} className="w-full px-3 py-2 border rounded-md text-sm h-48" />
              </div>
              <div className="flex gap-2">
                <button onClick={handleGenerate} disabled={generating} className="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 disabled:opacity-50">
                  {generating ? "Generating..." : "Generate Again"}
                </button>
                <button onClick={handleSend} disabled={sending} className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50">
                  {sending ? "Sending..." : "Send Email"}
                </button>
              </div>
            </>
          ) : (
            <p className="text-gray-500 text-sm">Fill in the form and click &quot;Generate Email&quot; to create an email using AI.</p>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
