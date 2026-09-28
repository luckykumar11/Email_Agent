import { TokenResponse, User } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((options.headers as Record<string, string>) || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (res.status === 401) {
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }
  if (res.status === 204) return null as T;
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  register: (data: { name: string; email: string; password: string }) =>
    request<TokenResponse>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (data: { email: string; password: string }) =>
    request<TokenResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  me: (token: string) =>
    request<User>("/api/v1/auth/me", {}, token),

  createCompany: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/company", { method: "POST", body: JSON.stringify(data) }, token),

  getCompany: (token: string) =>
    request<unknown>("/api/v1/company", {}, token),

  updateCompany: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/company", { method: "PUT", body: JSON.stringify(data) }, token),

  createEmailConfig: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/email-config", { method: "POST", body: JSON.stringify(data) }, token),

  getEmailConfig: (token: string) =>
    request<unknown>("/api/v1/email-config", {}, token),

  updateEmailConfig: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/email-config", { method: "PUT", body: JSON.stringify(data) }, token),

  testSmtp: (token: string, data: { recipient: string }) =>
    request<{ success: boolean; message: string }>("/api/v1/email-config/test", {
      method: "POST",
      body: JSON.stringify(data),
    }, token),

  createSignature: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/signature", { method: "POST", body: JSON.stringify(data) }, token),

  getSignature: (token: string) =>
    request<unknown>("/api/v1/signature", {}, token),

  updateSignature: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/signature", { method: "PUT", body: JSON.stringify(data) }, token),

  deleteSignature: (token: string) =>
    request<null>("/api/v1/signature", { method: "DELETE" }, token),

  getPreferences: (token: string) =>
    request<unknown>("/api/v1/preferences", {}, token),

  createPreferences: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/preferences", { method: "POST", body: JSON.stringify(data) }, token),

  updatePreferences: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/preferences", { method: "PUT", body: JSON.stringify(data) }, token),

  generateEmail: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/agent/generate-email", { method: "POST", body: JSON.stringify(data) }, token),

  sendEmail: (token: string, data: Record<string, unknown>) =>
    request<unknown>("/api/v1/emails/send", { method: "POST", body: JSON.stringify(data) }, token),

  getHistory: (token: string, page = 1) =>
    request<unknown>(`/api/v1/emails/history?page=${page}`, {}, token),
};
