# -------- STAGE 1 --------
FROM node:22 AS builder

WORKDIR /app

COPY . .

# web
WORKDIR /app/web
RUN npm install
RUN npm run build

# admin
WORKDIR /app/admin_panel
RUN npm install
RUN npm run build

# -------- STAGE 2 --------
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/web/dist /usr/share/nginx/html
COPY --from=builder /app/admin_panel/dist /usr/share/nginx/html/admin