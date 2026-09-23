export const env = {
  APP_URL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  API_URL: process.env.NEXT_PUBLIC_API_URL || "https://finguard-api-y6pg.onrender.com/api/v1",
  ML_URL: process.env.NEXT_PUBLIC_ML_URL || "https://finguard-ml-rai3.onrender.com",
  SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL || "https://ullxarnrrjdglxsabamg.supabase.co",
  SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "sb_publishable_1Jm3Tt5uV8W38HY-Bzi2gw_0sH_g0n0",
  ENABLE_DEMO_MODE: process.env.NEXT_PUBLIC_ENABLE_DEMO_MODE === "true" || true,
};

export function validateClientEnv(): { isValid: boolean; missing: string[] } {
  const missing: string[] = [];
  if (!env.API_URL && !env.ENABLE_DEMO_MODE) {
    missing.push("NEXT_PUBLIC_API_URL");
  }
  return {
    isValid: missing.length === 0,
    missing,
  };
}
