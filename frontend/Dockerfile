FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/vite.config.ts frontend/index.html /app/
COPY frontend/src /app/src

RUN npm ci
RUN npm run build

FROM nginx:1.27-alpine

COPY infra/docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
