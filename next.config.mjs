/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@libsql/client'],
    outputFileTracingIncludes: {
      '/api/**/*': ['./econometria.db'],
    },
  },
};

export default nextConfig;
