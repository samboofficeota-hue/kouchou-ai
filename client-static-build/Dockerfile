FROM node:22-alpine AS builder

WORKDIR /app
COPY ./client-static-build .
RUN npm ci
RUN npm run build

WORKDIR /client
COPY ./client/package.json ./client/package-lock.json ./
RUN npm ci

FROM node:22-alpine AS runner

WORKDIR /app
ARG NEXT_PUBLIC_API_BASEPATH
ARG NEXT_PUBLIC_PUBLIC_API_KEY
ARG NEXT_PUBLIC_SITE_URL
ARG API_BASEPATH

ENV NEXT_PUBLIC_API_BASEPATH=${NEXT_PUBLIC_API_BASEPATH}
ENV NEXT_PUBLIC_PUBLIC_API_KEY=${NEXT_PUBLIC_PUBLIC_API_KEY}
ENV NEXT_PUBLIC_SITE_URL=${NEXT_PUBLIC_SITE_URL}
ENV API_BASEPATH=${API_BASEPATH}

ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_DISABLE_FETCH_DURING_BUILD=true
ENV NODE_ENV=production

COPY ./client /client
COPY ./server/public /server/public
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /client/node_modules /client/node_modules

EXPOSE 3200
CMD ["node", "dist/index.js"]
