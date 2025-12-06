import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: './tests/setupTests.ts',
    globals: true,
    exclude: ['tests/e2e/**', 'node_modules/**', 'dist/**', '.next/**'],
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
