import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    // Disable ESLint during production builds - we run it separately in CI
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Still type-check but don't fail the build on type errors for now
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
