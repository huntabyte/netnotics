# pull base node image
FROM node:19-slim

# set node environment to development to ensure all packages are installed
ENV NODE_ENV=development

# create & move into the workdir
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy project files
COPY . .

# install node modules
RUN npm install

# Expose port 3000 for Sveltekit app & 24678 for Vite's HMR
EXPOSE 3000
EXPOSE 24678

# Run the dev server
CMD npm run dev --host 0.0.0.0