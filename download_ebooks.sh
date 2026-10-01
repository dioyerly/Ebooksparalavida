#!/bin/bash
# Download ebooks from GitHub on Render startup

echo "Downloading ebooks from GitHub..."

# GitHub raw content URL
GITHUB_RAW="https://raw.githubusercontent.com/dioyerly/ebooks-store/main/ebooks_github"

# Create storage directories
mkdir -p storage/ebooks
mkdir -p storage/interactive_ebooks

# Download PDF ebooks
echo "Downloading PDFs..."
curl -s -o storage/ebooks/convivir-sin-apagar-incendios.pdf "$GITHUB_RAW/convivir-sin-apagar-incendios.pdf" || true
curl -s -o storage/ebooks/kit-convivir-sin-apagar-incendios.pdf "$GITHUB_RAW/kit-convivir-sin-apagar-incendios.pdf" || true
curl -s -o storage/ebooks/primero-tu-mente-despues-tu-hogar.pdf "$GITHUB_RAW/primero-tu-mente-despues-tu-hogar.pdf" || true
curl -s -o storage/ebooks/Descubre_tu_identidad_como_lectora.pdf "$GITHUB_RAW/Descubre_tu_identidad_como_lectora.pdf" || true

# Download interactive ebook
echo "Downloading interactive ebooks..."
curl -s -o storage/interactive_ebooks/the-romance-reader-kit.html "$GITHUB_RAW/the-romance-reader-kit.html" || true

echo "Ebooks downloaded successfully!"
