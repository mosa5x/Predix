FROM node:16

WORKDIR /app

COPY package.json ./
RUN npm install
RUN npm install axios
RUN npm install @babel/plugin-proposal-private-property-in-object --save-dev
RUN npm install react-router-dom

COPY --chown=node:node . .
USER node
RUN mkdir -p /app/node_modules/.cache

CMD ["npm", "start"]