export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Company {
  id: number;
  name: string;
  description?: string;
  website?: string;
  industry?: string;
  location?: string;
  contact_person?: string;
  contact_email?: string;
  contact_phone?: string;
  address?: string;
  services_products: ServiceProduct[];
  target_customers: TargetCustomer[];
  value_propositions: ValueProposition[];
  social_links: SocialLink[];
  created_at: string;
  updated_at: string;
}

export interface ServiceProduct {
  id?: number;
  name: string;
  description?: string;
}

export interface TargetCustomer {
  id?: number;
  description: string;
}

export interface ValueProposition {
  id?: number;
  description: string;
}

export interface SocialLink {
  id?: number;
  platform: string;
  url: string;
}

export interface EmailConfig {
  id: number;
  email_address: string;
  smtp_host: string;
  smtp_port: number;
  username: string;
  password_configured: boolean;
  security_type: string;
  sender_name?: string;
  reply_to?: string;
  created_at: string;
  updated_at: string;
}

export interface EmailSignature {
  id: number;
  signature_text: string;
  enabled: boolean;
  append_automatically: boolean;
  created_at: string;
  updated_at: string;
}

export interface EmailPreferences {
  id: number;
  sender_name?: string;
  reply_to?: string;
  default_signature: boolean;
  append_signature: boolean;
  email_format: string;
  default_cc?: string;
  default_bcc?: string;
  sending_limit?: number;
  created_at: string;
  updated_at: string;
}

export interface GeneratedEmail {
  subject: string;
  body: string;
  recipient_name: string;
  recipient_email: string;
}

export interface EmailHistoryItem {
  id: number;
  sender: string;
  recipient: string;
  cc?: string;
  bcc?: string;
  subject: string;
  status: string;
  format: string;
  failure_reason?: string;
  created_at: string;
}

export interface EmailHistoryList {
  emails: EmailHistoryItem[];
  total: number;
  page: number;
  page_size: number;
}
