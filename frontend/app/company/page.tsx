"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { Company } from "@/lib/types";

export default function CompanyPage() {
  const { token } = useAuth();
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    name: "",
    description: "",
    website: "",
    industry: "",
    location: "",
    contact_person: "",
    contact_email: "",
    contact_phone: "",
    address: "",
  });
  const [services, setServices] = useState<{ name: string; description: string }[]>([]);
  const [targets, setTargets] = useState<{ description: string }[]>([]);
  const [values, setValues] = useState<{ description: string }[]>([]);
  const [socials, setSocials] = useState<{ platform: string; url: string }[]>([]);

  useEffect(() => {
    if (!token) return;
    api.getCompany(token).then((c) => {
      if (c) {
        const co = c as Company;
        setCompany(co);
        setForm({
          name: co.name,
          description: co.description || "",
          website: co.website || "",
          industry: co.industry || "",
          location: co.location || "",
          contact_person: co.contact_person || "",
          contact_email: co.contact_email || "",
          contact_phone: co.contact_phone || "",
          address: co.address || "",
        });
        setServices((co.services_products || []).map(s => ({ name: s.name, description: s.description || "" })));
        setTargets((co.target_customers || []).map(t => ({ description: t.description })));
        setValues((co.value_propositions || []).map(v => ({ description: v.description })));
        setSocials((co.social_links || []).map(s => ({ platform: s.platform, url: s.url })));
      }
    }).catch(() => {}).finally(() => setLoading(false));
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    setSaving(true);
    setMessage("");
    try {
      const data = {
        ...form,
        services_products: services,
        target_customers: targets,
        value_propositions: values,
        social_links: socials,
      };
      if (company) {
        await api.updateCompany(token, data);
      } else {
        await api.createCompany(token, data);
      }
      setMessage("Company profile saved successfully");
      const c = (await api.getCompany(token)) as Company;
      setCompany(c);
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <DashboardLayout><p>Loading...</p></DashboardLayout>;

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Company Profile</h1>
      {message && (
        <div className={`p-3 rounded mb-4 text-sm ${message.includes("success") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {message}
        </div>
      )}
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow max-w-3xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { key: "name", label: "Company Name", required: true },
            { key: "description", label: "Description" },
            { key: "website", label: "Website" },
            { key: "industry", label: "Industry" },
            { key: "location", label: "Location" },
            { key: "contact_person", label: "Contact Person" },
            { key: "contact_email", label: "Contact Email" },
            { key: "contact_phone", label: "Contact Phone" },
            { key: "address", label: "Address" },
          ].map((field) => (
            <div key={field.key} className={field.key === "description" || field.key === "address" ? "md:col-span-2" : ""}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
              <input
                type="text"
                value={(form as Record<string, string>)[field.key] || ""}
                onChange={(e) => setForm({ ...form, [field.key]: e.target.value })}
                className="w-full px-3 py-2 border rounded-md text-sm"
                required={field.required}
              />
            </div>
          ))}
        </div>

        <div className="mt-6">
          <h3 className="font-semibold mb-2">Services/Products</h3>
          {services.map((s, i) => (
            <div key={i} className="flex gap-2 mb-2">
              <input
                placeholder="Name"
                value={s.name}
                onChange={(e) => { const n = [...services]; n[i] = { ...n[i], name: e.target.value }; setServices(n); }}
                className="flex-1 px-2 py-1 border rounded text-sm"
              />
              <input
                placeholder="Description"
                value={s.description || ""}
                onChange={(e) => { const n = [...services]; n[i] = { ...n[i], description: e.target.value }; setServices(n); }}
                className="flex-1 px-2 py-1 border rounded text-sm"
              />
              <button type="button" onClick={() => setServices(services.filter((_, j) => j !== i))} className="text-red-500 text-sm">Remove</button>
            </div>
          ))}
          <button type="button" onClick={() => setServices([...services, { name: "", description: "" }])} className="text-blue-600 text-sm">+ Add Service</button>
        </div>

        <div className="mt-6">
          <h3 className="font-semibold mb-2">Target Customers</h3>
          {targets.map((t, i) => (
            <div key={i} className="flex gap-2 mb-2">
              <input
                placeholder="Description"
                value={t.description}
                onChange={(e) => { const n = [...targets]; n[i] = { description: e.target.value }; setTargets(n); }}
                className="flex-1 px-2 py-1 border rounded text-sm"
              />
              <button type="button" onClick={() => setTargets(targets.filter((_, j) => j !== i))} className="text-red-500 text-sm">Remove</button>
            </div>
          ))}
          <button type="button" onClick={() => setTargets([...targets, { description: "" }])} className="text-blue-600 text-sm">+ Add Target</button>
        </div>

        <div className="mt-6">
          <h3 className="font-semibold mb-2">Value Propositions</h3>
          {values.map((v, i) => (
            <div key={i} className="flex gap-2 mb-2">
              <input
                placeholder="Description"
                value={v.description}
                onChange={(e) => { const n = [...values]; n[i] = { description: e.target.value }; setValues(n); }}
                className="flex-1 px-2 py-1 border rounded text-sm"
              />
              <button type="button" onClick={() => setValues(values.filter((_, j) => j !== i))} className="text-red-500 text-sm">Remove</button>
            </div>
          ))}
          <button type="button" onClick={() => setValues([...values, { description: "" }])} className="text-blue-600 text-sm">+ Add Value Proposition</button>
        </div>

        <div className="mt-6">
          <h3 className="font-semibold mb-2">Social Links</h3>
          {socials.map((s, i) => (
            <div key={i} className="flex gap-2 mb-2">
              <input
                placeholder="Platform"
                value={s.platform}
                onChange={(e) => { const n = [...socials]; n[i] = { ...n[i], platform: e.target.value }; setSocials(n); }}
                className="w-32 px-2 py-1 border rounded text-sm"
              />
              <input
                placeholder="URL"
                value={s.url}
                onChange={(e) => { const n = [...socials]; n[i] = { ...n[i], url: e.target.value }; setSocials(n); }}
                className="flex-1 px-2 py-1 border rounded text-sm"
              />
              <button type="button" onClick={() => setSocials(socials.filter((_, j) => j !== i))} className="text-red-500 text-sm">Remove</button>
            </div>
          ))}
          <button type="button" onClick={() => setSocials([...socials, { platform: "", url: "" }])} className="text-blue-600 text-sm">+ Add Social Link</button>
        </div>

        <button type="submit" disabled={saving} className="mt-6 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50">
          {saving ? "Saving..." : company ? "Update Profile" : "Create Profile"}
        </button>
      </form>
    </DashboardLayout>
  );
}
