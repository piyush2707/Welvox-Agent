/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  experimental: {
    appDir: true,
    serverComponentsExternalPackages: ['@welvox/database'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws',
  },
  typescript: {
    tsconfigPath: '../../tsconfig.json',
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@welvox/ui': require.resolve('@welvox/ui'),
      '@welvox/types': require.resolve('@welvox/types'),
      '@welvox/shared': require.resolve('@welvox/shared'),
    };
    return config;
  },
};

module.exports = nextConfig;
