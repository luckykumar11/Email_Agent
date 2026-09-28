"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { EmailConfig } from "@/lib/types";

export default function EmailConfigPage() {
  const { token } = useAuth();
  const [config, setConfig] = useState<EmailConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [testRecipient, setTestRecipient] = useState("");
  const [testResult, setTestResult] = useState("");
  const [testing, setTesting] = useState(false);
  const [form, setForm] = useState({
    email_address: "",
    smtp_host: "",
    smtp_port: "587",
    username: "",
    password: "",
    security_type: "STARTTLS",
    sender_name: "",
    reply_to: "",
  });

  useEffect(() => {
    if (!token) return;
    api.getEmailConfig(token).then((c) => {
      if (c) {
        const co = c as EmailConfig;
        setConfig(co);
        setForm({
          email_address: co.email_address,
          smtp_host: co.smtp_host,
          smtp_port: String(co.smtp_port),
          username: co.username,
          password: "",
          security_type: co.security_type,
          sender_name: co.sender_name || "",
          reply_to: co.reply_to || "",
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
      const data: Record<string, unknown> = {
        ...form,
        smtp_port: parseInt(form.smtp_port),
      };
      if (!form.password && config) {
        delete data.password;
      }
      if (config) {
        await api.updateEmailConfig(token, data);
      } else {
        await api.createEmailConfig(token, data);
      }
      setMessage("Email configuration saved successfully");
      const c = (await api.getEmailConfig(token)) as EmailConfig;
      setConfig(c);
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    if (!token || !testRecipient) return;
    setTesting(true);
    setTestResult("");
    try {
      const res = await api.testSmtp(token, { recipient: testRecipient });
      setTestResult(res.message);
    } catch (err: unknown) {
      setTestResult(err instanceof Error ? err.message : "Test failed");
    } finally {
      setTesting(false);
    }
  };

  if (loading) return <DashboardLayout><p>Loading...</p></DashboardLayout>;

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Email Configuration</h1>
      {message && (
        <div className={`p-3 rounded mb-4 text-sm ${message.includes("success") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {message}
        </div>
      )}
      <div className="bg-white p-6 rounded-lg shadow max-w-2xl">
        <form onSubmit={handleSave}>
          {[
            { key: "email_address", label: "Email Address", type: "email" },
            { key: "smtp_host", label: "SMTP Host", type: "text" },
            { key: "smtp_port", label: "SMTP Port", type: "number" },
            { key: "username", label: "Username", type: "text" },
            { key: "password", label: config ? "New Password (leave blank to keep)" : "Password", type: "password" },
            { key: "sender_name", label: "Sender Name", type: "text" },
            { key: "reply_to", label: "Reply-To", type: "email" },
          ].map((field) => (
            <div key={field.key} className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
              <input
                type={field.type}
                value={(form as Record<string, string>)[field.key] || ""}
                onChange={(e) => setForm({ ...form, [field.key]: e.target.value })}
                className="w-full px-3 py-2 border rounded-md text-sm"
                required={field.key !== "password" && field.key !== "sender_name" && field.key !== "reply_to"}
              />
            </div>
          ))}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Security Type</label>
            <select
              value={form.security_type}
              onChange={(e) => setForm({ ...form, security_type: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            >
              <option value="NONE">None</option>
              <option value="STARTTLS">STARTTLS</option>
              <option value="SSL_TLS">SSL/TLS</option>
            </select>
          </div>
          {config && (
            <p className="text-sm text-gray-500 mb-4">
              Password configured: <span className="font-medium text-green-600">Yes</span>
            </p>
          )}
          <button type="submit" disabled={saving} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 mr-2">
            {saving ? "Saving..." : "Save Configuration"}
          </button>
        </form>
      </div>

      <div className="bg-white p-6 rounded-lg shadow max-w-2xl mt-6">
        <h2 className="text-lg font-semibold mb-4">Test SMTP Connection</h2>
        <div className="flex gap-2">
          <input
            type="email"
            placeholder="Test recipient email"
            value={testRecipient}
            onChange={(e) => setTestRecipient(e.target.value)}
            className="flex-1 px-3 py-2 border rounded-md text-sm"
          />
          <button
            onClick={handleTest}
            disabled={testing || !testRecipient}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
          >
            {testing ? "Testing..." : "Test Connection"}
          </button>
        </div>
        {testResult && (
          <p className={`mt-3 text-sm ${testResult.includes("success") || testResult.includes("successful") ? "text-green-600" : "text-red-600"}`}>
            {testResult}
          </p>
        )}
      </div>
    </DashboardLayout>
  );
}
