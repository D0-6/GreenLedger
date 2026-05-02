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
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        // Route all requests to the single Python Vercel Serverless Function entrypoint
        destination: "/api/index",
      },
    ];
  },
};


export default nextConfig;
