"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import DashboardLayout from "@/app/(auth)/layout";
import { EmailHistoryItem, EmailHistoryList } from "@/lib/types";

export default function HistoryPage() {
  const { token } = useAuth();
  const [history, setHistory] = useState<EmailHistoryList | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    api.getHistory(token, page).then((h) => {
      setHistory(h as EmailHistoryList);
    }).catch(() => {}).finally(() => setLoading(false));
  }, [token, page]);

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold mb-6">Email History</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Date</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">To</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Subject</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Status</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Format</th>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {loading ? (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-500">Loading...</td></tr>
            ) : history?.emails.length === 0 ? (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-500">No emails sent yet</td></tr>
            ) : (
              history?.emails.map((email: EmailHistoryItem) => (
                <tr key={email.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-600">{new Date(email.created_at).toLocaleString()}</td>
                  <td className="px-4 py-3 text-sm">{email.recipient}</td>
                  <td className="px-4 py-3 text-sm">{email.subject}</td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs ${email.status === "sent" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                      {email.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">{email.format}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {email.failure_reason ? (
                      <span className="text-xs text-red-600" title={email.failure_reason}>
                        {email.failure_reason.length > 50
                          ? email.failure_reason.substring(0, 50) + "..."
                          : email.failure_reason}
                      </span>
                    ) : email.status === "sent" ? (
                      <span className="text-xs text-green-600">-</span>
                    ) : null}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        {history && history.total > history.page_size && (
          <div className="flex justify-between items-center px-4 py-3 border-t">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="text-sm text-blue-600 disabled:text-gray-400"
            >
              Previous
            </button>
            <span className="text-sm text-gray-600">
              Page {page} of {Math.ceil(history.total / history.page_size)}
            </span>
            <button
              onClick={() => setPage(page + 1)}
              disabled={page >= Math.ceil(history.total / history.page_size)}
              className="text-sm text-blue-600 disabled:text-gray-400"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
