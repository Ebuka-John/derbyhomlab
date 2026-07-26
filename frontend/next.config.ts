import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Enables a minimal Node server image for Docker (copies .next/standalone)
  output: "standalone",
};

export default nextConfig;
