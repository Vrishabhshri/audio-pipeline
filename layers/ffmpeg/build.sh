#!/bin/bash
# Run this locally, before your first `sam build`, to populate the
# ffmpeg layer. The binary itself is not committed to the repo, since
# it's a large compiled artifact, this script fetches it on demand.
set -e
cd "$(dirname "$0")"
mkdir -p bin
curl -L -o /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf /tmp/ffmpeg.tar.xz -C /tmp
cp /tmp/ffmpeg-*-static/ffmpeg bin/
chmod +x bin/ffmpeg
echo "ffmpeg binary placed in layers/ffmpeg/bin/"
