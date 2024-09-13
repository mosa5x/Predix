FROM node:16

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install --save-dev @babel/plugin-proposal-private-property-in-object

COPY . .

RUN mkdir -p /app/node_modules/.cache && chown -R node:node /app

USER node

CMD ["npm", "start"]
