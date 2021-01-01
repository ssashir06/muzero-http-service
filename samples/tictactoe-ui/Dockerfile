FROM node:15.5-alpine AS build
WORKDIR /opt/ui
COPY package-lock.json package.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM nginx:1.18
COPY --from=build /opt/ui/dist /usr/share/nginx/html/