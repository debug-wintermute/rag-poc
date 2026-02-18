#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Post-create setup for RAG PoC devcontainer
# =============================================================================

GITLEAKS_VERSION="8.30.0"

# --- Base tooling (shared with agent-home) ---

# 1. Install Claude Code CLI
curl -fsSL https://claude.ai/install.sh | bash

# 2. Add CLI paths to ~/.bashrc
mkdir -p ~/.local/bin
echo 'export PATH="$HOME/.local/bin:$HOME/.claude/bin:$PATH"' >> ~/.bashrc

# 3. Install gitleaks for secret scanning
curl -sSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
  | tar -xz -C ~/.local/bin gitleaks

# 4. Configure git
git config --global commit.gpgsign false
git config --global tag.gpgsign false
git config --global user.name "debug-wintermute"
git config --global user.email "debug-wintermute@users.noreply.github.com"

# 5. Fix SSH permissions
if [ -d ~/.ssh ]; then
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_ed25519 2>/dev/null || true
    chmod 644 ~/.ssh/id_ed25519.pub 2>/dev/null || true
    ssh-keyscan -t ed25519,rsa github.com >> ~/.ssh/known_hosts 2>/dev/null || true
    sort -u -o ~/.ssh/known_hosts ~/.ssh/known_hosts 2>/dev/null || true
    chmod 644 ~/.ssh/known_hosts 2>/dev/null || true
    echo "[post-create] SSH key available: $(ssh-keygen -l -f ~/.ssh/id_ed25519.pub 2>/dev/null || echo 'ERROR')"
else
    echo "[post-create] WARNING: ~/.ssh not mounted"
fi

# --- RAG PoC specific ---

# 6. Install Ollama (tarball + Python zstd extract, no systemd needed)
pip install --break-system-packages zstandard
curl -L -o /tmp/ollama.tar.zst https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64.tar.zst
python3 -c "
import zstandard, tarfile, os
with open('/tmp/ollama.tar.zst', 'rb') as f:
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(f) as reader:
        with tarfile.open(fileobj=reader, mode='r|') as tar:
            tar.extractall(path=os.path.expanduser('~/.local'), filter='data')
"
rm /tmp/ollama.tar.zst
echo "[post-create] Ollama installed: $(ollama --version 2>/dev/null || echo 'ERROR')"

# 7. Install Python dependencies for RAG PoC
pip install --break-system-packages \
  fastapi \
  uvicorn[standard] \
  chromadb \
  sentence-transformers \
  httpx \
  python-multipart \
  jinja2
echo "[post-create] Python RAG dependencies installed"

echo "[post-create] Setup complete. Run 'ollama serve &' then 'ollama pull mistral' to start."
