FROM node:18 AS build

WORKDIR /app

COPY . .
RUN npm install

RUN cd web && npm install && npm run build
RUN cd admin_panel && npm install && npm run build

# nginx stage
FROM nginx:alpine

COPY --from=build /app/web/dist /usr/share/nginx/html/web
COPY --from=build /app/admin_panel/dist /usr/share/nginx/html/admin