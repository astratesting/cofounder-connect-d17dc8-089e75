import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://example.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'demo-anon-key';

export type FounderProfile = {
  id: string;
  name: string;
  email: string;
  skills: string[];
  industry: string;
  stage: string;
  preferences: Record<string, unknown>;
};

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
