import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    assetsDir: "static",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: "static/main.js",
        chunkFileNames: "static/[name].js",
        assetFileNames: "static/[name].[ext]",
      },
    },
  },
})