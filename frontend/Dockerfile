# -------- STAGE 1: build frontend --------
FROM node:22 AS builder

WORKDIR /app

# копируем весь фронт
COPY . .

# билд web
WORKDIR /app/frontend/web
RUN npm install
RUN npm run build

# билд admin
WORKDIR /app/frontend/admin_panel
RUN npm install
RUN npm run build


# -------- STAGE 2: nginx --------
FROM nginx:alpine

# nginx config
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

# копируем билды
COPY --from=builder /app/frontend/web/dist /usr/share/nginx/html/web
COPY --from=builder /app/frontend/admin_panel/dist /usr/share/nginx/html/admin