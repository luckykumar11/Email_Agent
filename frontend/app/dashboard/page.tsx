"use client";

import DashboardLayout from "@/app/(auth)/layout";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <a href="/company" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Company Profile</h3>
          <p className="text-gray-600 text-sm mt-2">Manage your company information and details</p>
        </a>
        <a href="/email-config" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Email Configuration</h3>
          <p className="text-gray-600 text-sm mt-2">Configure SMTP settings and test connection</p>
        </a>
        <a href="/signature" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Email Signature</h3>
          <p className="text-gray-600 text-sm mt-2">Set up your email signature</p>
        </a>
        <a href="/preferences" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Email Preferences</h3>
          <p className="text-gray-600 text-sm mt-2">Configure sending preferences</p>
        </a>
        <a href="/agent" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Email Agent</h3>
          <p className="text-gray-600 text-sm mt-2">AI-powered email generation</p>
        </a>
        <a href="/history" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition">
          <h3 className="font-semibold text-lg">Email History</h3>
          <p className="text-gray-600 text-sm mt-2">View sent email history</p>
        </a>
      </div>
    </DashboardLayout>
  );
}
