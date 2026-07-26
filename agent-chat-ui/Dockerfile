FROM node:22-alpine AS base

ARG GIT_REPO_URL
ARG GIT_REPO_BRANCH=main

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable && corepack prepare pnpm@10.5.1 --activate

FROM base AS deps
WORKDIR /app

RUN apk add --no-cache git

RUN rm -rf /app/* /app/.[!.]* /app/..?* 2>/dev/null || true && \
    if [ -z "$GIT_REPO_URL" ]; then \
      echo "GIT_REPO_URL build argument is required" >&2 && exit 1; \
    fi && \
    git clone --depth 1 --branch "$GIT_REPO_BRANCH" "$GIT_REPO_URL" /app

WORKDIR /app
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app /app

RUN if [ -f next.config.mjs ] && ! grep -q 'output: "standalone"' next.config.mjs; then \
      sed -i '/^const nextConfig = {/a\  output: "standalone",' next.config.mjs; \
    fi

RUN pnpm build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
RUN mkdir -p /app/public

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

CMD ["node", "server.js"]
