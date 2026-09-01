# Out of scope for this detector (not a false negative): no USER directive
# either, but nothing in this Dockerfile identifies it as a tool server for
# the model-context protocol -- this detector only scans manifests carrying
# that signal (nonMcpDockerfile_isNotFlagged).
FROM node:20-slim

WORKDIR /app
COPY . .
RUN npm install --omit=dev

ENTRYPOINT ["node", "server.js"]
